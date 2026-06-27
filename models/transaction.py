from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Transaction(ABC):
    """
    Abstract base class untuk seluruh jenis transaksi.
    """

    amount: float
    category: str
    description: str = ""

    id: str = field(default_factory=lambda: str(uuid4()))
    date: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )

    def transaction_type(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_display_type(self) -> str:
        """Return a user-friendly transaction type."""
        raise NotImplementedError

    @abstractmethod
    def get_display_wallet(self, wallets: dict[str, str]) -> str:
        """Return a user-friendly wallet description."""
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict):
        raise NotImplementedError


# ==========================================================
# INCOME
# ==========================================================

@dataclass
class IncomeTransaction(Transaction):

    wallet_id: str = ""

    def transaction_type(self) -> str:
        return "income"

    def get_display_type(self) -> str:
        return "Income"

    def get_display_wallet(self, wallets: dict[str, str]) -> str:
        return wallets.get(self.wallet_id, "-")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.transaction_type(),
            "wallet_id": self.wallet_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "IncomeTransaction":
        return cls(
            id=data["id"],
            wallet_id=data["wallet_id"],
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", ""),
            date=data["date"],
        )


# ==========================================================
# EXPENSE
# ==========================================================

@dataclass
class ExpenseTransaction(Transaction):

    wallet_id: str = ""

    def transaction_type(self) -> str:
        return "expense"

    def get_display_type(self) -> str:
        return "Expense"

    def get_display_wallet(self, wallets: dict[str, str]) -> str:
        return wallets.get(self.wallet_id, "-")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.transaction_type(),
            "wallet_id": self.wallet_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ExpenseTransaction":
        return cls(
            id=data["id"],
            wallet_id=data["wallet_id"],
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", ""),
            date=data["date"],
        )


# ==========================================================
# TRANSFER
# ==========================================================

@dataclass
class TransferTransaction(Transaction):

    source_wallet_id: str = ""
    destination_wallet_id: str = ""

    def transaction_type(self) -> str:
        return "transfer"

    def get_display_type(self) -> str:
        return "Transfer"

    def get_display_wallet(self, wallets: dict[str, str]) -> str:
        source = wallets.get(self.source_wallet_id, "-")
        destination = wallets.get(self.destination_wallet_id, "-")
        return f"{source} → {destination}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.transaction_type(),
            "source_wallet_id": self.source_wallet_id,
            "destination_wallet_id": self.destination_wallet_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TransferTransaction":
        return cls(
            id=data["id"],
            source_wallet_id=data["source_wallet_id"],
            destination_wallet_id=data["destination_wallet_id"],
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", ""),
            date=data["date"],
        )


# ==========================================================
# FACTORY
# ==========================================================

def transaction_from_dict(data: dict) -> Transaction:
    """
    Factory untuk mengubah dictionary menjadi object
    Transaction sesuai dengan field 'type'.
    """

    transaction_type = data["type"]

    if transaction_type == "income":
        return IncomeTransaction.from_dict(data)

    if transaction_type == "expense":
        return ExpenseTransaction.from_dict(data)

    if transaction_type == "transfer":
        return TransferTransaction.from_dict(data)

    raise ValueError(f"Unknown transaction type: {transaction_type}")