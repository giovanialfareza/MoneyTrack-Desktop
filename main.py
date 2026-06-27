

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from views.main_window import MainWindow


def main() -> int:
    """Entry point aplikasi MoneyTrack."""
    app = QApplication(sys.argv)

    style_path = (
        Path(__file__).parent
        / "resources"
        / "styles"
        / "style.qss"
    )

    if style_path.exists():
        with open(style_path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())

    icon_path = (
        Path(__file__).parent
        / "resources"
        / "icons"
        / "AppIcon.png"
    )

    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    if icon_path.exists():
        window.setWindowIcon(QIcon(str(icon_path)))
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())