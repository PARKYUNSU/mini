"""RAG 답변의 arXiv ID 인용을 **그 답변에 쓰인 컨텍스트**와 대조해 고친다.

왜 필요한가 (docs/experiments/protocol.md §5.4): 모델이 ID 를 옮겨 적다가 자릿수를
흘린다. 인용된 ID 중 코퍼스에 없는 것이 20~36% 이고, 전부 실제 ID 의 변형이다
(예: ``2406.18975v1`` → ``2406.1897v1``). 없는 논문을 지어내는 것이 아니라 **전사
오류**다. 사용자가 그 ID 로 논문을 찾으면 없으므로 출처로 쓸 수 없다.

왜 컨텍스트와 대조하나: 그 답변에 어떤 논문이 검색됐는지 우리가 안다. 보통 3~10편
뿐이므로 코퍼스 11,516건과 맞추는 것보다 훨씬 좁고, 한 글자 틀린 ID 의 후보가
사실상 하나로 정해진다.

정책 — 고칠 수 있을 때만 고치고, 애매하면 **지운다**:
  1. 컨텍스트에 그대로 있으면 둔다.
  2. 판(``v2``)만 다르면 컨텍스트의 판으로 맞춘다.
  3. 숫자부가 **한 글자 차이**인 후보가 **정확히 하나**면 그것으로 고친다.
  4. 그 외에는 대괄호째 **지운다.** 틀린 출처를 남기는 것보다 출처가 없는 편이 낫다.

순수 함수다 — LLM·네트워크·파일을 건드리지 않으므로 단위 테스트로 전부 덮인다.
"""

from __future__ import annotations

import re

__all__ = ["extract_context_ids", "fix_citations"]

# arXiv 신형 ID: 4자리.4~5자리(+판). 구형(hep-th/9901001)은 코퍼스에 없어 다루지 않는다.
# 컨텍스트에서 **참조 집합**을 뽑을 때는 엄격하게 본다 — 여기에 쓰레기가 섞이면 교정 기준이 망가진다.
_ID = r"\d{4}\.\d{4,5}(?:v\d+)?"
# 답변에서 인용을 **탐지**할 때는 느슨하게 본다. 자릿수가 하나 더 들어간 변형
# (`2408.080617v2`, 6자리)도 틀린 인용이므로 잡아서 교정 대상에 넣어야 한다.
# 비대칭이 의도다: 느슨하게 찾아 **엄격한 집합 쪽으로만** 고친다.
_ID_LOOSE = r"\d{4}\.\d{3,6}(?:v\d+)?"
_ID_IN_BRACKET = re.compile(rf"\[\s*({_ID_LOOSE})\s*\]")
_BARE = re.compile(r"v\d+$")


def _bare(pid: str) -> str:
    """판 suffix 를 뗀 숫자부."""
    return _BARE.sub("", pid.strip())


def extract_context_ids(context: str) -> list[str]:
    """컨텍스트에 실제로 들어 있는 ID 를 등장 순서대로, 중복 없이 돌려준다.

    운영 컨텍스트는 ``[2408.08067v2] 제목`` 형태이고 다른 빌더는
    ``paper_id=2408.08067v2`` 형태를 쓴다 — 둘 다 잡는다.
    """
    out: list[str] = []
    seen: set[str] = set()
    for m in re.finditer(rf"(?:\[\s*|paper_id=\s*)({_ID})", context):
        pid = m.group(1)
        if pid not in seen:
            seen.add(pid)
            out.append(pid)
    return out


def _edit_distance_le1(a: str, b: str) -> bool:
    """편집 거리가 1 이하인가 (삽입·삭제·치환 각 1회)."""
    if a == b:
        return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:  # 치환 1회
        return sum(1 for x, y in zip(a, b) if x != y) == 1
    # 길이 차 1 → 긴 쪽에서 한 글자를 빼면 같아지는가
    long_s, short_s = (a, b) if la > lb else (b, a)
    for i in range(len(long_s)):
        if long_s[:i] + long_s[i + 1 :] == short_s:
            return True
    return False


def fix_citations(answer: str, context: str) -> tuple[str, dict]:
    """``(고친 답변, 통계)``. 통계 키: kept · fixed · dropped · unknown_ids."""
    valid = extract_context_ids(context)
    by_bare: dict[str, list[str]] = {}
    for pid in valid:
        by_bare.setdefault(_bare(pid), []).append(pid)
    exact = set(valid)

    stats = {"kept": 0, "fixed": 0, "dropped": 0, "unknown_ids": []}

    # 컨텍스트에서 ID 를 하나도 못 찾았으면 **판단 근거가 없다** — 손대지 않는다.
    # (참고 문서가 없는 질의, 컨텍스트 형식 변경, 검색 실패 등. 이 가드가 없으면
    #  그런 경우에 답변의 인용을 전부 지워 버린다.)
    if not valid:
        stats["skipped_no_context_ids"] = True
        return answer, stats

    def repl(m: re.Match[str]) -> str:
        cited = m.group(1)
        if cited in exact:
            stats["kept"] += 1
            return m.group(0)
        # 2) 판만 다르다
        same = by_bare.get(_bare(cited))
        if same:
            stats["fixed"] += 1
            return f"[{same[0]}]"
        # 3) 숫자부가 한 글자 차이인 후보가 정확히 하나
        cands = [p for b, ps in by_bare.items() if _edit_distance_le1(_bare(cited), b) for p in ps]
        uniq = sorted({_bare(p): p for p in cands}.values())
        if len(uniq) == 1:
            stats["fixed"] += 1
            return f"[{uniq[0]}]"
        # 4) 못 고친다 — 지운다
        stats["dropped"] += 1
        stats["unknown_ids"].append(cited)
        return ""

    fixed = _ID_IN_BRACKET.sub(repl, answer)
    if stats["dropped"]:
        # 지운 자리에 남는 공백·구두점 정리: "…합니다  ." → "…합니다."
        fixed = re.sub(r"[ \t]{2,}", " ", fixed)
        fixed = re.sub(r"[ \t]+([.,;:)])", r"\1", fixed)
        fixed = re.sub(r"[ \t]+$", "", fixed, flags=re.M)
    return fixed, stats
