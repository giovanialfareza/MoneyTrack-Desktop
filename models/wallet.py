from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Wallet:
    """
    Merepresentasikan sebuah wallet pada aplikasi MoneyTrack.

    Class ini hanya menyimpan data (entity/model).
    Seluruh business logic seperti deposit, withdraw,
    transfer, dan CRUD dilakukan oleh WalletManager.
    """

    name: str
    balance: float = 0.0
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )

    def to_dict(self) -> dict:
        """
        Mengubah object Wallet menjadi dictionary
        agar dapat disimpan ke JSON.
        """
        return {
            "id": self.id,
            "name": self.name,
            "balance": self.balance,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Wallet":
        """
        Membuat object Wallet dari dictionary
        hasil pembacaan JSON.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            balance=data.get("balance", 0.0),
            created_at=data.get(
                "created_at",
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

    def __repr__(self) -> str:
        return (
            f"Wallet("
            f"id='{self.id}', "
            f"name='{self.name}', "
            f"balance={self.balance:.2f})"
        )