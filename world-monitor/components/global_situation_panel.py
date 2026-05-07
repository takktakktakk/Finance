"""左サイドパネル — 市場ステータス & 地域別パフォーマンス。"""
from __future__ import annotations

from datetime import datetime, time
from zoneinfo import ZoneInfo

import streamlit as st

from config import INSTRUMENTS
from data.market_data import fetch_all_quotes


MARKETS = [
    {"jp": "東京",        "en": "Tokyo (TSE)",   "tz": "Asia/Tokyo",     "open": time(9, 0),  "close": time(15, 0), "flag": "🇯🇵"},
    {"jp": "ムンバイ",    "en": "Mumbai (NSE)",  "tz": "Asia/Kolkata",   "open": time(9, 15), "close": time(15, 30), "flag": "🇮🇳"},
    {"jp": "ロンドン",    "en": "London (LSE)",  "tz": "Europe/London",  "open": time(8, 0),  "close": time(16, 30), "flag": "🇬🇧"},
    {"jp": "ニューヨーク","en": "New York (NYSE)","tz": "America/New_York","open": time(9, 30), "close": time(16, 0),  "flag": "🇺🇸"},
]


def _market_status(m: dict) -> tuple[str, str, str]:
    now_local = datetime.now(ZoneInfo(m["tz"]))
    weekday = now_local.weekday()
    is_weekend = weekday >= 5
    t = now_local.time()
    if is_weekend:
        return ("休場", "#888888", now_local.strftime("%H:%M"))
    if m["open"] <= t <= m["close"]:
        return ("OPEN", "#00E676", now_local.strftime("%H:%M"))
    return ("CLOSED", "#FF5252", now_local.strftime("%H:%M"))


REGIONS = [
    {"jp": "アジア",     "en": "Asia",     "instruments": ["nikkei", "nifty50"]},
    {"jp": "アメリカ",   "en": "Americas", "instruments": ["sp500", "gold"]},
    {"jp": "グローバル", "en": "Global",   "instruments": ["acwi"]},
    {"jp": "為替・債券", "en": "FX/Bonds", "instruments": ["usdjpy", "us10y"]},
]


def render_global_situation_panel() -> None:
    st.markdown(
        "<div style='font-size:14px;color:#FF6B35;font-weight:700;"
        "padding:6px 10px;border-bottom:1px solid #FF6B35;letter-spacing:1px'>"
        "🌐 グローバル情勢 / GLOBAL</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='font-size:11px;color:#888;letter-spacing:1px;"
        "margin:10px 0 4px 0'>📍 市場ステータス / Market Status</div>",
        unsafe_allow_html=True,
    )

    rows = []
    for m in MARKETS:
        status, color, local_time = _market_status(m)
        rows.append(
            f"<div style='display:flex;justify-content:space-between;align-items:center;"
            f"padding:6px 10px;border-bottom:1px solid #2A2F3E;font-size:12px'>"
            f"<span style='color:#FAFAFA'>{m['flag']} {m['jp']}</span>"
            f"<span><span style='color:{color};font-weight:600'>● {status}</span> "
            f"<span style='color:#888;font-family:monospace;margin-left:4px'>{local_time}</span></span>"
            f"</div>"
        )
    st.markdown(
        "<div style='background:#1A1F2E;border:1px solid #2A2F3E;"
        "border-radius:6px;overflow:hidden'>" + "".join(rows) + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='font-size:11px;color:#888;letter-spacing:1px;"
        "margin:14px 0 4px 0'>📊 地域別パフォーマンス / Regional</div>",
        unsafe_allow_html=True,
    )

    tickers = [INSTRUMENTS[k]["ticker"] for k in INSTRUMENTS]
    quotes = fetch_all_quotes(tickers)

    region_rows = []
    for r in REGIONS:
        pcts = []
        for inst_key in r["instruments"]:
            meta = INSTRUMENTS.get(inst_key)
            if not meta:
                continue
            q = quotes.get(meta["ticker"])
            if q is not None:
                pcts.append(q["change_pct"])
        if pcts:
            avg = sum(pcts) / len(pcts)
            color = "#00E676" if avg >= 0 else "#FF5252"
            arrow = "▲" if avg >= 0 else "▼"
            value = f"{arrow} {avg:+.2f}%"
        else:
            color = "#888"
            value = "—"

        region_rows.append(
            f"<div style='display:flex;justify-content:space-between;align-items:center;"
            f"padding:6px 10px;border-bottom:1px solid #2A2F3E;font-size:12px'>"
            f"<span style='color:#FAFAFA'>{r['jp']}</span>"
            f"<span style='color:{color};font-weight:600'>{value}</span>"
            f"</div>"
        )

    st.markdown(
        "<div style='background:#1A1F2E;border:1px solid #2A2F3E;"
        "border-radius:6px;overflow:hidden'>" + "".join(region_rows) + "</div>",
        unsafe_allow_html=True,
    )

    movers = []
    for key, meta in INSTRUMENTS.items():
        q = quotes.get(meta["ticker"])
        if q is not None:
            movers.append((key, meta, q["change_pct"]))
    movers.sort(key=lambda x: abs(x[2]), reverse=True)
    movers = movers[:3]

    if movers:
        st.markdown(
            "<div style='font-size:11px;color:#888;letter-spacing:1px;"
            "margin:14px 0 4px 0'>🔥 本日のハイライト / Top Movers</div>",
            unsafe_allow_html=True,
        )
        mover_rows = []
        for key, meta, pct in movers:
            color = "#00E676" if pct >= 0 else "#FF5252"
            arrow = "▲" if pct >= 0 else "▼"
            mover_rows.append(
                f"<div style='display:flex;justify-content:space-between;align-items:center;"
                f"padding:6px 10px;border-bottom:1px solid #2A2F3E;font-size:12px'>"
                f"<span style='color:#FAFAFA'>{meta['jp']}</span>"
                f"<span style='color:{color};font-weight:600'>{arrow} {pct:+.2f}%</span>"
                f"</div>"
            )
        st.markdown(
            "<div style='background:#1A1F2E;border:1px solid #2A2F3E;"
            "border-radius:6px;overflow:hidden'>" + "".join(mover_rows) + "</div>",
            unsafe_allow_html=True,
        )
