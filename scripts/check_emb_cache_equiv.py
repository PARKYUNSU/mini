"""캐시 경로 vs 현행 배치 get 경로 동치 확인 (실제 DB, 읽기 전용) — docs/experiments/emb_cache_1015 §3.

논문 5묶음(100편씩, 무작위) × 질의 3개. 논문별 상위 k 의 (거리 소수 10자리, 문서) 가 전부 같아야 통과.
"""
import json, os, random, sys, time
sys.path.insert(0, os.getcwd())
from dotenv import load_dotenv; load_dotenv(".env")
from core.config.agent_config import CHROMA_DB_DIR, COLLECTION_NAME
from core.config.chroma_client import make_chroma_client
from core.rag import agent_chroma_rag as R

col = make_chroma_client(str(CHROMA_DB_DIR)).get_collection(COLLECTION_NAME)
index = json.load(open(R.emb_cache_dir() / "paper_index.json"))
rnd = random.Random(1015)
papers = sorted(index)
groups = [rnd.sample(papers, 100) for _ in range(5)]
QS = ["speculative decoding draft model comparison", "retrieval augmented generation evaluation benchmark",
      "graph neural network for partial differential equations"]
K = 3


def run(flag, pids, q):
    os.environ["RAG_EMB_CACHE"] = flag
    R._emb_cache_state.clear()
    t = time.time(); out = R._nearest_chunks_per_paper_batched(col, pids, q, K); return out, time.time() - t


def key(v):
    return [(round(d, 10), doc) for doc, _, d in v]


bad = 0; tc = []; tb = []
for gi, pids in enumerate(groups):
    for q in QS:
        base, t0 = run("0", pids, q)
        got, t1 = run("1", pids, q)
        tb.append(t0); tc.append(t1)
        diff = [p for p in set(base) | set(got) if key(base.get(p, [])) != key(got.get(p, []))]
        # 거리가 같은 중복 청크끼리 순서만 다른 경우: 거리 목록이 같고 문서 집합이 같으면 동치로 본다
        hard = [p for p in diff if sorted(key(base.get(p, []))) != sorted(key(got.get(p, [])))]
        bad += len(hard)
        print(f"group{gi} q={q[:24]!r} papers={len(base)}/{len(got)} diff={len(diff)} hard={len(hard)} "
              f"t_get={t0:.2f}s t_cache={t1:.2f}s", flush=True)
        for p in hard[:3]:
            print("  ", p, key(base.get(p, []))[:2], key(got.get(p, []))[:2])
print(f"RESULT {'PASS' if bad == 0 else 'FAIL'} hard_diffs={bad} | 중앙 t_get={sorted(tb)[len(tb)//2]:.2f}s t_cache={sorted(tc)[len(tc)//2]:.2f}s")
