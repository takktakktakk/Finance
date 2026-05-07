"""右側ティッカー — 縦並び価格パネル (worldmonitor スタイル)。"""
from __future__ import annotations

import streamlit as st

from config import INSTRUMENTS, TOP_BAR_KEYS
from data.market_data import fetch_all_quotes


def _row_html(meta: dict, q: dict | None) -> str:
    if q is None:
        return (
            f"<div style='padding:8px 10px;border-bottom:1px solid #2A2F3E;'>"
            f"<div style='font-size:13px;color:#FAFAFA;font-weight:600'>{meta['jp']}</div>"
            f"<div style='font-size:11px;color:#888'>{meta['en']} · {meta['ticker']}</div>"
            f"<div style='font-size:14px;color:#888;margin-top:4px'>— no data</div>"
            f"</div>"
        )

    price_str = f"{q['price']:{meta['fmt']}}"
    if meta["kind"] == "yield":
        price_str += "%"

    pct = q["change_pct"]
    is_up = pct >= 0
    color = "#00E676" if is_up else "#FF5252"
    arrow = "▲" if is_up else "▼"
    delta_str = f"{q['change']:+{meta['fmt']}}  ({pct:+.2f}%)"

    return (
        f"<div style='padding:8px 10px;border-bottom:1px solid #2A2F3E;'>"
        f"<div style='display:flex;justify-content:space-between;align-items:baseline'>"
        f"<span style='font-size:13px;color:#FAFAFA;font-weight:600'>{meta['jp']}</span>"
        f"<span style='font-size:11px;color:#888'>{meta['ticker']}</span>"
        f"</div>"
        f"<div style='font-size:11px;color:#888;margin-top:1px'>{meta['en']}</div>"
        f"<div style='display:flex;justify-content:space-between;align-items:baseline;margin-top:6px'>"
        f"<span style='font-size:18px;color:#FAFAFA;font-weight:700'>{price_str}</span>"
        f"<span style='font-size:12px;color:{color};font-weight:600'>{arrow} {delta_str}</span>"
        f"</div>"
        f"</div>"
    )


def render_market_panel() -> None:
    """旧API互換 — 横並び 6 カードで描画する。"""
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
                if meta["kind"] == "yield":
                    price_str += "%"
                delta_str = f"{q['change']:+{meta['fmt']}} ({q['change_pct']:+.2f}%)"
                st.metric(label=label, value=price_str, delta=delta_str)


def render_ticker_panel() -> None:
    """worldmonitor 右パネル風 — 縦並びリアルタイムティッカー。"""
    st.markdown(
        "<div style='font-size:14px;color:#FF6B35;font-weight:700;"
        "padding:6px 10px;border-bottom:1px solid #FF6B35;letter-spacing:1px'>"
        "⚡ リアルタイム / LIVE</div>",
        unsafe_allow_html=True,
    )

    tickers = [INSTRUMENTS[k]["ticker"] for k in TOP_BAR_KEYS]
    quotes = fetch_all_quotes(tickers)

    rows = []
    for key in TOP_BAR_KEYS:
        meta = INSTRUMENTS[key]
        q = quotes.get(meta["ticker"])
        rows.append(_row_html(meta, q))

    st.markdown(
        "<div style='background:#1A1F2E;border:1px solid #2A2F3E;border-radius:6px;"
        "overflow:hidden'>" + "".join(rows) + "</div>",
        unsafe_allow_html=True,
    )

    st.caption("出典: Yahoo Finance · 5分ごと更新")
