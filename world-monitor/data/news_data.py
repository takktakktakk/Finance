"""ニュース取得モジュール — Yahoo Finance / Google News の RSS フィードから記事を取得。"""

from __future__ import annotations

import sys
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus

import feedparser
import streamlit as st

from config import NEWS_SOURCES


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_yahoo_news(yahoo_ticker: str, limit: int = 10) -> list[dict]:
    try:
        url = (
            f"https://feeds.finance.yahoo.com/rss/2.0/headline?"
            f"s={quote_plus(yahoo_ticker)}&region=US&lang=en-US"
        )
        feed = feedparser.parse(url)
        items: list[dict] = []
        for entry in feed.entries[:limit]:
            items.append(
                {
                    "title": getattr(entry, "title", ""),
                    "link": getattr(entry, "link", ""),
                    "published": getattr(entry, "published", ""),
                    "source": "Yahoo Finance",
                }
            )
        return items
    except Exception as e:
        print(f"[news_data] fetch_yahoo_news failed for {yahoo_ticker}: {e}", file=sys.stderr)
        return []


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_google_news(query: str, limit: int = 10) -> list[dict]:
    try:
        url = (
            f"https://news.google.com/rss/search?q={quote_plus(query)}"
            f"&hl=en-US&gl=US&ceid=US:en"
        )
        feed = feedparser.parse(url)
        items: list[dict] = []
        for entry in feed.entries[:limit]:
            source = "Google News"
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
        print(f"[news_data] fetch_google_news failed for {query}: {e}", file=sys.stderr)
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

    combined: list[dict] = []
    yahoo_ticker = src.get("yahoo_ticker")
    if yahoo_ticker:
        combined.extend(fetch_yahoo_news(yahoo_ticker))

    google_query = src.get("google_query")
    if google_query:
        combined.extend(fetch_google_news(google_query))

    seen: set[str] = set()
    deduped: list[dict] = []
    for item in combined:
        key = (item.get("title") or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    def sort_key(item: dict):
        dt = _parse_published(item.get("published", ""))
        return dt.timestamp() if dt is not None else 0.0

    deduped.sort(key=sort_key, reverse=True)
    return deduped[:15]
