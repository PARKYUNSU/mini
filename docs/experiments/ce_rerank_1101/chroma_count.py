"""ce_rerank_1101: 실행 앞뒤 Chroma 청크 수 — 측정 중 코퍼스가 그대로인지 본다. 쓰기 잠금이면 멈춘다 (README §2)."""
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv(".env")
import core.rag.agent_chroma_rag as acr

if acr.is_chroma_write_locked():
    sys.exit("Chroma 쓰기 잠금 — 측정 중단")
print("Chroma 청크", acr._get_chroma_singleton()._collection.count(), flush=True)
