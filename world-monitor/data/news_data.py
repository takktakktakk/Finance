"""ニュース取得モジュール — Google News (日本) RSS から日本語記事を取得。"""

from __future__ import annotations

import sys
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus

import feedparser
import streamlit as st

from config import NEWS_SOURCES, NEWS_PER_TOPIC


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_google_news_jp(query: str, limit: int = 10) -> list[dict]:
    try:
        url = (
            f"https://news.google.com/rss/search?q={quote_plus(query)}"
            f"&hl=ja&gl=JP&ceid=JP:ja"
        )
        feed = feedparser.parse(url)
        items: list[dict] = []
        for entry in feed.entries[:limit]:
            source = "Google ニュース"
            src_obj = getattr(entry, "source", None)
            if src_obj is not None:
                title = getattr(src_obj, "title", None)
                if not title and isinstance(src_obj, dict):
                    title = src_obj.get("title")
                if title:
                    source = title
            items.append(
                {
                    "title": getattr(entry, "title", ""),
                    "link": getattr(entry, "link", ""),
                    "published": getattr(entry, "published", ""),
                    "source": source,
                }
            )
        return items
    except Exception as e:
        print(f"[news_data] fetch_google_news_jp failed for {query}: {e}", file=sys.stderr)
        return []


def _parse_published(value: str):
    if not value:
        return None
    try:
        return parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None


def fetch_news_for_topic(topic_key: str) -> list[dict]:
    src = NEWS_SOURCES.get(topic_key)
    if src is None:
        return []

    query = src.get("google_query") or src.get("jp", "")
    if not query:
        return []

    items = fetch_google_news_jp(query, limit=NEWS_PER_TOPIC * 3)

    seen: set[str] = set()
    deduped: list[dict] = []
    for item in items:
        key = (item.get("title") or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    def sort_key(item: dict):
        dt = _parse_published(item.get("published", ""))
        return dt.timestamp() if dt is not None else 0.0

    deduped.sort(key=sort_key, reverse=True)
    return deduped[:NEWS_PER_TOPIC]
