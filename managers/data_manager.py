from __future__ import annotations

import json
import os
from pathlib import Path
import sys
from typing import List

from models.wallet import Wallet
from models.transaction import (
    Transaction,
    transaction_from_dict,
)


class DataManager:
    """
    Bertanggung jawab terhadap proses penyimpanan
    dan pembacaan data JSON.

    DataManager TIDAK memiliki business logic.
    """

    def __init__(self):

        if getattr(sys, "frozen", False):
            self.DATA_DIR = (
                Path.home()
                / "Library"
                / "Application Support"
                / "MoneyTrack"
            )
        else:
            self.DATA_DIR = Path("data")

        self.DATA_DIR.mkdir(parents=True, exist_ok=True)

        self.WALLETS_FILE = self.DATA_DIR / "wallets.json"
        self.TRANSACTIONS_FILE = self.DATA_DIR / "transactions.json"

        self._ensure_file(self.WALLETS_FILE)
        self._ensure_file(self.TRANSACTIONS_FILE)

    # =====================================================
    # PRIVATE
    # =====================================================

    def _ensure_file(self, path: Path):

        if not path.exists():

            path.write_text(
                "[]",
                encoding="utf-8"
            )

    def _read_json(self, path: Path) -> list:
        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON format: {path}") from exc

    def _write_json(self, path: Path, data: list):
        temp_path = path.with_suffix(path.suffix + ".tmp")

        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        os.replace(temp_path, path)

    # =====================================================
    # WALLET
    # =====================================================

    def load_wallets(self) -> List[Wallet]:

        data = self._read_json(self.WALLETS_FILE)

        return [Wallet.from_dict(item) for item in data]

    def save_wallets(
        self,
        wallets: List[Wallet]
    ):

        data = [wallet.to_dict() for wallet in wallets]
        self._write_json(self.WALLETS_FILE, data)

    # =====================================================
    # TRANSACTION
    # =====================================================

    def load_transactions(self) -> List[Transaction]:

        data = self._read_json(self.TRANSACTIONS_FILE)

        return [transaction_from_dict(item) for item in data]

    def save_transactions(
        self,
        transactions: List[Transaction]
    ):

        data = [transaction.to_dict() for transaction in transactions]
        self._write_json(self.TRANSACTIONS_FILE, data)

    # =====================================================
    # COORDINATED SAVE
    # =====================================================

    def save_all(
        self,
        wallets: List[Wallet],
        transactions: List[Transaction]
    ):

        self.save_wallets(wallets)

        self.save_transactions(transactions)