from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from app import MainWindow
from config.config import Config
import sys


def main():
    app = QApplication(sys.argv)

    app.setApplicationName(Config.APP_NAME)
    app.setApplicationVersion(Config.VERSION)

    stylesheet_path = Config.get_stylesheet_path()
    if stylesheet_path.exists():
        with open(stylesheet_path, "r") as f:
            app.setStyleSheet(f.read())

    Config.ensure_directories()

    window = MainWindow()
    window.move(100, 75)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
