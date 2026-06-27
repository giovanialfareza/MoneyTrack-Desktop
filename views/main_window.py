from __future__ import annotations
from pathlib import Path


from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QTabWidget, QStatusBar

from app.app_controller import AppController
from views.dashboard_tab import DashboardTab
from views.transactions_tab import TransactionsTab
from views.wallets_tab import WalletsTab
from views.reports_tab import ReportsTab
from views.settings_tab import SettingsTab



class MainWindow(QMainWindow):
    """Main window aplikasi MoneyTrack.

    Bertugas sebagai container seluruh tab.
    Tidak mengandung business logic.
    """

    def __init__(self):
        super().__init__()

        self._controller = AppController()

        self.setWindowTitle("MoneyTrack • Personal Finance Manager")
        self.resize(1280, 800)
        self.setMinimumSize(1100, 700)

        self._tabs = QTabWidget()
        self.setCentralWidget(self._tabs)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

        self._dashboard_tab = DashboardTab(self._controller)
        self._transactions_tab = TransactionsTab(self._controller)
        self._wallets_tab = WalletsTab(self._controller)
        self._reports_tab = ReportsTab(self._controller)
        self._settings_tab = SettingsTab(self._controller)

        icon_path = (
            Path(__file__).parent.parent
            / "resources"
            / "icons"
            / "AppIcon.png"
        )

        self._tabs.addTab(self._dashboard_tab, "Dashboard")
        self._tabs.addTab(self._transactions_tab, "Transactions")
        self._tabs.addTab(self._wallets_tab, "Wallets")
        self._tabs.addTab(self._reports_tab, "Reports")
        self._tabs.addTab(self._settings_tab, "Settings")

        app_icon = QIcon(str(icon_path))
        self._tabs.setTabIcon(0, app_icon)
        self._tabs.setTabIcon(1, app_icon)
        self._tabs.setTabIcon(2, app_icon)
        self._tabs.setTabIcon(3, app_icon)
        self._tabs.setTabIcon(4, app_icon)

        self.setWindowIcon(QIcon(str(icon_path)))