# OPERATIONS.md

## 🛠️ TradeSense AI – Operational & Task Runbook

This file contains routine operational procedures, troubleshooting steps, and background job setup for managing TradeSense AI.

---

## ✅ Virtual Environment Setup

### Create venv
```bash
python -m venv venv
```

### Activate venv (Windows)
```bash
venv\Scripts\activate
```

---

## ✅ Install Requirements
```bash
pip install -r requirements.txt
```

---

## 🗃️ PostgreSQL Database

### Create Database via `psql`
```sql
CREATE DATABASE tradesense_ai;
```

### Or Create via pgAdmin
1. Right-click `Databases`
2. Click `Create → Database`
3. Name it `tradesense_ai`
4. Save

---

## 📦 .env File Sample

```dotenv
POSTGRES_URL=postgresql://postgres:yourpass@localhost:5432/tradesense_ai
INFURA_URL=https://mainnet.infura.io/v3/your_project_id
PRIVATE_KEY=your_private_key
WALLET_ADDRESS=0xYourWallet
```

---

## ⚙️ Daily Batch Job (CoinGecko Fetch + Prediction)

### Create `run_tradesense.bat`
```bat
@echo off
cd /d C:\Users\jaypersanchez\projects\tradesense_ai
call venv\Scripts\activate
python app\main.py
```

---

### Schedule with Windows Task Scheduler

1. Open **Task Scheduler**
2. Create Basic Task → Name: `TradeSense AI Daily Run`
3. Trigger: Daily at 7:00 AM
4. Action: Start a Program
5. Program: `cmd.exe`
6. Add Arguments:
   ```cmd
   /c "C:\Users\jaypersanchez\projects\tradesense_ai\run_tradesense.bat"
   ```

---

## 🧪 Testing the Batch Script Manually (in PowerShell)
```powershell
& "C:\Users\jaypersanchez\projects\tradesense_ai\run_tradesense.bat"
```

---

## 🌀 Optional: Spinner/Animation for Long Tasks

In `main.py`, add spinner code to visualize long-running fetches from CoinGecko.

---

## 🔐 Security Notes

- Keep `.env` in `.gitignore`
- Never commit your private key
- Consider using `.env.dev`, `.env.prod` separation for environments

---

## 📈 Logs & Debugging

- Add `loguru` or extend Python's `logging` for file-based logs
- Consider `.log` file output with rotation for long-running jobs

---

## 📌 Future Enhancements

- Add APScheduler for cross-platform job scheduling
- Add GUI status panel (Tkinter/Streamlit)
- Add retry logic for CoinGecko outages

