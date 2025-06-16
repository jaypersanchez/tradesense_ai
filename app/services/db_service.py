
import os
import pandas as pd
from sqlalchemy import create_engine

class DatabaseService:
    def __init__(self):
        self.engine = create_engine(os.getenv("POSTGRES_URL"))

    def save_ohlcv(self, pair, df):
        df.to_sql(f"{pair.lower()}_ohlcv", self.engine, if_exists="replace", index=False)

    def save_predictions(self, pair, df):
        df.to_sql(f"{pair.lower()}_predictions", self.engine, if_exists="replace", index=False)
