# core-data-extract/fundamentals.py
import requests
import datetime
import logging

logger = logging.getLogger("TradeSenseAI")

class FundamentalsFetcher:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    def get_tokenomics(self, coin_id):
        url = f"{self.base_url}/coins/{coin_id}"
        try:
            res = requests.get(url, params={"localization": "false"})
            data = res.json()

            market_data = data.get("market_data", {})
            dev_data = data.get("developer_data", {})

            return {
                "market_cap": market_data.get("market_cap", {}).get("usd"),
                "circulating_supply": market_data.get("circulating_supply"),
                "max_supply": market_data.get("max_supply"),
                "total_volume": market_data.get("total_volume", {}).get("usd"),
                "commit_count_4w": dev_data.get("commit_count_4_weeks"),
                "timestamp": datetime.datetime.utcnow(),
            }
        except Exception as e:
            logger.warning(f"Failed to fetch tokenomics for {coin_id}: {e}")
            return {}

    def get_onchain_stub(self, coin_id):
        # Placeholder method for future integration with blockchain explorers
        return {
            "tx_count": None,
            "avg_gas_fee": None,
        }

    def calculate_score(self, tokenomics):
        # Example scoring algorithm (can be adjusted based on heuristics)
        if not tokenomics:
            return 0.0

        score = 0
        if tokenomics.get("market_cap"):
            score += min(tokenomics["market_cap"] / 1e9, 10)  # 10 points max
        if tokenomics.get("commit_count_4w"):
            score += min(tokenomics["commit_count_4w"] / 100, 5)  # 5 points max
        if tokenomics.get("circulating_supply") and tokenomics.get("max_supply"):
            ratio = tokenomics["circulating_supply"] / tokenomics["max_supply"]
            score += (1 - ratio) * 5  # Up to 5 points for low inflation

        return round(score, 2)

    def get_fundamentals(self, coin_id, label):
        tokenomics = self.get_tokenomics(coin_id)
        onchain = self.get_onchain_stub(coin_id)
        score = self.calculate_score(tokenomics)

        logger.info(f"Fundamentals score for {label}: {score}")
        return {
            **tokenomics,
            **onchain,
            "fundamentals_score": score
        }
