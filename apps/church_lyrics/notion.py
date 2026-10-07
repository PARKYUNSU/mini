"""노션 API 최소 래퍼. 표준 라이브러리만 사용합니다."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

API = "https://api.notion.com/v1"
VERSION = "2022-06-28"
CHUNK = 1900  # 노션 텍스트 조각 하나의 한도(2000자)보다 조금 작게


class NotionError(RuntimeError):
    pass


def call(method, path, body=None, retries=4):
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(retries):
        req = urllib.request.Request(
            API + path,
            method=method,
            data=data,
            headers={
                "Authorization": "Bearer " + os.environ["NOTION_TOKEN"],
                "Notion-Version": VERSION,
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                return json.load(res)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise NotionError(f"{method} {path} -> {e.code}: {detail}") from None


def plain(rich):
    return "".join(r.get("plain_text", "") for r in rich or [])


def links(rich):
    return [r["href"] for r in rich or [] if r.get("href")]


def text(content, url=None):
    """문자열을 노션 rich_text 배열로 바꿉니다(긴 글은 여러 조각으로)."""
    out = []
    for i in range(0, len(content), CHUNK):
        t = {"content": content[i:i + CHUNK]}
        if url:
            t["link"] = {"url": url}
        out.append({"type": "text", "text": t})
    return out


def rich_of(block):
    return (block.get(block["type"]) or {}).get("rich_text") or []


def block_text(block):
    return plain(rich_of(block))


def children(block_id):
    out, cursor = [], None
    while True:
        q = "?page_size=100" + (f"&start_cursor={cursor}" if cursor else "")
        res = call("GET", f"/blocks/{block_id}/children{q}")
        out += res["results"]
        if not res.get("has_more"):
            return out
        cursor = res["next_cursor"]


def query(db_id, body=None, limit=None):
    out, cursor = [], None
    while True:
        payload = dict(body or {})
        payload["page_size"] = min(100, limit - len(out)) if limit else 100
        if cursor:
            payload["start_cursor"] = cursor
        res = call("POST", f"/databases/{db_id}/query", payload)
        out += res["results"]
        if not res.get("has_more") or (limit and len(out) >= limit):
            return out
        cursor = res["next_cursor"]


def append(parent_id, blocks, after=None):
    """blocks를 parent 아래(after 블록 바로 뒤)에 순서대로 추가합니다."""
    for i in range(0, len(blocks), 100):
        body = {"children": blocks[i:i + 100]}
        if after:
            body["after"] = after
        res = call("PATCH", f"/blocks/{parent_id}/children", body)
        if after and res.get("results"):
            after = res["results"][-1]["id"]


def page_title(page):
    for prop in page["properties"].values():
        if prop["type"] == "title":
            return plain(prop["title"])
    return ""
