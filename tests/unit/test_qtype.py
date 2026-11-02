"""core.llm.qtype 질문 유형 분류기 · gate_types 연결 (docs/experiments/qtype_1102)."""
import csv
from pathlib import Path

from core.llm.presence_judge import gate_types
from core.llm.qtype import _TRAIN, predict


def test_flag_off_keeps_regex(monkeypatch):
    monkeypatch.delenv("RAG_QTYPE_CLF", raising=False)
    assert gate_types("RAG 문서 청킹 전략(고정 길이, 의미 단위 등)을 비교한 연구 있어?") == ["cmp"]


def test_flag_on(monkeypatch):
    monkeypatch.setenv("RAG_QTYPE_CLF", "1")
    assert gate_types("LightKV랑 CommVQ 차이가 뭐야?") == ["cmp"]
    assert gate_types("MXNorm이 RMSNorm보다 커널 속도가 최대 몇 배 빨라?") == ["num"]
    assert "list" in gate_types("KV 캐시 압축 관련 논문 5개 찾아서 설명해줘")
    # 실사용 job 116 · 136: 정규식은 비교로 잡거나(판정 건너뜀) 목록을 놓쳤다
    assert gate_types("RAG 문서 청킹 전략(고정 길이, 의미 단위 등)을 비교한 연구 있어?") == []
    assert "list" in gate_types("RAG검색을 했을시에, 두개의 DB에서(각 DB는 엄청난 양의 문서를 가지고 있음) "
                                "서로 비슷하거나 같은 내용을 찾는 연구에 대해서 조사해줘")
    assert predict("RoPE 주파수를 잘라서 컨텍스트 길이를 늘리는 방법 알려줘") == frozenset()


def test_train_has_no_heldout():
    held = Path("docs/experiments/foundation_1031")
    hq = {r[-1].strip() for f in ("heldout.tsv", "heldout_followup.tsv") for r in csv.reader(open(held / f), delimiter="\t") if r}
    train = {line.rstrip("\n").split("\t", 1)[1] for line in _TRAIN.open(encoding="utf-8")}
    assert not (hq & train)
