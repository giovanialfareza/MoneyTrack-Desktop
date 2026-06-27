from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from managers.data_manager import DataManager
from managers.transaction_manager import TransactionManager
from managers.wallet_manager import WalletManager

from models.transaction import (
    Transaction,
    IncomeTransaction,
    ExpenseTransaction,
    TransferTransaction,
)
from models.wallet import Wallet


class AppController(QObject):

    wallets_changed = Signal()
    transactions_changed = Signal()

    def __init__(self):
        super().__init__()

        self._data_manager = DataManager()

        self._wallet_manager = WalletManager(
            self._data_manager
        )

        self._transaction_manager = TransactionManager(
            self._data_manager,
            self._wallet_manager,
        )

    def _save(self):
        self._data_manager.save_all(
            self._wallet_manager.get_all_wallets(),
            self._transaction_manager.get_all_transactions(),
        )

    # =====================================================
    # WALLET
    # =====================================================

    def get_all_wallets(self) -> list[Wallet]:
        return self._wallet_manager.get_all_wallets()

    def get_wallet(self, wallet_id: str) -> Wallet | None:
        return self._wallet_manager.get_wallet_by_id(wallet_id)

    def wallet_exists(self, wallet_id: str) -> bool:
        return self._wallet_manager.wallet_exists(wallet_id)

    def wallet_count(self) -> int:
        return self._wallet_manager.wallet_count()

    def get_total_balance(self) -> float:
        return self._wallet_manager.total_balance()

    def add_wallet(
        self,
        name: str,
        balance: float = 0.0
    ):
        wallet = self._wallet_manager.add_wallet(
            name,
            balance,
        )

        self._save()
        self.wallets_changed.emit()

        return wallet

    def rename_wallet(
        self,
        wallet_id: str,
        new_name: str,
    ):
        self._wallet_manager.rename_wallet(
            wallet_id,
            new_name,
        )

        self._save()
        self.wallets_changed.emit()

    def delete_wallet(
        self,
        wallet_id: str,
    ):
        self._wallet_manager.delete_wallet(
            wallet_id
        )

        self._save()
        self.wallets_changed.emit()

    # =====================================================
    # TRANSACTION
    # =====================================================

    def get_all_transactions(self) -> list[Transaction]:
        return self._transaction_manager.get_all_transactions()

    def search_transactions(self, keyword: str) -> list[Transaction]:
        return self._transaction_manager.search(keyword)

    def sort_transactions_by_date(self, reverse: bool = True) -> list[Transaction]:
        return self._transaction_manager.sort_by_date(reverse)

    def sort_transactions_by_amount(self, reverse: bool = True) -> list[Transaction]:
        return self._transaction_manager.sort_by_amount(reverse)

    def get_transaction(
        self,
        transaction_id: str,
    ) -> Transaction | None:
        return self._transaction_manager.get_transaction_by_id(
            transaction_id
        )

    def transaction_exists(self, transaction_id: str) -> bool:
        return self._transaction_manager.transaction_exists(transaction_id)

    def transaction_count(self) -> int:
        return self._transaction_manager.transaction_count()

    def add_transaction_from_data(self, data: dict) -> Transaction:
        tx_type = data["type"]

        if tx_type == "income":
            transaction = IncomeTransaction(
                wallet_id=data["wallet_id"],
                amount=data["amount"],
                category=data["category"],
                description=data["description"],
                date=data["date"],
            )
        elif tx_type == "expense":
            transaction = ExpenseTransaction(
                wallet_id=data["wallet_id"],
                amount=data["amount"],
                category=data["category"],
                description=data["description"],
                date=data["date"],
            )
        else:
            transaction = TransferTransaction(
                source_wallet_id=data["wallet_id"],
                destination_wallet_id=data["destination_wallet_id"],
                amount=data["amount"],
                category=data["category"],
                description=data["description"],
                date=data["date"],
            )

        return self.add_transaction(transaction)

    def add_transaction(
        self,
        transaction: Transaction,
    ):
        transaction = self._transaction_manager.add_transaction(transaction)
        self.transactions_changed.emit()
        self.wallets_changed.emit()
        return transaction

    def edit_transaction_from_data(
        self,
        transaction_id: str,
        data: dict,
    ) -> Transaction:
        tx_type = data["type"]

        if tx_type == "income":
            transaction = IncomeTransaction(
                wallet_id=data["wallet_id"],
                amount=data["amount"],
                category=data["category"],
                description=data["description"],
                date=data["date"],
            )
        elif tx_type == "expense":
            transaction = ExpenseTransaction(
                wallet_id=data["wallet_id"],
                amount=data["amount"],
                category=data["category"],
                description=data["description"],
                date=data["date"],
            )
        else:
            transaction = TransferTransaction(
                source_wallet_id=data["wallet_id"],
                destination_wallet_id=data["destination_wallet_id"],
                amount=data["amount"],
                category=data["category"],
                description=data["description"],
                date=data["date"],
            )

        return self.edit_transaction(transaction_id, transaction)

    def edit_transaction(
        self,
        transaction_id: str,
        new_transaction: Transaction,
    ):
        transaction = self._transaction_manager.edit_transaction(
            transaction_id,
            new_transaction,
        )
        self.transactions_changed.emit()
        self.wallets_changed.emit()
        return transaction

    def delete_transaction(
        self,
        transaction_id: str,
    ):
        self._transaction_manager.delete_transaction(
            transaction_id
        )
        self.transactions_changed.emit()
        self.wallets_changed.emit()