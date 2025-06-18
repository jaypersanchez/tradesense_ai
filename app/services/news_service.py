import os
import requests
from datetime import datetime, timedelta

class NewsService:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"

    def get_news_for_coin(self, coin_name):
        today = datetime.utcnow().date()
        from_date = today - timedelta(days=7)
        params = {
            "q": coin_name,
            "from": from_date.isoformat(),
            "sortBy": "publishedAt",
            "apiKey": self.api_key,
            "language": "en",
            "pageSize": 3
        }
        response = requests.get(self.base_url, params=params)
        articles = response.json().get("articles", [])
        return [(a["title"], a["url"]) for a in articles]
