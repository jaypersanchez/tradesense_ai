from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QFrame, QHBoxLayout, QFormLayout, QPushButton, QTextEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import requests
import mplfinance as mpf
import pandas_ta as ta
import os
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


class TradeSenseViewWidget(QWidget):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.engine = create_engine(os.getenv("POSTGRES_URL"))

        self.setWindowTitle("TradeSense View")
        self.resize(1200, 900)

        self.symbol_map = self.symbol_map = self._load_supported_symbols()
        '''{
                    "BTC_USDC": "bitcoin",
                    "ETH_USDC": "ethereum",
                    "XRP_USDC": "ripple",
                    "SOL_USDC": "solana"
                }'''

        self.init_ui()
        self.load_chart()  # Load initial view

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Sidebar layout using QFormLayout for better alignment
        form_layout = QFormLayout()
        
        self.pair_selector = QComboBox()
        #self.pair_selector.addItems(self.symbol_map.keys())
        self.pair_selector.addItems(self.symbol_map.keys())
        self.pair_selector.currentTextChanged.connect(self.load_chart)
        form_layout.addRow("Select Trading Pair:", self.pair_selector)

        self.timeframe_selector = QComboBox()
        self.timeframe_selector.addItems(["daily", "weekly"])
        self.timeframe_selector.currentTextChanged.connect(self.load_chart)
        form_layout.addRow("Select Timeframe:", self.timeframe_selector)

        self.insight_btn = QPushButton("Insight and Advise")
        self.insight_btn.clicked.connect(self.provide_insight)
        form_layout.addRow(self.insight_btn)

        self.insight_text = QTextEdit()
        self.insight_text.setReadOnly(True)
        form_layout.addRow(self.insight_text)

        sidebar_frame = QFrame()
        sidebar_frame.setLayout(form_layout)
        main_layout.addWidget(sidebar_frame, 1)

        # Chart area
        self.chart_frame = QFrame()
        self.chart_layout = QVBoxLayout(self.chart_frame)
        main_layout.addWidget(self.chart_frame, 4)

        self.setLayout(main_layout)

    def load_chart(self):
        pair_key = self.pair_selector.currentText()
        timeframe = self.timeframe_selector.currentText()
        self.current_pair = pair_key
        self.current_timeframe = timeframe
        coingecko_id = self.symbol_map.get(pair_key)

        if not coingecko_id:
            return

        url = f"https://api.coingecko.com/api/v3/coins/{coingecko_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": "365" if timeframe == "weekly" else "90",
            "interval": "daily"
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
            prices = data.get("prices", [])

            df = pd.DataFrame(prices, columns=["timestamp", "close"])
            df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("Date", inplace=True)

            df["open"] = df["close"].shift(1)
            df["high"] = df[["open", "close"]].max(axis=1) * 1.01
            df["low"] = df[["open", "close"]].min(axis=1) * 0.99
            df["volume"] = df["close"] * 0.03  # simple synthetic volume

            if timeframe == "weekly":
                df = df.resample("W").agg({
                    "open": "first",
                    "high": "max",
                    "low": "min",
                    "close": "last",
                    "volume": "sum"
                }).dropna()

            df["EMA_fast"] = df["close"].ewm(span=9).mean()
            df["EMA_slow"] = df["close"].ewm(span=21).mean()
            df.ta.rsi(length=14, append=True)
            df.ta.macd(append=True)
            df.dropna(inplace=True)

            self.df = df  # save for insight use

            for i in reversed(range(self.chart_layout.count())):
                self.chart_layout.itemAt(i).widget().setParent(None)

            apds = [
                mpf.make_addplot(df["EMA_fast"], color='green'),
                mpf.make_addplot(df["EMA_slow"], color='red'),
                mpf.make_addplot(df["RSI_14"], panel=1, color='blue', ylabel='RSI'),
                mpf.make_addplot(df[["MACDh_12_26_9"]], panel=2, type='bar', color='dimgray', ylabel='MACD Hist'),
                mpf.make_addplot(df[["MACD_12_26_9", "MACDs_12_26_9"]], panel=2),
                mpf.make_addplot(df["volume"], panel=3, type='bar', color='gray', ylabel='Volume')
            ]

            fig, _ = mpf.plot(
                df,
                type='candle',
                style='charles',
                addplot=apds,
                returnfig=True,
                title=f"{pair_key} - {timeframe.capitalize()} Chart",
                ylabel="Price (USD)",
                panel_ratios=(3, 1, 1, 1)
            )

            canvas = FigureCanvas(fig)
            self.chart_layout.addWidget(canvas)

        except Exception as e:
            self.chart_layout.addWidget(QLabel(f"Error loading chart: {str(e)}"))

    def provide_insight(self):
        if not hasattr(self, "df") or self.df.empty:
            self.insight_text.setPlainText("No chart data available for analysis.")
            return

        df = self.df
        pair = self.current_pair
        tf = self.current_timeframe
        last = df.iloc[-1]

        prompt = f"""
        Act as a technical swing trader. Given the following:
        Pair: {pair}
        Timeframe: {tf}
        Current Price: {last['close']:.2f}
        EMA 9: {last['EMA_fast']:.2f}, EMA 21: {last['EMA_slow']:.2f}
        RSI: {last['RSI_14']:.2f}
        MACD Histogram: {last['MACDh_12_26_9']:.2f}
        MACD: {last['MACD_12_26_9']:.2f}, Signal: {last['MACDs_12_26_9']:.2f}
        Volume: {last['volume']:.2f}

        Provide:
        - A short paragraph assessment of current price action
        - Key resistance and support levels (based on recent price highs/lows)
        - A suggested long and short entry with stop-loss and take-profit targets
        - ROI estimate for a $100 position in both scenarios
        - Tone: professional, concise, trader-grade
        """

        try:
            headers = {
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json"
            }

            body = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt.strip()}
                ],
                "max_tokens": 500
            }

            res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(body))
            res.raise_for_status()
            result = res.json()["choices"][0]["message"]["content"]
            self.insight_text.setPlainText(result.strip())

        except Exception as e:
            self.insight_text.setPlainText(f"Error calling OpenAI API: {str(e)}")

    def _load_supported_symbols(self):
        try:
            query = """
                SELECT symbol, coingecko_id
                FROM supported_symbols
                WHERE active = true AND symbol_type = 'spot'
            """
            df = pd.read_sql(text(query), self.engine)
            return dict(zip(df["symbol"], df["coingecko_id"]))
        except Exception as e:
            print(f"Error loading supported symbols: {e}")
            return {}
