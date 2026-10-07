"""실행 진입점.

  python -m apps.church_lyrics rename              # 수요일: '2026-00-00 주일' 제목을 날짜로
  python -m apps.church_lyrics lyrics [--date YYYY-MM-DD] [--dry-run]   # 토요일: 가사 게시
  python -m apps.church_lyrics harvest             # '확인 완료' 체크된 가사를 가사 DB에 저장

종료 코드: 0 정상 · 1 주일 페이지/'02 찬양' 제목 없음 · 2 콘티가 아직 비어 있음(스케줄러가 2시간 뒤 재시도)
"""
from __future__ import annotations

import argparse
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import compare, notion, setlist, sources

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KST = timezone(timedelta(hours=9))
DATE_PROPERTY = "실제 주일 날짜"
CHECKED_PROPERTY = "확인일"
SECTION = "02찬양"
MARK = "[자동 가사] "
TODO_TEXT = "확인 완료 (악보와 대조하고, 틀린 곳은 위 가사를 고친 뒤 체크)"


def _env(name):
    return os.environ[name].split("?")[0].strip()


# ── 주일 페이지 ────────────────────────────────────────────────────────────
def sunday_of(page) -> str:
    prop = page["properties"].get(DATE_PROPERTY, {})
    date = prop.get("date") or (prop.get("formula") or {}).get("date")
    if date and date.get("start"):
        return date["start"][:10]
    created = datetime.fromisoformat(page["created_time"].replace("Z", "+00:00"))
    return (created.astimezone(KST) + timedelta(days=4)).strftime("%Y-%m-%d")


def target_sunday(today=None) -> str:
    today = today or datetime.now(KST).date()
    return (today + timedelta(days=(6 - today.weekday()) % 7)).isoformat()


def recent_pages(limit=8):
    return notion.query(
        _env("NOTION_SUNDAY_DB_ID"),
        {"sorts": [{"timestamp": "created_time", "direction": "descending"}]},
        limit=limit,
    )


def rename_job() -> int:
    pages = notion.query(
        _env("NOTION_SUNDAY_DB_ID"),
        {"filter": {"property": "title", "title": {"contains": "-00-00"}}},
    )
    for page in pages:
        title = sunday_of(page) + " 주일"
        notion.call("PATCH", f"/pages/{page['id']}",
                    {"properties": {"title": {"title": notion.text(title)}}})
        print("제목 변경:", title)
    if not pages:
        print("고칠 페이지가 없습니다.")
    return 0


# ── 02 찬양 구역 읽기 ──────────────────────────────────────────────────────
def section_of(blocks):
    """'02 찬양' 제목 다음부터 다음 제목·구분선 전까지의 블록과, 그 마지막 블록 id."""
    start = next(
        (i for i, b in enumerate(blocks)
         if b["type"].startswith("heading_") and SECTION in notion.block_text(b).replace(" ", "")),
        None,
    )
    if start is None:
        return None, None
    section = []
    for block in blocks[start + 1:]:
        if block["type"].startswith("heading_") or block["type"] == "divider":
            break
        section.append(block)
    return section, (section[-1]["id"] if section else blocks[start]["id"])


def to_items(section):
    kinds = {"numbered_list_item": "numbered", "bulleted_list_item": "bulleted"}
    items = []
    for block in section:
        if block["type"] in ("callout", "code", "image", "to_do"):
            continue
        rich = list(notion.rich_of(block))
        if block.get("has_children") and block["type"] in kinds:
            for child in notion.children(block["id"]):  # 곡명 아래에 들여쓴 링크
                rich += [{"plain_text": "\n"}] + list(notion.rich_of(child))
        if rich:
            items.append((kinds.get(block["type"], "other"), notion.plain(rich), notion.links(rich)))
    return items


def auto_callouts(blocks):
    for block in blocks:
        if block["type"] == "callout" and notion.block_text(block).startswith(MARK):
            yield block, notion.block_text(block)[len(MARK):].split(" · ")[0].strip()


# ── 가사 DB ────────────────────────────────────────────────────────────────
def lyrics_index() -> dict[str, str]:
    return {setlist.norm(notion.page_title(p)): p["id"]
            for p in notion.query(_env("NOTION_LYRICS_DB_ID"))}


def lyrics_read(page_id) -> str:
    blocks = notion.children(page_id)
    code = [notion.block_text(b) for b in blocks if b["type"] == "code"]
    return "\n\n".join(code or [notion.block_text(b) for b in blocks]).strip()


def lyrics_save(title, lyrics) -> str:
    body = {
        "parent": {"database_id": _env("NOTION_LYRICS_DB_ID")},
        "properties": {
            "title": {"title": notion.text(title)},
            CHECKED_PROPERTY: {"date": {"start": datetime.now(KST).date().isoformat()}},
        },
        "children": [code_block(lyrics)],
    }
    try:
        return notion.call("POST", "/pages", body)["id"]
    except notion.NotionError:  # '확인일' 속성이 없거나 이름이 다른 경우
        del body["properties"][CHECKED_PROPERTY]
        return notion.call("POST", "/pages", body)["id"]


def harvest(page_id, index, dry_run=False) -> int:
    """작업자가 '확인 완료'에 체크한 가사를 가사 DB에 저장합니다."""
    saved = 0
    for block, title in auto_callouts(notion.children(page_id)):
        if setlist.norm(title) in index:
            continue
        kids = notion.children(block["id"])
        checked = any(k["type"] == "to_do" and k["to_do"]["checked"] for k in kids)
        lyrics = "\n\n".join(notion.block_text(k) for k in kids if k["type"] == "code").strip()
        if checked and lyrics:
            print("가사 DB 저장:", title)
            index[setlist.norm(title)] = "dry-run" if dry_run else lyrics_save(title, lyrics)
            saved += 1
    return saved


# ── 게시할 블록 만들기 ─────────────────────────────────────────────────────
def paragraph(rich):
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich}}


def code_block(lyrics):
    return {"object": "block", "type": "code",
            "code": {"rich_text": notion.text(lyrics), "language": "plain text"}}


def callout(song, icon, color, status, lyrics, notes=(), todo=True):
    kids = [paragraph(rich) for rich in notes] + [code_block(lyrics)]
    if todo:
        kids.append({"object": "block", "type": "to_do",
                     "to_do": {"rich_text": notion.text(TODO_TEXT), "checked": False}})
    return {"object": "block", "type": "callout", "callout": {
        "rich_text": notion.text(f"{MARK}{song.title} · {song.role} — {status}"),
        "icon": {"type": "emoji", "emoji": icon},
        "color": color,
        "children": kids,
    }}


def build(song, index):
    saved = index.get(setlist.norm(song.title))
    if saved and saved != "dry-run":
        return callout(song, "📗", "gray_background", "가사 DB에서 가져옴 (확인된 가사)",
                       lyrics_read(saved), todo=False)
    try:
        found = sources.candidates(song.title, song.url)
    except Exception as e:  # 검색·모델 오류로 한 곡이 실패해도 나머지 곡은 계속
        return callout(song, "❌", "red_background",
                       f"가사를 가져오지 못함 ({type(e).__name__}). 직접 붙여넣고 체크", "")
    if not found:
        return callout(song, "❌", "red_background", "가사를 찾지 못함. 직접 붙여넣고 체크", "")

    result = compare.compare([c.lyrics for c in found])
    notes = [notion.text("출처: ") + [r for i, c in enumerate(found)
                                     for r in notion.text(f"[{i + 1}] ", c.url)]]
    for line, other in result.issues:
        notes.append(notion.text(f"확인할 줄: {line}\n다른 출처: {other or '(해당 줄 없음)'}"))
    if result.status == "differ":
        status = f"확인 필요: {len(result.issues)}줄이 출처마다 다름"
    elif result.status == "single":
        status = "확인 필요: 출처가 1곳뿐"
    elif not song.url:
        status = "확인 필요: 링크 없는 곡이라 같은 제목의 다른 곡일 수 있음"
    else:
        return callout(song, "✅", "green_background",
                       f"출처 {len(found)}곳 일치. 사용 후 체크하면 가사 DB에 저장", result.lyrics, notes)
    return callout(song, "⚠️", "yellow_background", status, result.lyrics, notes)


# ── 토요일 작업 ────────────────────────────────────────────────────────────
def lyrics_job(date=None, dry_run=False) -> int:
    pages = recent_pages()
    index = lyrics_index()
    for page in pages[:4]:  # 지난 주일들에서 체크된 가사를 먼저 반영
        harvest(page["id"], index, dry_run)

    date = date or target_sunday()
    page = next((p for p in pages if sunday_of(p) == date), None)
    if not page:
        print(f"{date} 주일 페이지가 없습니다.")
        return 1
    section, anchor = section_of(notion.children(page["id"]))
    if section is None:
        print("'02 찬양' 제목을 찾지 못했습니다.")
        return 1
    songs = setlist.parse(to_items(section))
    if not songs:
        print(f"{date}: 콘티가 아직 없습니다.")
        return 2

    done = {setlist.norm(title) for _, title in auto_callouts(section)}
    blocks = []
    for song in songs:
        if setlist.norm(song.title) in done:
            continue
        block = build(song, index)
        print(notion.plain([{"plain_text": t["text"]["content"]}
                            for t in block["callout"]["rich_text"]]))
        blocks.append(block)
    if blocks and not dry_run:
        notion.append(page["id"], blocks, after=anchor)
    print(f"{date}: {len(songs)}곡 중 {len(blocks)}곡 {'확인(dry-run)' if dry_run else '게시'}")
    return 0


def harvest_job() -> int:
    index = lyrics_index()
    print("저장:", sum(harvest(p["id"], index) for p in recent_pages()), "곡")
    return 0


def main(argv=None) -> int:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env", override=True)
    parser = argparse.ArgumentParser(prog="apps.church_lyrics")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("rename")
    sub.add_parser("harvest")
    p = sub.add_parser("lyrics")
    p.add_argument("--date", help="YYYY-MM-DD (기본: 다가오는 주일)")
    p.add_argument("--dry-run", action="store_true", help="노션에 쓰지 않고 결과만 출력")
    args = parser.parse_args(argv)
    if args.cmd == "rename":
        return rename_job()
    if args.cmd == "harvest":
        return harvest_job()
    return lyrics_job(args.date, args.dry_run)
