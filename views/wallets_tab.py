from __future__ import annotations

from PySide6.QtCore import Qt
from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
)

from app.app_controller import AppController
from views.dialogs.add_wallet_dialog import AddWalletDialog
from views.dialogs.rename_wallet_dialog import RenameWalletDialog


class WalletsTab(QWidget):
    """Tab untuk menampilkan daftar wallet."""

    def __init__(self, controller: AppController):
        super().__init__()
        self._controller = controller
        self._controller.wallets_changed.connect(self.refresh)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("Wallets")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("font-size:24px;font-weight:bold;")
        layout.addWidget(title)

        toolbar = QHBoxLayout()
        icons_dir = (
            Path(__file__).resolve().parent.parent
            / "resources"
            / "icons"
        )
        self.add_button = QPushButton(" Add Wallet")
        self.rename_button = QPushButton(" Rename")
        self.delete_button = QPushButton(" Delete")

        self.add_button.setIcon(QIcon(str(icons_dir / "Add.png")))
        self.rename_button.setIcon(QIcon(str(icons_dir / "Edit.png")))
        self.delete_button.setIcon(QIcon(str(icons_dir / "Delete.png")))

        icon_size = QSize(18, 18)
        self.add_button.setIconSize(icon_size)
        self.rename_button.setIconSize(icon_size)
        self.delete_button.setIconSize(icon_size)

        self.add_button.clicked.connect(self._on_add_wallet)
        self.rename_button.clicked.connect(self._on_rename_wallet)
        self.delete_button.clicked.connect(self._on_delete_wallet)

        toolbar.addWidget(self.add_button)
        toolbar.addWidget(self.rename_button)
        toolbar.addWidget(self.delete_button)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels([
            "Wallet ID",
            "Wallet Name",
            "Balance",
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setShowGrid(False)

        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(38)

        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

    def refresh(self):
        wallets = self._controller.get_all_wallets()

        self.table.setRowCount(len(wallets))

        for row, wallet in enumerate(wallets):
            self.table.setItem(row, 0, QTableWidgetItem(wallet.id))
            self.table.setItem(row, 1, QTableWidgetItem(wallet.name))
            balance_item = QTableWidgetItem(f"Rp {wallet.balance:,.0f}")
            balance_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.table.setItem(row, 2, balance_item)

    def _selected_wallet(self):
        row = self.table.currentRow()
        if row < 0:
            return None

        item = self.table.item(row, 0)
        if item is None:
            return None

        return self._controller.get_wallet(item.text())

    def _on_add_wallet(self):
        dialog = AddWalletDialog(self)

        if dialog.exec():
            name, balance = dialog.get_wallet_data()
            self._controller.add_wallet(name, balance)

    def _on_rename_wallet(self):
        wallet = self._selected_wallet()

        if wallet is None:
            QMessageBox.information(self, "Rename Wallet", "Pilih wallet terlebih dahulu.")
            return

        dialog = RenameWalletDialog(wallet.name, self)

        if dialog.exec():
            self._controller.rename_wallet(wallet.id, dialog.get_wallet_name())

    def _on_delete_wallet(self):
        wallet = self._selected_wallet()

        if wallet is None:
            QMessageBox.information(self, "Delete Wallet", "Pilih wallet terlebih dahulu.")
            return

        reply = QMessageBox.question(
            self,
            "Delete Wallet",
            f"Hapus wallet '{wallet.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self._controller.delete_wallet(wallet.id)