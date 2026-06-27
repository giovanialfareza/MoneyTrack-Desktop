

from __future__ import annotations

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QTextEdit,
    QVBoxLayout,
)

from app.app_controller import AppController


class AddTransactionDialog(QDialog):
    """Dialog untuk menambahkan transaksi baru.

    Dialog ini hanya mengumpulkan input pengguna.
    Tidak membuat Transaction maupun memanggil AppController.
    """

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self._controller = controller

        self.setWindowTitle("Add Transaction")
        self.setModal(True)
        self.resize(420, 320)

        self._build_ui()
        self._load_wallets()
        self._update_destination_visibility()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.type_input = QComboBox()
        self.type_input.addItems(["Income", "Expense", "Transfer"])
        self.type_input.currentTextChanged.connect(self._update_destination_visibility)

        self.wallet_input = QComboBox()
        self.destination_wallet_input = QComboBox()

        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems([
            "Salary", "Food", "Transport", "Shopping",
            "Bills", "Investment", "Transfer", "Other",
        ])

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0.01, 1_000_000_000)
        self.amount_input.setDecimals(2)
        self.amount_input.setPrefix("Rp ")

        self.description_input = QTextEdit()
        self.description_input.setFixedHeight(70)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        form.addRow("Type", self.type_input)
        form.addRow("Wallet", self.wallet_input)
        form.addRow("Destination", self.destination_wallet_input)
        form.addRow("Category", self.category_input)
        form.addRow("Amount", self.amount_input)
        form.addRow("Description", self.description_input)
        form.addRow("Date", self.date_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _load_wallets(self):
        self.wallet_input.clear()
        self.destination_wallet_input.clear()
        for wallet in self._controller.get_all_wallets():
            self.wallet_input.addItem(wallet.name, wallet.id)
            self.destination_wallet_input.addItem(wallet.name, wallet.id)

    def _update_destination_visibility(self):
        visible = self.type_input.currentText() == "Transfer"
        self.destination_wallet_input.setVisible(visible)
        label = self.layout().itemAt(0).layout().labelForField(self.destination_wallet_input)
        if label:
            label.setVisible(visible)

    def get_transaction_data(self) -> dict:
        return {
            "type": self.type_input.currentText().lower(),
            "wallet_id": self.wallet_input.currentData(),
            "destination_wallet_id": self.destination_wallet_input.currentData(),
            "category": self.category_input.currentText().strip(),
            "amount": float(self.amount_input.value()),
            "description": self.description_input.toPlainText().strip(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
        }