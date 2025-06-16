import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AIInterpreterService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.endpoint = "https://api.openai.com/v1/chat/completions"

    def interpret_chart(self, coin_name, df):
        if df.empty:
            return "No data available to analyze."

        try:
            sample = df.tail(10)[["timestamp", "price"]].to_string(index=False)
            prompt = (
                f"You are a financial analyst. Here are recent prices for {coin_name}:\n\n"
                f"{sample}\n\n"
                "Please interpret the trend in natural language."
            )

            payload = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a helpful financial analyst."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 400
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            response = requests.post(self.endpoint, json=payload, headers=headers, timeout=15)

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            else:
                return f"OpenAI API error: {response.status_code} – {response.text}"

        except Exception as e:
            return f"Error interpreting chart: {e}"
