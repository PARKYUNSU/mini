"""답변 👍/👎 피드백 요약 — 잡별 마지막 평가 기준 (apps/telegram_bot/answer_feedback.py).

    .venv/bin/python scripts/feedback_summary.py            # 집계 + 👎 질문 목록
    .venv/bin/python scripts/feedback_summary.py --all      # 👍 질문도
"""
import argparse, json, os, sys
sys.path.insert(0, os.getcwd())
from apps.telegram_bot.answer_feedback import log_path

ap = argparse.ArgumentParser(); ap.add_argument("--all", action="store_true"); args = ap.parse_args()
p = log_path()
if not p.exists():
    print(f"아직 기록 없음: {p}"); raise SystemExit(0)
last = {}
for line in p.read_text(encoding="utf-8").splitlines():
    if line.strip():
        r = json.loads(line); last[r["job_id"]] = r
rows = sorted(last.values(), key=lambda r: r["ts"])
up = sum(r["rating"] == "up" for r in rows)
print(f"평가한 답변 {len(rows)} · 👍 {up} · 👎 {len(rows) - up}  ({rows[0]['ts']} ~ {rows[-1]['ts']})")
for r in rows:
    if args.all or r["rating"] == "down":
        print(f"{'👍' if r['rating'] == 'up' else '👎'} {r['ts']} #{r['job_id']} {r['question'][:80]!r} 논문={r['answer_papers'][:4]}")
