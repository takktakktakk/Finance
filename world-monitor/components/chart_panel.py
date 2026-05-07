"""メインチャート — 期間切替＋ローソク足/ライン。"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from config import INSTRUMENTS, CHART_KEYS, PERIODS
from data.market_data import fetch_history


def _interval_for_period(period: str) -> str:
    if period == "1d":
        return "5m"
    if period == "5d":
        return "15m"
    return "1d"


def render_chart_panel() -> None:
    st.subheader("📈 メインチャート / Main Chart")
    tabs = st.tabs([INSTRUMENTS[k]["jp"] for k in CHART_KEYS])
    for tab, key in zip(tabs, CHART_KEYS):
        with tab:
            meta = INSTRUMENTS[key]
            period_label = st.radio(
                "期間 / Period",
                list(PERIODS.keys()),
                index=4,  # default 6M
                horizontal=True,
                key=f"period_{key}",
            )
            period = PERIODS[period_label]
            interval = _interval_for_period(period)
            df = fetch_history(meta["ticker"], period=period, interval=interval)
            if df is None or df.empty:
                st.warning(f"{meta['jp']} のデータを取得できませんでした / Data unavailable")
                continue

            fig = go.Figure()
            if interval == "1d":
                fig.add_trace(go.Candlestick(
                    x=df.index,
                    open=df["Open"], high=df["High"],
                    low=df["Low"], close=df["Close"],
                    name=meta["en"],
                ))
                if len(df) >= 25:
                    fig.add_trace(go.Scatter(
                        x=df.index, y=df["Close"].rolling(25).mean(),
                        mode="lines", name="MA25", line=dict(width=1),
                    ))
            else:
                fig.add_trace(go.Scatter(
                    x=df.index, y=df["Close"],
                    mode="lines", name=meta["en"],
                ))
            fig.update_layout(
                height=480,
                margin=dict(l=10, r=10, t=30, b=10),
                xaxis_rangeslider_visible=False,
                template="plotly_dark",
            )
            st.plotly_chart(fig, use_container_width=True)
