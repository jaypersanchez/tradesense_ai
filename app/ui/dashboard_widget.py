from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QPushButton, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sqlalchemy import create_engine
import pandas as pd
import os

from app.services.ai_interpreter_service import AIInterpreterService
from dotenv import load_dotenv

load_dotenv()

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.engine = create_engine(os.getenv("POSTGRES_URL"))
        self.ai = AIInterpreterService()
        self.coins = {
            "btc_usd": "Bitcoin",
            "eth_usd": "Ethereum",
            "xrp_usd": "Ripple",
            "sol_usd": "Solana"
        }

        self.init_ui()

    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)

        title = QLabel("Crypto Dashboard: BTC, ETH, XRP, SOL")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        for pair, name in self.coins.items():
            card = self._create_coin_card(pair, name)
            layout.addWidget(card)

        scroll.setWidget(container)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def _create_coin_card(self, pair, name):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                border: 1px solid #d0d0d0;
                border-radius: 10px;
                padding: 14px;
                margin-bottom: 20px;
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #fefefe, stop:1 #f4f8fb
                );
            }
        """)

        layout = QVBoxLayout()

        try:
            df = pd.read_sql(f"{pair}_predictions", self.engine)
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            fig = Figure(figsize=(5, 2.5))
            ax = fig.add_subplot(111)
            ax.plot(df["timestamp"], df["price"], label="Actual")
            ax.plot(df["timestamp"], df["predicted"], label="Predicted")
            ax.set_title(f"{name} Price vs Prediction")
            ax.legend()
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)

            insight = self.ai.interpret_chart(name, df)
            insight_label = QLabel(insight)
            insight_label.setWordWrap(True)
            insight_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-top: 10px;
                margin-bottom: 20px;
            """)

            layout.addWidget(insight_label)

            # Expand Button
            expand_btn = QPushButton("View Fullscreen")
            expand_btn.clicked.connect(lambda: self._open_detail_view(name, df, insight))
            layout.addWidget(expand_btn)
            expand_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a90e2;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #357ab8;
                }
            """)

        except Exception as e:
            layout.addWidget(QLabel(f"Failed to load {name}: {str(e)}"))

        frame.setLayout(layout)
        return frame

    def _open_detail_view(self, name, df, insight):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{name} - Full View")
        dialog.setMinimumSize(1000, 600)

        layout = QVBoxLayout()

        fig = Figure(figsize=(9, 4))
        ax = fig.add_subplot(111)
        ax.plot(df["timestamp"], df["price"], label="Actual")
        ax.plot(df["timestamp"], df["predicted"], label="Predicted")
        ax.set_title(f"{name} - Price vs Prediction (Full)")
        ax.legend()
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        insight_label = QLabel(insight)
        insight_label.setWordWrap(True)
        layout.addWidget(insight_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        dialog.exec_()