from app.services.coingecko_service import CoinGeckoService
from app.services.db_service import DatabaseService
from app.services.model_service import PredictionModel
import logging
from sqlalchemy import create_engine, text

engine = create_engine(os.getenv("POSTGRES_URL"))
from dotenv import load_dotenv
import os
import sys
from app.core_data_extract.fundamentals import FundamentalsFetcher
from app.core_data_extract.aggregator import run_daily_aggregation

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure .env is loaded from the project root no matter where it's run from
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)


# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TradeSenseAI")

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("TradeSenseAI")

    logger.info("Starting TradeSense AI")

    cg = CoinGeckoService()
    db = DatabaseService()
    predictor = PredictionModel()

    coins = fetch_active_coins() 
    '''{
        "BTC_USD": ("bitcoin", "usd"),
        "ETH_USD": ("ethereum", "usd"),
        "XRP_USD": ("ripple", "usd"),
        "SOL_USD": ("solana", "usd"),
    }'''

    for label, (coin_id, currency) in coins.items():
        logger.info(f"Fetching {label} OHLCV from CoinGecko")
        df = cg.fetch_ohlcv(coin_id, currency)

        if df.empty:
            logger.warning(f"No data received for {label}")
            continue

        db.save_ohlcv(label, df)
        logger.info(f"Saved {label} OHLCV to database")

        prediction = predictor.train_and_predict(df)
        db.save_predictions(label, prediction)
        logger.info(f"Saved {label} predictions to database")
        print(f"Predicted next price for {label}:\n", prediction.tail(5))
        
        # Now fetch fundamentals data
        print(f"\n\nNow extracting data for fundamental analysis")
        fundamentals = FundamentalsFetcher()
        fundamentals_data = fundamentals.get_fundamentals(coin_id, label)
        db.save_fundamentals(label, fundamentals_data)
        logger.info(f"Saved {label} fundamentals to database")

def fetch_active_coins():
    query = """
        SELECT symbol, coingecko_id, quote
        FROM supported_symbols
        WHERE active = true AND symbol_type = 'spot'
    """
    df = pd.read_sql(text(query), engine)
    return {
        row["symbol"]: (row["coingecko_id"], row["quote"].lower())
        for _, row in df.iterrows()
    }
    
if __name__ == "__main__":
    main()
    run_daily_aggregation()