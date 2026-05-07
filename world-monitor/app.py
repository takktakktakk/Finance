"""🌍 World Monitor — 投資情勢ダッシュボード."""
from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from config import AUTO_REFRESH_INTERVAL_MS
from components.map_panel import render_map_panel
from components.market_panel import render_ticker_panel
from components.global_situation_panel import render_global_situation_panel
from components.chart_panel import render_chart_panel
from components.news_panel import render_news_panel

st.set_page_config(
    page_title="🌍 World Monitor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    div[data-testid="stPlotlyChart"] {background: transparent;}
    h1, h2, h3 {letter-spacing: 0.5px;}
    </style>
    """,
    unsafe_allow_html=True,
)

st_autorefresh(interval=AUTO_REFRESH_INTERVAL_MS, key="auto_refresh")

now_jst = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S JST")

header_l, header_r = st.columns([3, 1])
with header_l:
    st.markdown(
        "<h1 style='margin-bottom:0'>🌍 World Monitor</h1>"
        "<div style='color:#FF6B35;font-size:13px;letter-spacing:2px;font-weight:600'>"
        "MONITOR · v1.0 · 投資情勢ダッシュボード"
        "</div>",
        unsafe_allow_html=True,
    )
with header_r:
    st.markdown(
        f"<div style='text-align:right;color:#888;font-size:12px'>🔄 Last update</div>"
        f"<div style='text-align:right;color:#FAFAFA;font-family:monospace;font-size:13px'>{now_jst}</div>"
        f"<div style='text-align:right;color:#00E676;font-size:11px;margin-top:2px'>● LIVE</div>",
        unsafe_allow_html=True,
    )

st.divider()

global_col, map_col, ticker_col = st.columns([1, 3, 1], gap="small")
with global_col:
    render_global_situation_panel()
with map_col:
    st.markdown(
        "<div style='font-size:13px;color:#888;letter-spacing:1px;margin-bottom:4px'>"
        "🗺️  GLOBAL FINANCIAL CENTERS / 主要金融センター</div>",
        unsafe_allow_html=True,
    )
    render_map_panel()
with ticker_col:
    render_ticker_panel()

st.divider()

with st.expander("📈 メインチャート / Main Chart", expanded=False):
    render_chart_panel()

st.divider()
render_news_panel()

st.divider()
st.caption(
    "Data: Yahoo Finance via yfinance (personal use only) · "
    "News: Yahoo Finance RSS / Google News RSS · "
    "Auto-refresh: 5 min · "
    "Inspired by worldmonitor.app"
)
