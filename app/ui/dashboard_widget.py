from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QPushButton, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd
import os

from app.services.ai_interpreter_service import AIInterpreterService
from app.services.news_service import NewsService
from app.services.text_to_speech_service import TextToSpeechService
from app.ui.tradesense_view_widget import TradeSenseViewWidget

from dotenv import load_dotenv
load_dotenv()

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.engine = create_engine(os.getenv("POSTGRES_URL"))
        self.ai = AIInterpreterService()
        self.news_service = NewsService()
        self.tts = TextToSpeechService()
        self.coins = self._load_supported_symbols()

        self.init_ui()

    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)

        title = QLabel("Crypto Dashboard")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        for symbol, coin_name in self.coins.items():
            card = self._create_coin_card(symbol, coin_name)
            layout.addWidget(card)

        scroll.setWidget(container)
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def _create_coin_card(self, symbol, name):
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
            query = f'SELECT * FROM "{symbol}_predictions"'
            df = pd.read_sql(text(query), self.engine)
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

            news = self.news_service.get_news_for_coin(symbol.split("_")[0])
            news_title = QLabel(f"<b>📰 Recent News on {name}</b>")
            layout.addWidget(news_title)

            for title, url in news:
                label = QLabel(f'<a href="{url}">• {title}</a>')
                label.setOpenExternalLinks(True)
                label.setStyleSheet("color: #0066cc; margin-left: 10px;")
                layout.addWidget(label)

            listen_btn = QPushButton("🔊 Listen to Insight")
            listen_btn.clicked.connect(lambda _, text=insight: self.tts.speak(text))
            layout.addWidget(listen_btn)

            expand_btn = QPushButton("View Fullscreen")
            expand_btn.clicked.connect(lambda: self._open_detail_view(symbol, name, df, insight))
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

    def _open_detail_view(self, symbol, name, df, insight):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{name} - Full View")
        dialog.setMinimumSize(1000, 600)

        layout = QVBoxLayout()

        fundamentals = self._get_latest_fundamentals(symbol.upper())

        if fundamentals:
            fundamentals_html = "<b>📊 Fundamentals</b><br><ul>"
            for key, value in fundamentals.items():
                if key == "timestamp":
                    continue
                fundamentals_html += f"<li><b>{key.replace('_', ' ').title()}</b>: {value}</li>"
            fundamentals_html += "</ul>"

            fundamentals_label = QLabel(fundamentals_html)
            fundamentals_label.setWordWrap(True)
            fundamentals_label.setStyleSheet("font-size: 14px; margin-top: 10px;")
            layout.addWidget(fundamentals_label)
        elif isinstance(fundamentals, dict) and "error" in fundamentals:
            layout.addWidget(QLabel(f"Error loading fundamentals: {fundamentals['error']}"))
        else:
            layout.addWidget(QLabel("No fundamentals data available."))

        trend_df = self._get_fundamentals_trend(symbol.upper())
        
        if isinstance(trend_df, pd.DataFrame):
            
            # ✅ Convert numeric fields to float
            for col in ["avg_market_cap", "avg_total_volume", "pct_change_mcap", "stddev_mcap"]:
                trend_df[col] = pd.to_numeric(trend_df[col], errors="coerce")
            trend_df.dropna(inplace=True)
            
            trend_fig = Figure(figsize=(9, 3.5))
            trend_ax = trend_fig.add_subplot(111)
            trend_ax.plot(trend_df["day"], trend_df["avg_market_cap"], label="Market Cap Avg", color="blue")
            trend_ax.plot(trend_df["day"], trend_df["avg_total_volume"], label="Volume Avg", color="green")
            trend_ax.plot(trend_df["day"], trend_df["pct_change_mcap"], label="% Change Market Cap", color="orange")
            trend_ax.plot(trend_df["day"], trend_df["stddev_mcap"], label="Volatility (Market Cap)", color="red")

            trend_ax.set_title(f"{name} - Fundamentals Trend")
            trend_ax.legend()
            trend_canvas = FigureCanvas(trend_fig)
            layout.addWidget(QLabel("<b>📈 Fundamentals Trend</b>"))
            layout.addWidget(trend_canvas)
        elif isinstance(trend_df, dict) and "error" in trend_df:
            layout.addWidget(QLabel(f"Trend data error: {trend_df['error']}"))
        else:
            layout.addWidget(QLabel("No trend data available."))

        # --- Buttons ---
        buttons = QDialogButtonBox()
        btn_tradesense = QPushButton("📈 Open TradeSense")
        btn_tradesense.clicked.connect(self._open_tradesense_view)
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(dialog.reject)

        buttons.addButton(btn_tradesense, QDialogButtonBox.ActionRole)
        buttons.addButton(btn_close, QDialogButtonBox.RejectRole)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        dialog.exec_()

    def _open_tradesense_view(self):
        ts_dialog = QDialog(self)
        ts_dialog.setWindowTitle("TradeSense View")
        ts_dialog.setMinimumSize(1200, 800)
        layout = QVBoxLayout()
        layout.addWidget(TradeSenseViewWidget())
        ts_dialog.setLayout(layout)
        ts_dialog.exec_()

    def _get_latest_fundamentals(self, symbol):
        try:
            query = """
                SELECT *
                FROM fundamentals_data
                WHERE symbol = :symbol
                ORDER BY timestamp DESC
                LIMIT 1
            """
            df = pd.read_sql(text(query), self.engine, params={"symbol": symbol})
            return df.iloc[0].to_dict() if not df.empty else None
        except Exception as e:
            return {"error": str(e)}

    def _get_fundamentals_trend(self, symbol):
        try:
            query = """
                SELECT 
                    day, avg_market_cap, pct_change_mcap,
                    avg_total_volume, pct_change_vol,
                    stddev_mcap, stddev_volume
                FROM fundamentals_daily
                WHERE symbol = :symbol
                ORDER BY day ASC
            """
            df = pd.read_sql(text(query), self.engine, params={"symbol": symbol})
            return df if not df.empty else None
        except Exception as e:
            return {"error": str(e)}

    def _load_supported_symbols(self):
        try:
            query = """
                SELECT symbol, coingecko_id
                FROM supported_symbols
                WHERE active = true AND symbol_type = 'spot'
            """
            df = pd.read_sql(text(query), self.engine)

            existing_tables = {"btc_usd", "eth_usd", "xrp_usd", "sol_usd"}  # Tables you know exist
            return {
                row["symbol"].lower(): row["coingecko_id"].capitalize()
                for _, row in df.iterrows()
                if row["symbol"].lower() in existing_tables
            }
        except Exception as e:
            print(f"Error loading supported symbols: {e}")
            return {}
