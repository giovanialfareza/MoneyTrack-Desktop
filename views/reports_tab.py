from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QFrame,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from app.app_controller import AppController


class ReportsTab(QWidget):
    """Tab laporan transaksi."""

    def __init__(self, controller: AppController):
        super().__init__()

        self._controller = controller

        self._controller.transactions_changed.connect(self.refresh)
        self._controller.wallets_changed.connect(self.refresh)

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("Reports")
        title.setStyleSheet("font-size:24px;font-weight:bold;")
        layout.addWidget(title)

        summary_layout = QGridLayout()

        self.income_label = QLabel()
        self.expense_label = QLabel()
        self.balance_label = QLabel()

        summary_layout.addWidget(
            self._create_card("Total Income", self.income_label), 0, 0
        )
        summary_layout.addWidget(
            self._create_card("Total Expense", self.expense_label), 0, 1
        )
        summary_layout.addWidget(
            self._create_card("Net Balance", self.balance_label), 0, 2
        )

        layout.addLayout(summary_layout)

        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Filter"))

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(
            [
                "All",
                "Income",
                "Expense",
                "Transfer",
            ]
        )

        self.filter_combo.currentTextChanged.connect(self.refresh)

        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()

        layout.addLayout(filter_layout)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            [
                "Type",
                "Category",
                "Wallet",
                "Amount",
                "Description",
                "Date",
            ]
        )

        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setShowGrid(False)

        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(38)

        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

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
        transactions = self._controller.get_all_transactions()

        wallets = {
            wallet.id: wallet.name
            for wallet in self._controller.get_all_wallets()
        }

        income = 0.0
        expense = 0.0

        filter_type = self.filter_combo.currentText()

        filtered = []

        for transaction in transactions:

            tx_type = transaction.get_display_type()

            if filter_type != "All" and tx_type != filter_type:
                continue

            filtered.append(transaction)

            if tx_type == "Income":
                income += transaction.amount

            elif tx_type == "Expense":
                expense += transaction.amount

        self.income_label.setText(f"Rp {income:,.0f}")
        self.expense_label.setText(f"Rp {expense:,.0f}")
        self.balance_label.setText(f"Rp {(income-expense):,.0f}")

        self.table.setRowCount(len(filtered))

        for row, transaction in enumerate(filtered):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    transaction.get_display_type()
                ),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(transaction.category),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    transaction.get_display_wallet(wallets)
                ),
            )

            amount_item = QTableWidgetItem(
                f"Rp {transaction.amount:,.0f}"
            )
            amount_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.table.setItem(row, 3, amount_item)

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    transaction.description
                ),
            )

            date_item = QTableWidgetItem(transaction.date)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 5, date_item)