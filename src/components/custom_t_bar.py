from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent
from config.config import Config


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.dragging = False
        self.drag_position = QPoint()

        self._init_ui()

    def _init_ui(self):
        self.setFixedHeight(Config.TITLEBAR_HEIGHT)
        self.setStyleSheet(
            """
        CustomTittleBar {
                           background-color: #2c3e50;
                           }
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)

        self.title = QLabel(Config.APP_NAME)
        self.title.setStyleSheet("color: white; font-weight: bold")
        layout.addWidget(self.title)

        layout.addStretch()

        self._create_button("-", self._on_minimize, layout)
        self._create_button("□", self._on_maximize, layout)
        self._create_button("x", self._on_close, layout)

    def _create_button(self, text: str, callback, layout):
        btn = QPushButton(text)
        btn.setFixedSize(45, Config.TITLEBAR_HEIGHT)
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
        """
        )
        btn.clicked.connect(callback)
        layout.addWidget(btn)

    def _on_minimize(self):
        if self.parent_window:
            self.parent_window.showMinimized()

    def _on_maximize(self):
        if self.parent_window:
            if self.parent_window.isMaximized():
                self.parent_window.showNormal()
            else:
                self.parent_window.showMaximized()

    def _on_close(self):
        if self.parent_window:
            self.parent_window.close()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.draffing = True
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.parent_window.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.parent_window.move(
                event.globalPosition().toPoint() - self.drag_position
            )

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.dragging = False
