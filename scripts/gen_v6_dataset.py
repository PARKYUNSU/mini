#!/usr/bin/env python3
"""yunsur_v6 학습 데이터 생성 — v5 파이프라인 재사용 + 두 가지 변경.

docs/experiments/yunsur_v6/README.md §4 의 두 변수를 구현한다.
  1) 코딩 거절 필터 교체: comment_heavy(주석 비율) 해제 → multi_block + self_revision
  2) RAG 이스케이프 수정: literal `\\n`(역슬래시+n) → 진짜 개행 (v5 400건 중 175건)

잡담·계획은 v5 raw 를 그대로 흡수하고, 코딩만 새 필터로 다시 만든다.
건수·하이퍼파라미터·seed 는 v5 와 같다 (RAG 400건은 같은 seed → 같은 샘플).

  # 1) 새 필터를 v5 생성분에 소급 적용해 거절률만 본다 (LLM 없이, 맥북에서도 빠름)
  python scripts/gen_v6_dataset.py --audit

  # 2) v5 raw 흡수 후 부족분만 생성 → 조립 (맥미니, Ollama 필요)
  python scripts/gen_v6_dataset.py --import-v5-raw

  # 3) 생성 없이 재조립만 / 결과 검증
  python scripts/gen_v6_dataset.py --assemble
  python scripts/gen_v6_dataset.py --verify

--audit 와 --verify 는 무거운 임포트(core.graph 등)를 하지 않는다. 생성·조립 때만
scripts/gen_v5_dataset.py 를 불러 전역을 v6 로 갈아끼운다 — 파이프라인을 복제하지 않고
바뀐 부분만 덮어써서 두 버전이 갈라지지 않게 한다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v6"
V5_DIR = ROOT / "finetune_datasets" / "v5"
V6_DIR = ROOT / "finetune_datasets" / VERSION
TRAIN_V5 = V5_DIR / f"train_data_v5.jsonl"
TRAIN_V6 = V6_DIR / f"train_data_{VERSION}.jsonl"

# ── 변수 1: 코딩 거절 필터 (README §4)
# v5 의 실패 원문에서 추린 표현들. 한 번 쓴 구현을 주석으로 의심하고 다시 쓰기 시작하는 신호.
SELF_REVISION_RE = re.compile(
    r"재작성"
    r"|다시\s*(?:쓰|작성)"
    r"|로직\s*수정"
    r"|수정\s*(?:필요|하겠|합니다|해야|하면)"
    r"|올바른\s*(?:구현|코드|방식|피보나치)"
    r"|더\s*(?:간결|정확|직관|짧)"
    r"|또는\s*(?:다음|기존|아래|이렇게|단순히)"
    r"|실제로\s*요청하신"
    r"|코드\s*참조"
    r"|앞서(?:의|서)"
    r"|대신\s*이렇게"
)
FENCE_TOKEN_RE = re.compile(r"```")


def literal_newlines(text: str) -> int:
    """진짜 개행이 아니라 역슬래시+n 두 글자의 개수."""
    return (text or "").count("\\n")


def unescape_newlines(text: str) -> str:
    return (text or "").replace("\\n", "\n")


def fence_count(output: str) -> int:
    return len(FENCE_TOKEN_RE.findall(output or ""))


def coding_reject(output: str) -> str:
    """v6 가 새로 거절하는 사유. 통과면 ''.

    multi_block  — 펜스 토큰 3개 이상. 닫힌 블록 하나 + 열린 블록 하나부터 걸린다.
    self_revision — 자기 수정 표현. v5 실패는 대부분 한 블록 안에서 일어나므로 이쪽이 주력이다.
    """
    if fence_count(output) >= 3:
        return "multi_block"
    m = SELF_REVISION_RE.search(output or "")
    if m:
        return "self_revision"
    return ""


def _read_jsonl(p: Path) -> list[dict]:
    if not p.is_file():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


# ---------------------------------------------------------------- --audit
def audit() -> int:
    """새 필터를 v5 생성분에 소급 적용한다. 목표 300건을 채울 수 있는지 먼저 본다."""
    print("===== v6 코딩 필터 소급 적용 (v5 생성분) =====\n")

    raw = _read_jsonl(V5_DIR / "raw" / "coding.jsonl")
    passed = [r for r in raw if r.get("output") and not r.get("reject_reason")]
    print(f"v5 코딩 raw: {len(raw)}건, 그중 v5 필터 통과 {len(passed)}건")

    reasons = Counter()
    hits = Counter()
    for r in passed:
        why = coding_reject(r["output"])
        reasons[why or "pass"] += 1
        if why == "self_revision":
            m = SELF_REVISION_RE.search(r["output"])
            if m:
                hits[m.group(0).strip()] += 1
    keep = reasons["pass"]
    print(f"v6 필터 적용 후: 통과 {keep}건 / 거절 {len(passed) - keep}건 {dict(reasons)}")
    if passed:
        print(f"  → 통과율 {100 * keep / len(passed):.0f}%")
    if keep < 300:
        print(f"  ⚠️ 목표 300건 미달 — {300 - keep}건을 새로 생성해야 한다")
    else:
        print("  목표 300건 충족 — 재생성 없이 조립만으로 가능")

    if hits:
        print("\nself_revision 을 발동시킨 표현 (상위 12):")
        for phrase, n in hits.most_common(12):
            print(f"  {n:4}회  {phrase!r}")

    # v5 가 comment_heavy 로 버렸던 것들이 v6 에서는 살아나는가
    rej = [r for r in _read_jsonl(V5_DIR / "rejected.jsonl") if r.get("reason") == "comment_heavy"]
    print(f"\nv5 가 comment_heavy 로 거절한 {len(rej)}건 — v6 는 이 규칙을 해제한다")

    # 학습 파일 기준 교차 확인
    tr = [r for r in _read_jsonl(TRAIN_V5) if r.get("slot") == "coding"]
    tr_rej = Counter(coding_reject(r["output"]) or "pass" for r in tr)
    print(f"\nv5 train_data 의 코딩 {len(tr)}건에 v6 필터: {dict(tr_rej)}")

    # RAG 이스케이프 현황
    rag = [r for r in _read_jsonl(TRAIN_V5) if r.get("slot") == "rag"]
    bad = [r for r in rag if literal_newlines(r.get("output", "")) or literal_newlines(r.get("instruction", ""))]
    print(f"\n===== RAG 이스케이프 =====")
    print(f"v5 RAG {len(rag)}건 중 literal \\n 포함 {len(bad)}건 ({100 * len(bad) / max(1, len(rag)):.0f}%)")
    if bad:
        tot = sum(literal_newlines(r["output"]) for r in bad)
        print(f"  총 {tot}개 — v6 는 이를 진짜 개행으로 되돌린다")
    other = [
        r for r in _read_jsonl(TRAIN_V5)
        if r.get("slot") != "rag" and literal_newlines(r.get("output", ""))
    ]
    print(f"다른 슬롯의 literal \\n: {len(other)}건 " + (f"{Counter(r['slot'] for r in other)}" if other else ""))
    for r in other:
        print(f"  [{r['slot']}] {r['output'][:90]!r}  ← 코드 안 정상 문자열이면 건드리지 않는다")
    return 0


# ---------------------------------------------------------------- --verify
def verify() -> int:
    rows = _read_jsonl(TRAIN_V6)
    if not rows:
        print(f"❌ {TRAIN_V6} 없음 — 먼저 생성·조립할 것")
        return 1
    dist = Counter(r["slot"] for r in rows)
    print(f"{TRAIN_V6}: {len(rows)}건 {dict(dist)}")
    rc = 0

    rag_bad = [r for r in rows if r["slot"] == "rag" and literal_newlines(r.get("output", ""))]
    if rag_bad:
        print(f"❌ RAG 에 literal \\n 이 {len(rag_bad)}건 남았다 — 이스케이프 수정이 안 먹었다")
        rc = 1
    else:
        print("✅ RAG literal \\n 0건")

    cod = [r for r in rows if r["slot"] == "coding"]
    cod_lit = [r for r in cod if literal_newlines(r.get("output", ""))]
    print(f"   코딩 {len(cod)}건 중 literal \\n 포함 {len(cod_lit)}건 (파이썬 코드 안 정상 문자열이면 보존이 맞다)")
    for r in cod_lit:
        print(f"     {r['output'][:90]!r}")

    bad_filter = [(r, coding_reject(r["output"])) for r in cod]
    bad_filter = [(r, w) for r, w in bad_filter if w]
    if bad_filter:
        print(f"❌ 코딩 {len(bad_filter)}건이 v6 필터에 걸리는데 학습 파일에 들어 있다 {Counter(w for _, w in bad_filter)}")
        rc = 1
    else:
        print("✅ 코딩 전건이 v6 필터 통과")
    return rc


# ---------------------------------------------------------------- 생성·조립 (무거운 임포트)
def _load_v5_pipeline():
    """gen_v5_dataset 을 불러 전역을 v6 로 갈아끼운다."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("_gen_v5", ROOT / "scripts" / "gen_v5_dataset.py")
    g5 = importlib.util.module_from_spec(spec)
    sys.modules["_gen_v5"] = g5
    spec.loader.exec_module(g5)

    # 경로: 출력은 v6, 흡수 원본(V4_RAW_DIR)은 v5 raw, 시드는 v6 전용이 있으면 그것
    g5.VERSION = VERSION
    g5.RAW_DIR = V6_DIR / "raw"
    g5.REJECT_PATH = V6_DIR / "rejected.jsonl"
    g5.TRAIN_PATH = TRAIN_V6
    g5.STATS_PATH = V6_DIR / "stats.json"
    g5.V4_RAW_DIR = V5_DIR / "raw"
    v6_seeds = V6_DIR / "seeds"
    g5.SEED_DIR = v6_seeds if v6_seeds.is_dir() else (V5_DIR / "seeds")

    # 변수 1: comment_heavy 해제 (비율은 최대 1.0 이므로 1.01 이면 절대 걸리지 않는다) + 새 규칙 추가
    g5.CODING_COMMENT_MAX = 1.01
    _v5_post_filter = g5.post_filter

    def post_filter(slot: str, instruction: str, output: str):
        out, reason = _v5_post_filter(slot, instruction, output)
        if reason:
            return out, reason
        if slot == "coding":
            why = coding_reject(out)
            if why:
                return "", why
        return out, reason

    g5.post_filter = post_filter

    # 변수 2: RAG 이스케이프 수정
    _v5_sample_rag = g5.sample_rag

    def sample_rag(n: int, rng):
        rows = _v5_sample_rag(n, rng)
        fixed = 0
        for r in rows:
            for k in ("instruction", "output"):
                if literal_newlines(r.get(k, "")):
                    r[k] = unescape_newlines(r[k])
                    fixed += 1
            r["escape_fixed"] = True
        print(f"[rag] 이스케이프 수정 {fixed}개 필드 ({len(rows)}건 중)")
        return rows

    g5.sample_rag = sample_rag
    print(f"[v6] 파이프라인 준비 — raw={g5.RAW_DIR} seeds={g5.SEED_DIR}")
    return g5


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true", help="새 필터를 v5 생성분에 소급 적용해 거절률만 본다 (LLM 불필요)")
    ap.add_argument("--verify", action="store_true", help="train_data_v6 검증 (이스케이프·필터) (LLM 불필요)")
    ap.add_argument("--import-v5-raw", action="store_true", help="v5 raw 를 v6 raw 로 흡수한 뒤 부족분만 생성")
    ap.add_argument("--assemble", action="store_true", help="생성 없이 raw → train_data_v6 재조립만")
    ap.add_argument("--model", default="qwen3.5:9b")
    ap.add_argument("--slots", default="coding", help="생성할 슬롯 (기본 coding — 잡담·계획은 v5 흡수분을 그대로 쓴다)")
    ap.add_argument("--target", default="", help="예: coding=300")
    ap.add_argument("--variants", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--seed", type=int, default=3407, help="v4=v5=v6 동일 → RAG 400건 같은 샘플")
    args = ap.parse_args()

    if args.audit:
        return audit()
    if args.verify:
        return verify()

    V6_DIR.mkdir(parents=True, exist_ok=True)
    g5 = _load_v5_pipeline()
    argv = ["gen_v6_dataset.py", "--model", args.model, "--slots", args.slots,
            "--variants", str(args.variants), "--limit", str(args.limit), "--seed", str(args.seed)]
    if args.target:
        argv += ["--target", args.target]
    if args.import_v5_raw:
        argv += ["--import-v4-raw"]  # 위에서 V4_RAW_DIR 을 v5 raw 로 갈아끼웠다
    if args.assemble:
        argv += ["--assemble"]
    sys.argv = argv
    rc = g5.main()
    if rc == 0:
        print("\n===== 검증 =====")
        rc = verify()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
