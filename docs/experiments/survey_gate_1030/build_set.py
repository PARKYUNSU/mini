"""survey_gate_1030: 기존 세트에서 조사형 게이트(§1)에 새로 걸리는 문항을 모은다 (같은 글 중복은 하나만)."""
import csv, json, os, re, sys
sys.path.insert(0, os.getcwd())
from core.llm.presence_judge import gate_types
from core.llm.presence_judge import _GATE_SURVEY
E = "docs/experiments/"
SETS = [("as", "aspect_split_1022/questions.tsv", "aspect_split_1022/gold.jsonl"),
        ("x2", "external_search_v2_1020/new_questions.tsv", "external_search_v2_1020/new_gold.jsonl"),
        ("ho", "corpus_seed_1020/heldout_questions.tsv", "corpus_seed_1020/heldout_gold.jsonl"),
        ("dc", "corpus_seed_1020/discovery_questions.tsv", "corpus_seed_1020/discovery_gold.jsonl"),
        ("x3", "external_search_v3_1020/new_questions.tsv", "external_search_v3_1020/new_gold.jsonl"),
        ("us", "user_suite_1027/questions.tsv", "user_suite_1027/gold.jsonl"),
        ("qg", "query_glossary_1029/g_questions.tsv", "query_glossary_1029/g_gold.jsonl"),
        ("cs", "corpus_seed_1023/questions.tsv", "corpus_seed_1023/gold.jsonl"),
        ("er", "corpus_er_1029/questions.tsv", "corpus_er_1029/gold.jsonl"),
        ("nd", "nodoc_conclusion_1029/questions.tsv", "nodoc_conclusion_1029/gold.jsonl"),
        ("162", "e2e_ko_1008/ko_questions.tsv", "retrieval_eval_1007/eval_set.jsonl"),
        ("r40", "real_eval_1013/questions.tsv", "real_eval_1013/gold.jsonl"),
        ("r2", "real_eval2_1015/questions.tsv", "real_eval2_1015/gold.jsonl")]
seen, qs, gold = set(), [], []
for tag, qf, gf in SETS:
    g = {j["id"]: j for j in map(json.loads, open(E + gf)) if j.get("id")}
    for r in csv.reader(open(E + qf), delimiter="\t"):
        if len(r) < 2 or r[0] == "id":
            continue
        q = r[-1].strip()
        if q in seen or gate_types(q) or not _GATE_SURVEY.search(q):
            continue
        seen.add(q)
        qs.append((f"{tag}_{r[0]}", q))
        gold.append({"id": f"{tag}_{r[0]}", "stratum": tag, "relevant_papers": g.get(r[0], {}).get("relevant_papers", [])})
d = E + "survey_gate_1030/"
with open(d + "old_questions.tsv", "w") as f:
    f.write("id\tquestion\n" + "".join(f"{i}\t{q}\n" for i, q in qs))
with open(d + "old_gold.jsonl", "w") as f:
    f.write("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in gold))
print(len(qs), "문항 ·", sum(bool(x["relevant_papers"]) for x in gold), "정답 있음")
