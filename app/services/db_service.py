
from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text  

def get_supported_symbols(self):
    q = text("SELECT symbol, coingecko_id, symbol_type FROM supported_symbols WHERE active = true")
    return pd.read_sql(q, self.engine)

from datetime import datetime

class DatabaseService:
    def __init__(self):
        self.engine = create_engine(os.getenv("POSTGRES_URL"))
        print("DB URL Loaded:", os.getenv("POSTGRES_URL"))

    def save_ohlcv(self, pair, df):
        df.to_sql(f"{pair.lower()}_ohlcv", self.engine, if_exists="replace", index=False)

    def save_predictions(self, pair, df):
        df.to_sql(f"{pair.lower()}_predictions", self.engine, if_exists="replace", index=False)

    def save_fundamentals(self, symbol, data):
        # Prepare a single-row DataFrame
        df = pd.DataFrame([{
            "symbol": symbol,
            "timestamp": data.get("timestamp", datetime.utcnow()),
            "market_cap": data.get("market_cap"),
            "circulating_supply": data.get("circulating_supply"),
            "max_supply": data.get("max_supply"),
            "total_volume": data.get("total_volume"),
            "commit_count_4w": data.get("commit_count_4w"),
            "tx_count": data.get("tx_count"),
            "avg_gas_fee": data.get("avg_gas_fee"),
            "fundamentals_score": data.get("fundamentals_score")
        }])

        # Append to fundamentals_data table
        df.to_sql("fundamentals_data", self.engine, if_exists="append", index=False)
        
    def get_supported_symbols(self):
        q = text("SELECT symbol, coingecko_id, symbol_type FROM supported_symbols WHERE active = true")
        return pd.read_sql(q, self.engine)

