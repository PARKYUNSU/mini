#!/usr/bin/env python3
"""JSONL에서 미스 논문들이 존재하는지 + BM25 토크나이즈 결과 확인."""
import json, os, sys, re
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.config.agent_config import PROJECT_ROOT

TOKEN_RE = re.compile(r"[^0-9A-Za-z]+")

def tokenize(text):
    return [t for t in TOKEN_RE.split((text or "").lower().strip()) if len(t) >= 2]

def normalize_pid(pid):
    s = (pid or "").strip()
    if "v" in s:
        base, suffix = s.rsplit("v", 1)
        if suffix.isdigit() and base.replace(".", "").isdigit():
            return base
    return s

target_pids = [
    "2312.10997", "2407.08223", "2409.10102", "2601.15457",
    "2412.15246", "1706.03762", "2412.16188", "2407.01603",
]

processed_dir = PROJECT_ROOT / "raw_data_queue" / "processed"
main_jsonl = PROJECT_ROOT / "raw_data_queue" / "crawled_papers.jsonl"

jsonl_files = sorted(processed_dir.glob("crawled_papers*.jsonl")) if processed_dir.exists() else []
if main_jsonl.exists():
    jsonl_files.append(main_jsonl)

found = {}
for fpath in jsonl_files:
    with fpath.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            pid = normalize_pid((d.get("paper_id") or "").strip())
            if pid in target_pids and pid not in found:
                found[pid] = d

print(f"JSONL 파일 수: {len(jsonl_files)}")
print()

for pid in target_pids:
    if pid in found:
        d = found[pid]
        title = (d.get("title") or "")[:100]
        abstract = (d.get("abstract") or d.get("summary") or "")
        content = (d.get("content") or d.get("text") or "")
        combined = f"{title} {title} {abstract} {content[:1000]}"
        tokens = tokenize(combined)
        
        # Check key terms
        key_terms_map = {
            "2312.10997": ["retrieval", "augmented", "generation", "survey", "rag"],
            "2407.08223": ["speculative", "rag", "retrieval"],
            "2409.10102": ["trustworthiness", "rag", "hallucination"],
            "2601.15457": ["chunking", "retrieval", "reranking"],
            "2412.15246": ["accelerating", "rag", "retrieval"],
            "1706.03762": ["attention", "transformer"],
            "2412.16188": ["vision", "transformer", "image"],
            "2407.01603": ["llm", "agents", "chemistry"],
        }
        key_terms = key_terms_map.get(pid, [])
        present = [t for t in key_terms if t in tokens]
        missing = [t for t in key_terms if t not in tokens]
        
        print(f"OK {pid}: {title}")
        print(f"   abstract_len={len(abstract)}, content_len={len(content)}, token_count={len(tokens)}")
        print(f"   Key terms present: {present}")
        print(f"   Key terms MISSING: {missing}")
        print(f"   First 20 tokens: {tokens[:20]}")
        print()
    else:
        print(f"MISSING {pid}: NOT FOUND in any JSONL file")
        print()
