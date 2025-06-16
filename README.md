# TradeSense AI

**TradeSense AI** is your personal crypto trading research assistant powered by agentic AI, price prediction models, and real-time data. Built for serious traders who want to make trading a sustainable source of income.

---

## 🚀 Project Purpose

- Identify crypto investment opportunities
- Predict entry and exit points using AI models
- Use Kraken, Coins.ph, and CoinGecko data
- Integrate Telegram for alerts and AI queries
- Track and analyze volatility and market trends
- Future-ready: plug in DeFi protocols like Uniswap v4

---

## 🧱 Project Structure

```
tradesense_ai/
├── app/
│   ├── ui/              # Desktop GUI (Tkinter or Streamlit)
│   ├── agents/          # Agentic AI logic
│   ├── models/          # ML models for prediction
│   ├── services/        # CoinGecko, Kraken, DB, Telegram, DeFi
│   ├── utils/           # Config loader, logging, decorators
│   └── main.py          # Entry point
├── telegram_bot/        # Crypto-Buddy Telegram interface
├── data/                # Cached price snapshots, CSVs
├── db/                  # PostgreSQL schema and migrations
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🧠 AI & Agentic Capabilities

- Modular AI agents for trading signals
- Price prediction (initially via Linear Regression)
- Extendable to LSTM, Prophet, or transformer-based models
- Telegram queries like: “When to buy ETH?” or “Is BTC overbought?”

---

## 🗂️ Roadmap

- ✅ Consolidate Crypto-Buddy Telegram logic
- ✅ Desktop scaffold (PostgreSQL, CoinGecko, ML)
- 🔄 Add Kraken integration (live + historical data)
- 🔄 AI Agent with entry/exit strategy rules
- 🔄 GUI (Tkinter or Streamlit)
- 🔄 DeFi module (Uniswap v4, Compound, Aave)
- 🔄 Wallet tracking & order simulation

---

## 📦 Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create `.env` with:
   ```
   POSTGRES_URL=postgresql://user:pass@localhost:5432/tradesense_ai
   ```

3. Run the app:
   ```
   python app/main.py
   ```

---

## 🧾 Credits

Built by a developer dedicated to making crypto trading a full-time profession using AI, data, and automation.

