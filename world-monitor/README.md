# 🌍 World Monitor

世界の市場・指数・ニュースをリアルタイムに俯瞰する Streamlit ダッシュボード。主要な株価指数・為替・コモディティ・暗号資産の動向と関連ニュースを 1 画面で監視できます。

A Streamlit dashboard for monitoring global markets, indices, and financial news at a glance.

---

## ✨ Features

- 📈 **マルチアセット監視 / Multi-asset tracking** — 株式指数、為替、コモディティ、暗号資産
- 🔄 **自動更新 / Auto refresh** — `streamlit-autorefresh` による定期更新
- 📰 **ニュースフィード / News feed** — RSS による最新マーケットニュース
- 🎨 **ダークテーマ / Dark theme** — 視認性の高い投資向けカラーパレット
- 📊 **インタラクティブチャート / Interactive charts** — Plotly によるズーム・ホバー対応

---

## 📊 Data Sources

| Source            | Coverage                              | Terms                                    |
|-------------------|---------------------------------------|------------------------------------------|
| yfinance          | 株価・指数・為替・暗号資産 / Stocks, FX, Crypto | **Personal use only** (Yahoo! ToS 準拠) |
| RSS feeds         | マーケットニュース / Market news     | 各メディアの利用規約に従う / Per publisher |

> ⚠️ `yfinance` is an unofficial Yahoo! Finance API wrapper. **個人利用に限ります** / personal-use only. Commercial use requires a licensed data provider.

---

## 🚀 Local Run

```bash
cd world-monitor
pip install -r requirements.txt
streamlit run app.py
```

ブラウザで `http://localhost:8501` を開きます。

Open `http://localhost:8501` in your browser.

---

## ☁️ Render Deployment

このリポジトリには `render.yaml` (Blueprint) が同梱されているため、Render に接続するだけで自動デプロイが可能です。

This repo includes a `render.yaml` Blueprint for one-click Render deployment.

### 手順 / Steps

1. [Render Dashboard](https://dashboard.render.com/) にログイン
2. **New → Blueprint** を選択
3. GitHub の `Finace` リポジトリを連結
4. Render が自動的に `render.yaml` を検出 → **Apply** をクリック
5. ビルド完了後、付与された `*.onrender.com` URL でアクセス

### ⏱️ Free Tier の注意 / Free tier caveat

- 15 分間アクセスが無いと **スリープ状態** になります
- 次回アクセス時は起動に **30〜60 秒** 程度かかります
- After 15 min of inactivity the service sleeps; first request takes ~30–60s to wake.

---

## 📁 Project Structure

```
world-monitor/
├── app.py                  # Streamlit エントリポイント
├── config.py               # ティッカー設定・定数
├── requirements.txt        # Python 依存ライブラリ
├── .gitignore
├── .streamlit/
│   └── config.toml         # テーマ・サーバ設定
├── components/             # UI コンポーネント
└── data/                   # データ取得モジュール
```

---

## ⚖️ Legal / Disclaimer

- 🚫 **本ツールは投資助言ではありません** / This tool does **NOT** constitute investment advice.
- 📉 表示される全ての情報は参考目的であり、正確性・完全性を保証しません。
- 🔒 `yfinance` は Yahoo! Finance の非公式ラッパーであり、**個人利用のみ**許可されます。商用利用は Yahoo! のライセンス契約が必要です。
- 投資判断はご自身の責任で行ってください / Trade at your own risk.

---

## 📜 License

MIT License — ただし `yfinance` の利用は Yahoo! Finance ToS に従います。

MIT License, except that `yfinance` usage is bound by Yahoo! Finance Terms of Service.
