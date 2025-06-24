from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QFrame, QHBoxLayout, QFormLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import requests
import mplfinance as mpf
import pandas_ta as ta

class TradeSenseViewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TradeSense View")
        self.resize(1200, 900)

        self.symbol_map = {
            "BTC_USDC": "bitcoin",
            "ETH_USDC": "ethereum",
            "XRP_USDC": "ripple",
            "SOL_USDC": "solana"
        }

        self.init_ui()
        self.load_chart()  # Load initial view

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Sidebar layout using QFormLayout for better alignment
        form_layout = QFormLayout()

        self.pair_selector = QComboBox()
        self.pair_selector.addItems(self.symbol_map.keys())
        self.pair_selector.currentTextChanged.connect(self.load_chart)
        form_layout.addRow("Select Trading Pair:", self.pair_selector)

        self.timeframe_selector = QComboBox()
        self.timeframe_selector.addItems(["daily", "weekly"])
        self.timeframe_selector.currentTextChanged.connect(self.load_chart)
        form_layout.addRow("Select Timeframe:", self.timeframe_selector)

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