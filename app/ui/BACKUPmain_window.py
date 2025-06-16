from PyQt5.QtWidgets import QMainWindow, QApplication, QMenuBar, QAction, QStackedWidget
from PyQt5.QtCore import Qt
from app.ui.dashboard_widget import DashboardWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TradeSense AI")
        self.showMaximized()

        # Create menu bar
        self._create_menu_bar()

        # Central widget (modular layout)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Add default dashboard widget
        self.dashboard = DashboardWidget()
        self.stack.addWidget(self.dashboard)
        self.stack.setCurrentWidget(self.dashboard)

    def _create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
