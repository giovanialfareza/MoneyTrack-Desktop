

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)


class RenameWalletDialog(QDialog):
    """Dialog untuk mengganti nama wallet.

    Dialog ini hanya mengumpulkan input pengguna dan tidak mengandung business logic.
    """

    def __init__(self, current_name: str = "", parent=None):
        super().__init__(parent)

        self.setWindowTitle("Rename Wallet")
        self.setModal(True)
        self.resize(360, 140)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_input = QLineEdit(current_name)
        self.name_input.selectAll()

        form.addRow("Wallet Name", self.name_input)
        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def get_wallet_name(self) -> str:
        return self.name_input.text().strip()