

from __future__ import annotations

from PySide6.QtCore import *
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QMessageBox,
)

from app.app_controller import AppController


class SettingsTab(QWidget):
    """Settings dan informasi aplikasi MoneyTrack."""

    APP_NAME = "MoneyTrack"
    VERSION = "1.0.0"

    def __init__(self, controller: AppController):
        super().__init__()
        self._controller = controller
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("font-size:24px;font-weight:bold;")
        layout.addWidget(title)

        about_group = QGroupBox("About")
        about_layout = QVBoxLayout(about_group)
        about_layout.addWidget(QLabel(f"Application : {self.APP_NAME}"))
        about_layout.addWidget(QLabel(f"Version : {self.VERSION}"))
        about_layout.addWidget(QLabel("Framework : PySide6"))
        about_layout.addWidget(QLabel("Architecture : MVC (Model-View-Controller)"))
        layout.addWidget(about_group)

        data_group = QGroupBox("Data")
        data_layout = QVBoxLayout(data_group)

        self.reset_button = QPushButton("Reset Application Data")
        self.reset_button.clicked.connect(self._reset_placeholder)

        data_layout.addWidget(self.reset_button)
        layout.addWidget(data_group)

        layout.addStretch()

    def _reset_placeholder(self):
        QMessageBox.information(
            self,
            "Coming Soon",
            "Reset data akan diimplementasikan pada versi berikutnya.",
        )