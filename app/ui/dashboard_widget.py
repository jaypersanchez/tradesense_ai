from dotenv import load_dotenv
load_dotenv()

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
import pandas as pd
from sqlalchemy import create_engine
import os

from app.services.ai_interpreter_service import AIInterpreterService

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("Crypto Dashboard: BTC, ETH, XRP, SOL")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.engine = create_engine(os.getenv("POSTGRES_URL"))
        self.ai = AIInterpreterService()
        self.coins = {
            "btc_usd": "Bitcoin",
            "eth_usd": "Ethereum",
            "xrp_usd": "Ripple",
            "sol_usd": "Solana"
        }

        self.load_charts()

    def load_charts(self):
        for coin, name in self.coins.items():
            frame = QFrame()
            frame_layout = QVBoxLayout()

            try:
                df = pd.read_sql(f"{coin}_predictions", self.engine)
                df["timestamp"] = pd.to_datetime(df["timestamp"])

                # Chart
                fig = Figure(figsize=(6, 3))
                ax = fig.add_subplot(111)
                ax.plot(df["timestamp"], df["price"], label="Actual")
                ax.plot(df["timestamp"], df["predicted"], label="Predicted")
                ax.set_title(f"{name} Price vs Prediction")
                ax.legend()
                canvas = FigureCanvas(fig)
                frame_layout.addWidget(canvas)

                # GPT Insight
                insight = self.ai.interpret_chart(name, df)
                insight_label = QLabel(insight)
                insight_label.setWordWrap(True)
                insight_label.setStyleSheet("font-style: italic; margin: 5px 0 10px 0;")
                frame_layout.addWidget(insight_label)

            except Exception as e:
                error_label = QLabel(f"Failed to load {name.upper()}: {str(e)}")
                frame_layout.addWidget(error_label)

            frame.setLayout(frame_layout)
            frame.setStyleSheet("margin-bottom: 25px;")
            self.layout.addWidget(frame)
