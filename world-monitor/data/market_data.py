"""市場データ取得モジュール — yfinance を用いた価格・履歴の取得。"""

from __future__ import annotations

import sys
from datetime import datetime

import pandas as pd
import streamlit as st
import yfinance as yf

YIELD_TICKERS = {"^TNX", "^FVX", "^TYX", "^IRX"}


@st.cache_data(ttl=300, show_spinner=False)
def fetch_quote(ticker: str) -> dict | None:
    try:
        t = yf.Ticker(ticker)
        price = None
        prev_close = None

        try:
            fi = t.fast_info
            price = float(fi["last_price"])
            prev_close = float(fi["previous_close"])
        except Exception as e:
            print(f"[market_data] fast_info failed for {ticker}: {e}", file=sys.stderr)

        if price is None or prev_close is None or pd.isna(price) or pd.isna(prev_close):
            hist = t.history(period="2d")
            if hist is None or hist.empty or len(hist) < 2:
                return None
            closes = hist["Close"].dropna()
            if len(closes) < 2:
                return None
            price = float(closes.iloc[-1])
            prev_close = float(closes.iloc[-2])

        # yfinance returns ^TNX/^FVX/^TYX/^IRX yields multiplied by 10 (e.g. 42.20 == 4.220%)
        if ticker in YIELD_TICKERS:
            price = price / 10.0
            prev_close = prev_close / 10.0

        change = price - prev_close
        change_pct = (change / prev_close * 100.0) if prev_close else 0.0

        return {
            "price": price,
            "prev_close": prev_close,
            "change": change,
            "change_pct": change_pct,
            "ts": datetime.now(),
        }
    except Exception as e:
        print(f"[market_data] fetch_quote failed for {ticker}: {e}", file=sys.stderr)
        return None


@st.cache_data(ttl=300, show_spinner=False)
def fetch_history(
    ticker: str, period: str = "6mo", interval: str = "1d"
) -> pd.DataFrame | None:
    try:
        if period == "1d":
            interval = "5m"
        elif period == "5d":
            interval = "15m"
        else:
            interval = "1d"

        df = yf.Ticker(ticker).history(period=period, interval=interval)
        if df is None or df.empty:
            return None

        # yfinance returns ^TNX/^FVX/^TYX/^IRX yields multiplied by 10
        if ticker in YIELD_TICKERS:
            for col in ("Open", "High", "Low", "Close"):
                if col in df.columns:
                    df[col] = df[col] / 10.0

        return df
    except Exception as e:
        print(f"[market_data] fetch_history failed for {ticker}: {e}", file=sys.stderr)
        return None


def fetch_all_quotes(tickers: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for tk in tickers:
        q = fetch_quote(tk)
        if q is not None:
            out[tk] = q
    return out
