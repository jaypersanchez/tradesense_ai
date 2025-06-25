from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QStackedWidget
from PyQt5.QtCore import Qt
from app.ui.dashboard_widget import DashboardWidget
from app.ui.tradesense_view_widget import TradeSenseViewWidget
# from app.ui.wallet_tracker_widget import WalletTrackerWidget
# from app.ui.ai_assistant_widget import AIAssistantWidget
# from app.ui.trade_planner_widget import TradePlannerWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TradeSense AI")
        self.showMaximized()  # Fullscreen on launch

        # Stack to hold view widgets
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize views
        self.dashboard = DashboardWidget()
        self.tradesense_view = TradeSenseViewWidget()

        # self.wallet_tracker = WalletTrackerWidget()
        # self.ai_assistant = AIAssistantWidget()
        # self.trade_planner = TradePlannerWidget()

        # Dictionary of views
        self.views = {
            "Dashboard": self.dashboard,
            "TradeSense View": self.tradesense_view,
            # "Wallet Tracker": self.wallet_tracker,
            # "AI Assistant": self.ai_assistant,
            # "Trade Planner": self.trade_planner,
        }



        # Add views to stack
        for view in self.views.values():
            self.stack.addWidget(view)

        # Set default view
        self.stack.setCurrentWidget(self.dashboard)

        # Create menu after initializing views
        self._create_menu_bar()
        self.adjustSize()
        self.show()
        self.showMaximized()
        
    def _create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("View")
        for view_name in self.views:
            action = QAction(view_name, self)
            action.triggered.connect(lambda checked, name=view_name: self._switch_view(name))
            view_menu.addAction(action)

    def _switch_view(self, view_name):
        if view_name in self.views:
            self.stack.setCurrentWidget(self.views[view_name])
