from __future__ import annotations

from typing import List, Optional

from models.wallet import Wallet
from managers.data_manager import DataManager


class WalletManager:
    """
    Mengelola seluruh operasi yang berkaitan dengan Wallet.

    Business logic wallet berada di class ini.
    """

    def __init__(self, data_manager: DataManager):

        self._data_manager = data_manager
        self._wallets: List[Wallet] = self._data_manager.load_wallets()

    # =====================================================
    # GETTER
    # =====================================================

    def get_all_wallets(self) -> List[Wallet]:
        return list(self._wallets)

    def get_wallet_by_id(self, wallet_id: str) -> Optional[Wallet]:

        for wallet in self._wallets:
            if wallet.id == wallet_id:
                return wallet

        return None

    def get_wallet_by_name(self, name: str) -> Optional[Wallet]:
        name = name.strip()

        for wallet in self._wallets:
            if wallet.name.strip().lower() == name.lower():
                return wallet

        return None

    def total_balance(self) -> float:

        return sum(wallet.balance for wallet in self._wallets)

    # =====================================================
    # CRUD
    # =====================================================

    def add_wallet(
        self,
        name: str,
        balance: float = 0.0
    ) -> Wallet:
        name = name.strip()

        if not name:
            raise ValueError("Nama wallet tidak boleh kosong.")

        if self.get_wallet_by_name(name):
            raise ValueError("Wallet sudah ada.")

        wallet = Wallet(
            name=name,
            balance=balance
        )

        self._wallets.append(wallet)

        return wallet

    def rename_wallet(
        self,
        wallet_id: str,
        new_name: str
    ):
        new_name = new_name.strip()

        if not new_name:
            raise ValueError("Nama wallet tidak boleh kosong.")

        wallet = self.get_wallet_by_id(wallet_id)

        if wallet is None:
            raise ValueError("Wallet tidak ditemukan.")

        duplicate = self.get_wallet_by_name(new_name)

        if duplicate and duplicate.id != wallet_id:
            raise ValueError("Nama wallet sudah digunakan.")

        wallet.name = new_name

    def delete_wallet(
        self,
        wallet_id: str
    ):

        wallet = self.get_wallet_by_id(wallet_id)

        if wallet is None:
            raise ValueError("Wallet tidak ditemukan.")

        self._wallets.remove(wallet)

    # =====================================================
    # BALANCE
    # =====================================================

    def deposit(
        self,
        wallet_id: str,
        amount: float
    ):

        if amount <= 0:
            raise ValueError("Nominal harus lebih dari 0.")

        wallet = self.get_wallet_by_id(wallet_id)

        if wallet is None:
            raise ValueError("Wallet tidak ditemukan.")

        wallet.balance += amount
        return wallet

    def withdraw(
        self,
        wallet_id: str,
        amount: float
    ):

        if amount <= 0:
            raise ValueError("Nominal harus lebih dari 0.")

        wallet = self.get_wallet_by_id(wallet_id)

        if wallet is None:
            raise ValueError("Wallet tidak ditemukan.")

        if wallet.balance < amount:
            raise ValueError("Saldo tidak mencukupi.")

        wallet.balance -= amount
        return wallet

    def transfer(
        self,
        source_wallet_id: str,
        destination_wallet_id: str,
        amount: float
    ):

        if source_wallet_id == destination_wallet_id:
            raise ValueError("Wallet asal dan tujuan tidak boleh sama.")

        if amount <= 0:
            raise ValueError("Nominal harus lebih dari 0.")

        source = self.get_wallet_by_id(source_wallet_id)

        destination = self.get_wallet_by_id(destination_wallet_id)

        if source is None:
            raise ValueError("Wallet asal tidak ditemukan.")

        if destination is None:
            raise ValueError("Wallet tujuan tidak ditemukan.")

        if source.balance < amount:
            raise ValueError("Saldo tidak mencukupi.")

        source.balance -= amount
        destination.balance += amount
        return source, destination

    # =====================================================
    # BALANCE ADJUSTMENT
    # =====================================================

    def set_balance(
        self,
        wallet_id: str,
        new_balance: float
    ):

        if new_balance < 0:
            raise ValueError("Saldo tidak boleh negatif.")

        wallet = self.get_wallet_by_id(wallet_id)

        if wallet is None:
            raise ValueError("Wallet tidak ditemukan.")

        wallet.balance = new_balance
        return wallet

    # =====================================================
    # HELPER
    # =====================================================

    def wallet_exists(
        self,
        wallet_id: str
    ) -> bool:

        return self.get_wallet_by_id(wallet_id) is not None

    def wallet_count(self) -> int:

        return len(self._wallets)