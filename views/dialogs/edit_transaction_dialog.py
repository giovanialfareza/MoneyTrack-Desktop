from __future__ import annotations

from PySide6.QtCore import QDate

from models.transaction import (
    ExpenseTransaction,
    IncomeTransaction,
    TransferTransaction,
)
from views.dialogs.add_transaction_dialog import AddTransactionDialog


class EditTransactionDialog(AddTransactionDialog):
    """Dialog untuk mengubah transaksi yang sudah ada."""

    def __init__(self, controller, transaction, parent=None):
        self._transaction = transaction
        super().__init__(controller, parent)
        self.setWindowTitle("Edit Transaction")
        self._load_transaction()

    def _load_transaction(self):
        if isinstance(self._transaction, IncomeTransaction):
            transaction_type = "Income"
            wallet_id = self._transaction.wallet_id
        elif isinstance(self._transaction, ExpenseTransaction):
            transaction_type = "Expense"
            wallet_id = self._transaction.wallet_id
        elif isinstance(self._transaction, TransferTransaction):
            transaction_type = "Transfer"
            wallet_id = self._transaction.source_wallet_id
            self._set_combo_data(
                self.destination_wallet_input,
                self._transaction.destination_wallet_id,
            )
        else:
            return

        self.type_input.setCurrentText(transaction_type)
        self._set_combo_data(self.wallet_input, wallet_id)
        self.category_input.setCurrentText(self._transaction.category)
        self.amount_input.setValue(self._transaction.amount)
        self.description_input.setPlainText(self._transaction.description)

        date = QDate.fromString(self._transaction.date[:10], "yyyy-MM-dd")
        if date.isValid():
            self.date_input.setDate(date)

        self._update_destination_visibility()

    def _set_combo_data(self, combo, data):
        index = combo.findData(data)
        if index >= 0:
            combo.setCurrentIndex(index)
