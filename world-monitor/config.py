"""World Monitor — configuration constants."""

from __future__ import annotations

INSTRUMENTS = {
    "nikkei":  {"jp": "日経平均",            "en": "Nikkei 225",     "ticker": "^N225",    "kind": "index",     "fmt": ",.2f", "city": "Tokyo",    "lat": 35.6762, "lon": 139.6503},
    "sp500":   {"jp": "S&P 500",             "en": "S&P 500",        "ticker": "^GSPC",    "kind": "index",     "fmt": ",.2f", "city": "New York", "lat": 40.7128, "lon":  -74.0060},
    "gold":    {"jp": "ゴールド",            "en": "Gold Futures",   "ticker": "GC=F",     "kind": "commodity", "fmt": ",.2f", "city": "Chicago",  "lat": 41.8781, "lon":  -87.6298},
    "us10y":   {"jp": "米国債10年利回り",    "en": "US 10Y Yield",   "ticker": "^TNX",     "kind": "yield",     "fmt": ".3f",  "city": "Washington","lat": 38.9072,"lon":  -77.0369},
    "us5y":    {"jp": "米国債5年利回り",     "en": "US 5Y Yield",    "ticker": "^FVX",     "kind": "yield",     "fmt": ".3f",  "city": "Washington","lat": 38.9072,"lon":  -77.0369},
    "usdjpy":  {"jp": "米ドル/円",           "en": "USD/JPY",        "ticker": "USDJPY=X", "kind": "fx",        "fmt": ",.3f", "city": "Tokyo",    "lat": 35.6762, "lon": 139.6503},
    "nifty50": {"jp": "Nifty 50 (印度)",     "en": "Nifty 50 India", "ticker": "^NSEI",    "kind": "index",     "fmt": ",.2f", "city": "Mumbai",   "lat": 19.0760, "lon":  72.8777},
    "acwi":    {"jp": "オールカントリー (ACWI)","en":"MSCI ACWI ETF","ticker": "ACWI",     "kind": "index",     "fmt": ",.2f", "city": "London",   "lat": 51.5074, "lon":   -0.1278},
}

MAP_KEYS = ["nikkei", "sp500", "gold", "us10y", "usdjpy", "nifty50", "acwi"]

TOP_BAR_KEYS = ["nikkei", "sp500", "gold", "us5y", "us10y", "usdjpy"]

CHART_KEYS = ["nikkei", "sp500", "gold", "nifty50", "acwi", "usdjpy"]

PERIODS = {
    "1D": "1d",
    "5D": "5d",
    "1M": "1mo",
    "3M": "3mo",
    "6M": "6mo",
    "1Y": "1y",
    "5Y": "5y",
}

NEWS_SOURCES = {
    "nikkei":     {"jp": "日経平均",      "google_query": "日経平均"},
    "sp500":      {"jp": "S&P 500",       "google_query": "S&P500 株価"},
    "gold":       {"jp": "ゴールド",      "google_query": "金価格 相場"},
    "ustreasury": {"jp": "米国債",        "google_query": "米国債 利回り"},
    "nifty50":    {"jp": "Nifty 50",      "google_query": "インド株 Nifty"},
    "acwi":       {"jp": "オルカン",      "google_query": "オールカントリー 投資信託"},
}

NEWS_PER_TOPIC = 3

CACHE_TTL_MARKET = 300
CACHE_TTL_NEWS = 1800
AUTO_REFRESH_INTERVAL_MS = 5 * 60 * 1000
