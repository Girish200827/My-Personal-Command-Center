from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
)
from PySide6.QtGui import QPixmap, QPalette, QBrush
from PySide6.QtCore import Qt, Signal
from core.state import AppState
from components.invisible_sections import InvisibleSections
from models.task import TaskCategory
from config.config import Config


class BlueView(QWidget):
    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)
        self.app_state = app_state
        self._init_ui()

    def _init_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)

        background_path = Config.BACKGROUNDS.get("ep_jar_bg")
        pix_bg = QPixmap(str(background_path))
        pix_scaled = pix_bg.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(pix_scaled))

        self.setPalette(palette)
        self.setAutoFillBackground(True)

        layout = QGridLayout(self)
        invisible_section = InvisibleSections(category=TaskCategory)
        layout.addWidget(invisible_section, 0, 0)
