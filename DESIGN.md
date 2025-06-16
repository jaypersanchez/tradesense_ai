# DESIGN.md

## 📘 TradeSense AI – Technical Architecture Document

**Project Name**: TradeSense AI  
**Goal**: A personal crypto trading research platform powered by AI, real-time data pipelines, and DeFi integrations.  
**Target**: Desktop-first solution for data-driven, automated trading decisions, with Telegram as a companion interface.

---

## 🔧 Architecture Overview

### 📌 Core Components

| Layer       | Component                   | Description |
|-------------|-----------------------------|-------------|
| Data Ingest | `CoinGeckoService`          | Pulls OHLCV data from CoinGecko API |
| Data Store  | `PostgreSQL` via SQLAlchemy | Stores historical OHLCV and AI predictions |
| Modeling    | `PredictionModel`           | Runs simple linear regression (extendable to Prophet/XGBoost) |
| Interface   | `Tkinter` or `Streamlit`    | Local desktop GUI for interaction |
| Agent Layer | `Telegram Bot` (Crypto-Buddy) | Sends AI-generated alerts, responds to user queries |
| Blockchain  | `EthereumService`           | Web3 setup using Infura and wallet keys |
| DeFi        | `CompoundService` & `AaveService` | Stubs to interact with lending protocols |

---

## 🗂️ Folder Structure

```
tradesense_ai/
├── app/
│   ├── services/              # Core services (data, defi, ethereum)
│   │   ├── coingecko_service.py
│   │   ├── db_service.py
│   │   ├── model_service.py
│   │   ├── ethereum_service.py
│   │   ├── compound_service.py
│   │   └── aave_service.py
│   ├── utils/
│   │   └── config.py
│   ├── main.py                # Orchestrates fetch + prediction
├── telegram_bot/              # Will house Telegram integration
├── data/                      # For CSV snapshots or cache
├── db/                        # PostgreSQL migrations (future)
├── .env                       # Environment config
├── requirements.txt
├── README.md
└── DESIGN.md                  # ← This file
```

---

## 🧩 Component Details

### ✅ main.py
- Loads environment config
- Initializes database, fetches OHLCV via CoinGecko
- Runs prediction model
- Saves both raw data and model output

### ✅ db_service.py
- Uses SQLAlchemy engine from `POSTGRES_URL`
- Two main methods:
  - `save_ohlcv(pair, df)`
  - `save_predictions(pair, df)`

### ✅ coingecko_service.py
- Pulls OHLCV for any token from CoinGecko
- Returns a pandas DataFrame with timestamps and price

### ✅ model_service.py
- Uses linear regression on price vs. time for forecasting
- Output: adds a `predicted` column to original DataFrame

---

## 🔗 Blockchain and DeFi Modules

### ✅ ethereum_service.py
- Initializes Web3 provider using Infura URL
- Loads wallet using private key
- Exposes `web3` and `account` objects for use in other services

### ✅ compound_service.py (stub)
- Loads USDC, cUSDC, DAI, cDAI, Comptroller addresses
- Placeholder for:
  - `supply(token, amount)`
  - `borrow(token, amount)`
  - `repay(token, amount)`

### ✅ aave_service.py (stub)
- Loads Aave lending pool contract addresses
- Ready for ABI wiring and lending functionality

---

## 📡 External APIs and Data Sources

| Source     | Purpose              |
|------------|----------------------|
| CoinGecko  | Market OHLCV data    |
| Infura     | Ethereum RPC         |
| PostgreSQL | Local data storage   |

---

## 📈 Future Enhancements

- Add Kraken + Coins.ph integrations
- Add Uniswap v4 support for swaps and liquidity tracking
- Implement more robust AI models (Prophet, LSTM)
- Add Telegram command handler and notification system
- Integrate Streamlit GUI with user inputs
- Extend DB schema with wallet snapshots and trade logs

---

## ✅ Status

**Scaffold Complete**: Yes  
**Ready for Development**: ✅  
**Testing & Expansion**: Ongoing  

---

## 🔐 Security Notes

- Never commit your `.env` file
- Always treat `PRIVATE_KEY` and `INFURA_URL` as sensitive
- Rotate keys if needed and use `.gitignore`

