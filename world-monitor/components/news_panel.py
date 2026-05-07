"""関連ニュース — トピック別タブ表示。"""
from __future__ import annotations

import streamlit as st

from config import NEWS_SOURCES
from data.news_data import fetch_news_for_topic


def render_news_panel() -> None:
    st.subheader("📰 関連ニュース / Related News")
    topic_keys = list(NEWS_SOURCES.keys())
    tabs = st.tabs([NEWS_SOURCES[k]["jp"] for k in topic_keys])
    for tab, key in zip(tabs, topic_keys):
        with tab:
            items = fetch_news_for_topic(key)
            if not items:
                st.info("ニュースを取得できませんでした / No news available")
                continue
            for item in items:
                title = item.get("title", "(no title)")
                link = item.get("link", "#")
                source = item.get("source", "")
                published = item.get("published", "")
                st.markdown(
                    f"- [{title}]({link})  \n"
                    f"  <span style='color:#888;font-size:0.85em'>{source} · {published}</span>",
                    unsafe_allow_html=True,
                )
