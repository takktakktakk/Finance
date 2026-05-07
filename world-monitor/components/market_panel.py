"""上部メトリックパネル — 6つの指標カードを横並びに表示する。"""
from __future__ import annotations

import streamlit as st

from config import INSTRUMENTS, TOP_BAR_KEYS
from data.market_data import fetch_all_quotes


def render_market_panel() -> None:
    tickers = [INSTRUMENTS[k]["ticker"] for k in TOP_BAR_KEYS]
    quotes = fetch_all_quotes(tickers)

    cols = st.columns(len(TOP_BAR_KEYS))
    for col, key in zip(cols, TOP_BAR_KEYS):
        meta = INSTRUMENTS[key]
        q = quotes.get(meta["ticker"])
        with col:
            label = f"{meta['jp']}\n*{meta['en']}*"
            if q is None:
                st.metric(label=label, value="—", delta=None)
                st.caption("取得失敗 / fetch failed")
            else:
                price_str = f"{q['price']:{meta['fmt']}}"
                if meta['kind'] == 'yield':
                    price_str += "%"
                delta_str = f"{q['change']:+{meta['fmt']}} ({q['change_pct']:+.2f}%)"
                st.metric(label=label, value=price_str, delta=delta_str)
