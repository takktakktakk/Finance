"""🌍 World Monitor — 投資情勢ダッシュボード."""
from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from config import AUTO_REFRESH_INTERVAL_MS
from components.market_panel import render_market_panel
from components.chart_panel import render_chart_panel
from components.news_panel import render_news_panel

st.set_page_config(
    page_title="🌍 World Monitor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st_autorefresh(interval=AUTO_REFRESH_INTERVAL_MS, key="auto_refresh")

now_jst = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S JST")

header_l, header_r = st.columns([3, 1])
with header_l:
    st.title("🌍 World Monitor")
    st.caption("投資情勢ダッシュボード / Investment Market Dashboard")
with header_r:
    st.markdown(f"**🔄 Last update**  \n`{now_jst}`")

st.divider()
render_market_panel()
st.divider()
render_chart_panel()
st.divider()
render_news_panel()

st.divider()
st.caption(
    "Data: Yahoo Finance via yfinance (personal use only) · "
    "News: Yahoo Finance RSS / Google News RSS · "
    "Auto-refresh: 5 min"
)
