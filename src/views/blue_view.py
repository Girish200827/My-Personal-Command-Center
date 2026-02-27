from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGridLayout,
)
from PySide6.QtGui import QCursor, QPixmap
from PySide6.QtCore import Qt, Signal
from core.state import AppState
from components.invisible_sections import InvisibleSections
from models.task import TaskCategory


class BlueView(QWidget):
    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)
        self.app_state = app_state
        self._init_ui()

    def _init_ui(self):
        layout = QGridLayout(self)
        invisible_section = InvisibleSections(category=TaskCategory)
        layout.addWidget(invisible_section, 0, 0)
