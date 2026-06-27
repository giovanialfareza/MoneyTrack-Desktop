from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
    QFrame,
    QGridLayout,
)

from app.app_controller import AppController


class DashboardTab(QWidget):
    """Dashboard utama aplikasi MoneyTrack."""

    def __init__(self, controller: AppController):
        super().__init__()

        self._controller = controller
        self._controller.wallets_changed.connect(self.refresh)
        self._controller.transactions_changed.connect(self.refresh)

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("font-size:24px;font-weight:bold;")
        layout.addWidget(title)

        subtitle = QLabel("Welcome to MoneyTrack - Personal Finance Manager")
        subtitle.setObjectName("dashboardSubtitle")
        layout.addWidget(subtitle)

        cards = QGridLayout()
        cards.setHorizontalSpacing(16)

        self._wallets_value = QLabel()
        self._transactions_value = QLabel()
        self._balance_value = QLabel()

        cards.addWidget(self._create_card("Total Wallet", self._wallets_value), 0, 0)
        cards.addWidget(self._create_card("Total Transaction", self._transactions_value), 0, 1)
        cards.addWidget(self._create_card("Total Balance", self._balance_value), 0, 2)

        layout.addLayout(cards)
        layout.addStretch()

    def _create_card(self, title: str, value_label: QLabel) -> QFrame:
        frame = QFrame()
        frame.setObjectName("dashboardCard")

        layout = QVBoxLayout(frame)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        value_label.setObjectName("cardValue")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        return frame

    def refresh(self):
        self._wallets_value.setText(str(self._controller.wallet_count()))
        self._transactions_value.setText(str(self._controller.transaction_count()))
        balance = self._controller.get_total_balance()
        self._balance_value.setText(f"Rp {balance:,.0f}")