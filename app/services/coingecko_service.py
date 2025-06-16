
import requests
import pandas as pd
from datetime import datetime

class CoinGeckoService:
    def fetch_ohlcv(self, coin_id, vs_currency="usd", days="30"):
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {"vs_currency": vs_currency, "days": days}
        res = requests.get(url, params=params).json()

        prices = res.get("prices", [])
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
