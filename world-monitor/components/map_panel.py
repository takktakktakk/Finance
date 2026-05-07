"""世界地図パネル — 主要金融センターをマーカー表示する。"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from config import INSTRUMENTS, MAP_KEYS
from data.market_data import fetch_all_quotes


HIGHLIGHTED_COUNTRIES = ["JPN", "USA", "GBR", "IND"]

COUNTRY_LABELS = [
    {"name": "日本",       "lat": 36.20, "lon": 138.25},
    {"name": "米国",       "lat": 39.83, "lon":  -98.58},
    {"name": "英国",       "lat": 54.50, "lon":   -2.50},
    {"name": "インド",     "lat": 20.59, "lon":   78.96},
    {"name": "中国",       "lat": 35.86, "lon":  104.20},
    {"name": "ドイツ",     "lat": 51.16, "lon":   10.45},
    {"name": "オーストラリア","lat": -25.27,"lon": 133.78},
    {"name": "ブラジル",   "lat": -14.24, "lon": -51.93},
    {"name": "ロシア",     "lat": 61.52, "lon":  105.32},
    {"name": "カナダ",     "lat": 56.13, "lon": -106.35},
    {"name": "メキシコ",   "lat": 23.63, "lon": -102.55},
    {"name": "サウジ",     "lat": 23.89, "lon":   45.08},
    {"name": "南アフリカ", "lat": -30.56, "lon":  22.94},
]


def _color_for(change_pct: float | None) -> str:
    if change_pct is None:
        return "#888888"
    if change_pct > 0.5:
        return "#00E676"
    if change_pct > 0:
        return "#66BB6A"
    if change_pct > -0.5:
        return "#EF5350"
    return "#FF1744"


def _size_for(change_pct: float | None) -> float:
    if change_pct is None:
        return 12.0
    return min(40.0, max(14.0, 14.0 + abs(change_pct) * 6.0))


def render_map_panel() -> None:
    tickers = list({INSTRUMENTS[k]["ticker"] for k in MAP_KEYS})
    quotes = fetch_all_quotes(tickers)

    fig = go.Figure()

    fig.add_trace(
        go.Choropleth(
            locations=HIGHLIGHTED_COUNTRIES,
            z=[1] * len(HIGHLIGHTED_COUNTRIES),
            colorscale=[[0, "#3A2218"], [1, "#FF6B35"]],
            zmin=0,
            zmax=1,
            showscale=False,
            marker_line_color="#FF6B35",
            marker_line_width=0.6,
            hoverinfo="location",
            name="",
        )
    )

    fig.add_trace(
        go.Scattergeo(
            lat=[c["lat"] for c in COUNTRY_LABELS],
            lon=[c["lon"] for c in COUNTRY_LABELS],
            mode="text",
            text=[c["name"] for c in COUNTRY_LABELS],
            textfont=dict(color="#999", size=10, family="sans-serif"),
            textposition="middle center",
            hoverinfo="skip",
            showlegend=False,
        )
    )

    lats, lons, sizes, colors, hovers, texts = [], [], [], [], [], []
    for k in MAP_KEYS:
        meta = INSTRUMENTS[k]
        q = quotes.get(meta["ticker"])
        change_pct = q["change_pct"] if q else None
        price = q["price"] if q else None

        lats.append(meta["lat"])
        lons.append(meta["lon"])
        sizes.append(_size_for(change_pct))
        colors.append(_color_for(change_pct))

        if q is None:
            hover = f"<b>{meta['jp']}</b><br>{meta['city']}<br>取得失敗 / no data"
        else:
            arrow = "▲" if change_pct >= 0 else "▼"
            price_str = f"{price:{meta['fmt']}}"
            if meta["kind"] == "yield":
                price_str += "%"
            hover = (
                f"<b>{meta['jp']} / {meta['en']}</b><br>"
                f"📍 {meta['city']}<br>"
                f"💹 {price_str}<br>"
                f"{arrow} {change_pct:+.2f}%"
            )
        hovers.append(hover)
        texts.append(meta["jp"])

    fig.add_trace(
        go.Scattergeo(
            lat=lats,
            lon=lons,
            mode="markers+text",
            marker=dict(
                size=sizes,
                color=colors,
                line=dict(width=1.5, color="#FAFAFA"),
                opacity=0.92,
            ),
            text=texts,
            textposition="top center",
            textfont=dict(color="#FAFAFA", size=11, family="sans-serif"),
            hovertext=hovers,
            hoverinfo="text",
            showlegend=False,
        )
    )

    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="#1A1F2E",
        showocean=True,
        oceancolor="#0E1117",
        showcountries=True,
        countrycolor="#3A3F4E",
        showcoastlines=True,
        coastlinecolor="#3A3F4E",
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        height=560,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.caption(
        "🟧 アクティブ地域 (日米英印) ・ 🟢 上昇 / Up ・ 🔴 下落 / Down ・ ⚪ データなし    "
        "マーカー サイズ = 変化率 / Size = magnitude"
    )
