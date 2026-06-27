from __future__ import annotations

from typing import List, Optional

from managers.data_manager import DataManager
from managers.wallet_manager import WalletManager
from models.transaction import (
    Transaction,
    IncomeTransaction,
    ExpenseTransaction,
    TransferTransaction,
)


class TransactionManager:
    """Business logic untuk seluruh transaksi."""

    def __init__(self, data_manager: DataManager, wallet_manager: WalletManager):
        self._data_manager = data_manager
        self._wallet_manager = wallet_manager
        self._transactions: List[Transaction] = self._data_manager.load_transactions()

    def get_all_transactions(self) -> List[Transaction]:
        return list(self._transactions)

    def get_transaction_by_id(self, transaction_id: str) -> Optional[Transaction]:
        return next((t for t in self._transactions if t.id == transaction_id), None)

    def transaction_exists(self, transaction_id: str) -> bool:
        return self.get_transaction_by_id(transaction_id) is not None

    def transaction_count(self) -> int:
        return len(self._transactions)

    def _save(self):
        self._data_manager.save_all(
            self._wallet_manager.get_all_wallets(),
            self._transactions,
        )

    def _apply(self, transaction: Transaction):
        if transaction.amount <= 0:
            raise ValueError("Nominal transaksi harus lebih dari 0.")
        if isinstance(transaction, IncomeTransaction):
            self._wallet_manager.deposit(transaction.wallet_id, transaction.amount)
        elif isinstance(transaction, ExpenseTransaction):
            self._wallet_manager.withdraw(transaction.wallet_id, transaction.amount)
        elif isinstance(transaction, TransferTransaction):
            self._wallet_manager.transfer(
                transaction.source_wallet_id,
                transaction.destination_wallet_id,
                transaction.amount,
            )

    def _rollback(self, transaction: Transaction):
        if isinstance(transaction, IncomeTransaction):
            self._wallet_manager.withdraw(transaction.wallet_id, transaction.amount)
        elif isinstance(transaction, ExpenseTransaction):
            self._wallet_manager.deposit(transaction.wallet_id, transaction.amount)
        elif isinstance(transaction, TransferTransaction):
            self._wallet_manager.transfer(
                transaction.destination_wallet_id,
                transaction.source_wallet_id,
                transaction.amount,
            )

    def add_transaction(self, transaction: Transaction) -> Transaction:
        self._apply(transaction)
        self._transactions.append(transaction)
        self._save()
        return transaction

    def delete_transaction(self, transaction_id: str):
        transaction = self.get_transaction_by_id(transaction_id)
        if transaction is None:
            raise ValueError("Transaction tidak ditemukan.")
        self._rollback(transaction)
        self._transactions.remove(transaction)
        self._save()

    def edit_transaction(self, transaction_id: str, new_transaction: Transaction) -> Transaction:
        old_transaction = self.get_transaction_by_id(transaction_id)
        if old_transaction is None:
            raise ValueError("Transaction tidak ditemukan.")

        index = self._transactions.index(old_transaction)
        self._rollback(old_transaction)
        new_transaction.id = old_transaction.id
        new_transaction.date = old_transaction.date
        self._apply(new_transaction)
        self._transactions[index] = new_transaction
        self._save()
        return new_transaction

    def search(self, keyword: str) -> List[Transaction]:
        keyword = keyword.lower().strip()

        return [
            transaction
            for transaction in self._transactions
            if keyword in transaction.category.lower()
            or keyword in transaction.description.lower()
        ]

    def sort_by_date(self, reverse: bool = True) -> List[Transaction]:
        return sorted(
            self._transactions,
            key=lambda transaction: transaction.date,
            reverse=reverse,
        )

    def sort_by_amount(self, reverse: bool = True) -> List[Transaction]:
        return sorted(
            self._transactions,
            key=lambda transaction: transaction.amount,
            reverse=reverse,
        )