# TradeSense AI TODO

This file contains upcoming tasks and feature improvements planned for the TradeSense AI project.

---

## 📌 Features to Implement

- [ ] Replace hardcoded coin list with a database-driven configuration table.
- [ ] Schedule a daily batch job to refresh OHLCV data and predictions.
- [ ] Add animated loading indicator to `main.py` for better feedback.
- [ ] Implement a REST API backend for future web integration.
- [ ] Integrate wallet connection via Infura for Ethereum interactions.
- [ ] Build out stubs for `compound_service.py` and `aave_service.py`.
- [ ] Create modular PyQt views for additional visualizations (e.g., volatility, news sentiment).
- [ ] Add a config management module for environment variables with validation.

---

## Short-Term Features
1. Add table-driven support for crypto coins (instead of hardcoded).
2. Historical volatility analysis charts.
3. Real-time price feed integration via WebSocket (e.g., Binance).
4. Technical indicators: RSI, MACD, Bollinger Bands.
5. News sentiment analysis overlay (CoinDesk or Twitter API).
6. AI strategy suggestion tool.
7. Export data and predictions to CSV/PDF.

## Notes
- All features must be modular and extensible.
- Keep UI responsive and clean.

---

## 🛠 Maintenance

- [ ] Document `main.py` responsibilities in `operations.md`.
- [ ] Improve error handling and logging for database and API failures.

---

## 📈 Future Ideas

- [ ] Integrate Kraken or Binance for exchange-specific trading data.
- [ ] Implement strategy simulation module (backtesting).
- [ ] Add Telegram/Email alerts when volatility or predictive thresholds are triggered.
