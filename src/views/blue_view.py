from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
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
        self.setObjectName("BlueView")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet(
            """
            #BlueView {
            background-color: rgba(0,0,0,0.2);
            }
        """
        )

        frame = QFrame(self)
        frame.setFrameShape(QFrame.Shape.NoFrame)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(frame)

        # make the label a child of the frame so the frame's layout can center it
        self.image_label = QLabel(frame)
        pixmap = QPixmap(str(Config.BACKGROUNDS["ep_jar_bg"]))
        self._orig_pixmap = pixmap
        self.sized = self._orig_pixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        self.image_label.setPixmap(self.sized)
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignCenter)

        # center the label inside the frame using a layout
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        self.add_btn = QPushButton("+", frame)
        self.add_btn.setGeometry(10, 10, 35, 35)
        self.add_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #132F18;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0C1F11;
            }
            """
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # scale from the original pixmap so scaling isn't compounded
        self.sized = self._orig_pixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(self.sized)
