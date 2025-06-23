# TradeSenseAI-SETUP.md

## 🧠 Project Vision
**TradeSense AI** aims to provide a fully local, privacy-preserving AI assistant for crypto investors and analysts. It extends the proven `scoutjar-semantic` architecture to cover on-chain assets, market sentiment, and trading workflows while remaining independent of third-party LLM APIs.

---

## 🎯 Core Objectives
1. **Vectorized Knowledge Base** for coins, protocols, news, and technical summaries.
2. **LLM-Powered Q&A & Advisory** via local models (Ollama / LM Studio).
3. **Signal Generation & Alerting** based on vector search + rule engine.
4. **Multi-Chat Interface** (Telegram, WhatsApp, Messenger, Signal).

---

## 🏗️ High-Level Architecture

| Layer                | Tool / Service                               |
|----------------------|----------------------------------------------|
| Embedding Model      | `sentence-transformers` (e.g., MiniLM or `all-mpnet-base`) |
| Vector Store         | PostgreSQL 15 + `pgvector` (768-dim)         |
| LLM Serving          | **Ollama** (`llama3-instruct`, `mistral`, `openchat`) **or** LM Studio local endpoint |
| Backend API          | **FastAPI** served by **Gunicorn**           |
| ETL / Data Ingest    | Python batch jobs + Cron / Airflow           |
| Process Manager      | `pm2` (for API) + Systemd timers (for ETL)   |
| Chat Adapters        | Bot API SDKs (Telegram, WhatsApp Business via Twilio, FB Messenger, Signal-CLI) |
| Notification Engine  | Webhooks → Chat adapters / Email / Push      |

---

## 📂 Repository Layout (Proposed)
```
tradesense-ai/
├── data_ingest/
│   ├── fetch_ohlcv.py          # Daily OHLCV → PostgreSQL
│   ├── fetch_news.py           # Crypto news → PostgreSQL
│   └── asset_profile_loader.py # Coin profiles from CG / CM / Docs
├── embeddings/
│   ├── embed_assets.py         # Vectorize coin/project docs
│   ├── embed_news.py           # Vectorize news headlines & bodies
│   └── embed_technicals.py     # Vectorize OHLCV summaries
├── search/
│   ├── search_assets.py        # Semantic asset lookup
│   └── search_sentiment.py     # Sentiment Q&A
├── llm/
│   └── chat.py                 # Wrapper for Ollama / LM-Studio
├── api/
│   └── app.py                  # FastAPI routes (search, chat, alerts)
├── sql/
│   └── setup_vector_schema.sql # pgvector DDL
├── scripts/
│   └── start-api.sh            # Activate venv & run Gunicorn via pm2
├── requirements.txt
└── README.md
```

---

## 🗄️ Database Schema (pgvector)
```sql
CREATE EXTENSION IF NOT EXISTS vector;

-- COIN / PROJECT EMBEDDINGS
CREATE TABLE IF NOT EXISTS asset_embeddings (
    asset_id TEXT PRIMARY KEY,
    embedding VECTOR(768),
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_asset_embeddings
    ON asset_embeddings USING ivfflat (embedding vector_cosine_ops);

-- NEWS / SENTIMENT
CREATE TABLE IF NOT EXISTS news_embeddings (
    news_id BIGINT PRIMARY KEY,
    embedding VECTOR(768),
    created_at TIMESTAMP DEFAULT NOW()
);

-- OHLCV TECHNICAL SUMMARIES
CREATE TABLE IF NOT EXISTS technical_embeddings (
    summary_id BIGINT PRIMARY KEY,
    embedding VECTOR(768),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔄 Embedding Workflow
1. **ETL** scripts fetch new data → raw tables.
2. **Embedding jobs** (run hourly / daily):
   - Load un-embedded rows.
   - Construct text blob (`title + description + metadata`).
   - Encode via `SentenceTransformer`.
   - Insert into *_embeddings tables.
3. **ANN Indexes** updated automatically.

---

## 🤖 Local LLM Integration
### Option A — Ollama
```bash
ollama pull llama3
ollama serve &
```
*Python wrapper example:*
```python
import requests
resp = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3",
    "prompt": "Explain today’s BTC price action">
})
print(resp.json()["response"])
```

### Option B — LM Studio
- GUI download → expose `http://localhost:1234/v1/chat/completions`.
- Swap base URL in `llm/chat.py`.

---

## 🧠 Chat Command Flow (Telegram Example)
/start
→ Welcome to TradeSense AI! Choose:
   1️⃣ Asset Insight   2️⃣ Market Sentiment   3️⃣ Strategy Advisor

/insight ETH
→ Returns project summary + latest news + technical score.

/sentiment "Layer-2 zk rollups"
→ Aggregates news embeddings for sentiment polarity.

/advice "Scalp trade SOL/USDT"
→ LLM + vector context → strategy outline.

---

## 🚀 Deployment Steps (DEV → PROD)
1. **Provision GCP VM** (8 vCPU, 32 GB RAM, optional RTX GPU via A100/L4) or local server with NVIDIA GPU.
2. **Install PostgreSQL 15 + pgvector**.
3. **Create Python 3.11 virtualenv**.
4. `pip install -r requirements.txt`.
5. `bash scripts/start-api.sh` (runs FastAPI on `:6002`).
6. Set up **pm2** for API and **systemd timers** for ETL jobs.
7. Open firewall `6002` if exposing API (otherwise keep internal).

---

## 📈 Roadmap
| Phase | Milestone | Outcome |
|-------|-----------|---------|
| 0     | Repo Bootstrap + Schema | Local dev env ready |
| 1     | Asset & News Embeddings | Search API returns top-K vectors |
| 2     | Local Chat (Ollama)     | `chat.py` answers crypto Q&A |
| 3     | Trading Alert Engine    | `/alert` pushes signals to chats |
| 4     | Multi-Chat Adapters     | Telegram + WhatsApp bots live |
| 5     | Fine-Tuning Cycle       | Custom instruction-tuned LLM |

---

## 🔐 Security & Privacy Considerations
- **No external API calls** for inference → fully local.
- **Data encryption at rest** via `pgcrypto` or disk-level AES.
- **Chat webhook secrets** stored in `.env` (never commit).
- **Role-based queries** for investor vs. public endpoints.

---

**Maintained by**: `Jayper Sanchez`
