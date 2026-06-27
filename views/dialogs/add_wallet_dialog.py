

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)


class AddWalletDialog(QDialog):
    """Dialog untuk menambahkan wallet baru.

    Dialog ini hanya mengumpulkan input pengguna.
    Tidak mengandung business logic maupun akses ke AppController.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Wallet")
        self.setModal(True)
        self.resize(360, 180)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Cash, BCA, Mandiri")

        self.balance_input = QDoubleSpinBox()
        self.balance_input.setRange(0, 1_000_000_000)
        self.balance_input.setDecimals(2)
        self.balance_input.setSingleStep(10000)
        self.balance_input.setPrefix("Rp ")

        form.addRow("Wallet Name", self.name_input)
        form.addRow("Initial Balance", self.balance_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def get_wallet_data(self) -> tuple[str, float]:
        return (
            self.name_input.text().strip(),
            float(self.balance_input.value()),
        )