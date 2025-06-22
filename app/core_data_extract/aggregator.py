import pandas as pd
from sqlalchemy import text
from datetime import date
from datetime import timedelta
from typing import Optional
from app.services.db_service import DatabaseService  # ✅ class-based

db = DatabaseService()  # ✅ instantiate
ENGINE = db.engine      # ✅ use its engine

def run_daily_aggregation(target_day: Optional[date] = None):
    
    """
    Aggregate all fundamentals_data rows into daily stats.
    If target_day is None we aggregate 'yesterday'.
    """
    print("Running aggregation for day:", target_day)

    #target_day = target_day or date.today()
    target_day = target_day or (date.today() - timedelta(days=1))

    q = text("""
        SELECT *
        FROM fundamentals_data
        WHERE DATE(timestamp) = :day
    """)
    df = pd.read_sql(q, ENGINE, params={"day": target_day})

    if df.empty:
        print(f"No raw data for {target_day}")
        return

    groups = []
    for symbol, sub in df.groupby("symbol"):
        out = {
            "symbol": symbol,
            "day": target_day,
            "samples": len(sub),
            "avg_market_cap": sub["market_cap"].mean(),
            "pct_change_mcap": sub["market_cap"].pct_change().mean() * 100,
            "avg_total_volume": sub["total_volume"].mean(),
            "pct_change_vol": sub["total_volume"].pct_change().mean() * 100,
            "stddev_mcap": sub["market_cap"].std(),
            "stddev_volume": sub["total_volume"].std(),
            "avg_circ_supply": sub["circulating_supply"].mean(),
            "fundamentals_score_mean": sub["fundamentals_score"].mean(),
            "commit_count_4w_mean": sub["commit_count_4w"].mean()
        }
        groups.append(out)

    daily_df = pd.DataFrame(groups)
    daily_df.to_sql(
        "fundamentals_daily",
        ENGINE,
        if_exists="append",
        index=False,
        method="multi"
    )
    print(f"✅ Aggregated {len(daily_df)} symbols for {target_day}")

if __name__ == "__main__":
    run_daily_aggregation()
