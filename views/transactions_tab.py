from __future__ import annotations

from PySide6.QtCore import Qt, QSize
from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QMessageBox,
    QHeaderView,
)

from app.app_controller import AppController
from views.dialogs.edit_transaction_dialog import EditTransactionDialog
from views.dialogs.add_transaction_dialog import AddTransactionDialog


class TransactionsTab(QWidget):
    """Tab untuk menampilkan seluruh transaksi."""

    def __init__(self, controller: AppController):
        super().__init__()
        self._controller = controller
        self._controller.transactions_changed.connect(self.refresh)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("Transactions")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("font-size:24px;font-weight:bold;")
        layout.addWidget(title)

        toolbar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search category or description...")

        icons_dir = (
            Path(__file__).resolve().parent.parent
            / "resources"
            / "icons"
        )

        self.add_button = QPushButton(" Add")
        self.edit_button = QPushButton(" Edit")
        self.delete_button = QPushButton(" Delete")

        self.add_button.setIcon(QIcon(str(icons_dir / "Add.png")))
        self.edit_button.setIcon(QIcon(str(icons_dir / "Edit.png")))
        self.delete_button.setIcon(QIcon(str(icons_dir / "Delete.png")))

        icon_size = QSize(18, 18)
        self.add_button.setIconSize(icon_size)
        self.edit_button.setIconSize(icon_size)
        self.delete_button.setIconSize(icon_size)

        self.add_button.clicked.connect(self._add_transaction)
        self.edit_button.clicked.connect(self._edit_transaction)
        self.delete_button.clicked.connect(self._delete_transaction)

        toolbar.addWidget(self.search_input)
        toolbar.addWidget(self.add_button)
        toolbar.addWidget(self.edit_button)
        toolbar.addWidget(self.delete_button)

        layout.addLayout(toolbar)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Type",
            "Category",
            "Description",
            "Wallet",
            "Amount",
            "Date",
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)

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

        self.search_input.textChanged.connect(self._on_search)

    def refresh(self):
        self.table.setSortingEnabled(False)

        self._populate_table(
            self._controller.get_all_transactions()
        )

        self.table.setSortingEnabled(True)

    def _on_search(self, text: str):
        if not text.strip():
            self.refresh()
            return
        self._populate_table(self._controller.search_transactions(text))

    def _populate_table(self, transactions):
        self.table.setRowCount(len(transactions))

        wallets = {
            wallet.id: wallet.name
            for wallet in self._controller.get_all_wallets()
        }

        for row, transaction in enumerate(transactions):
            tx_type = transaction.get_display_type()
            wallet = transaction.get_display_wallet(wallets)

            type_item = QTableWidgetItem(tx_type)
            type_item.setData(Qt.ItemDataRole.UserRole, transaction.id)
            self.table.setItem(row, 0, type_item)
            self.table.setItem(row, 1, QTableWidgetItem(transaction.category))
            self.table.setItem(row, 2, QTableWidgetItem(transaction.description))
            self.table.setItem(row, 3, QTableWidgetItem(wallet))
            amount_item = QTableWidgetItem(f"Rp {transaction.amount:,.0f}")
            amount_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.table.setItem(row, 4, amount_item)
            date_item = QTableWidgetItem(transaction.date)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 5, date_item)

    def _selected_transaction_id(self) -> str | None:
        row = self.table.currentRow()
        if row < 0:
            return None

        item = self.table.item(row, 0)
        if item is None:
            return None

        return item.data(Qt.ItemDataRole.UserRole)

    def _add_transaction(self):
        dialog = AddTransactionDialog(self._controller, self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_transaction_data()

        self._controller.add_transaction_from_data(data)

    def _edit_transaction(self):
        transaction_id = self._selected_transaction_id()
        if transaction_id is None:
            return

        transaction = self._controller.get_transaction(transaction_id)
        if transaction is None:
            return

        dialog = EditTransactionDialog(self._controller, transaction, self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_transaction_data()
        self._controller.edit_transaction_from_data(
            transaction_id,
            data,
        )

    def _delete_transaction(self):
        transaction_id = self._selected_transaction_id()
        if transaction_id is None:
            return

        reply = QMessageBox.question(
            self,
            "Delete Transaction",
            "Hapus transaksi ini?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self._controller.delete_transaction(transaction_id)
