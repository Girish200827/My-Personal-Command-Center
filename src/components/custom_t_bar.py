from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QMouseEvent
from datetime import datetime
from config.config import Config


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.dragging = False
        self.drag_position = QPoint()
        self.datetime_label = None
        self.timer = QTimer()

        self._init_ui()
        self._init_timer()

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
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)

        # Left side: Date and Time
        self.datetime_label = QLabel()
        self.datetime_label.setStyleSheet("color: white; font-size: 12px;")
        self.datetime_label.setMinimumWidth(200)
        layout.addWidget(self.datetime_label)

        # Center: WAR ROOM title
        layout.addStretch()
        self.title = QLabel("WAR ROOM")
        self.title.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.title)
        layout.addStretch()

        # Right side: Buttons
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

    def _init_timer(self):
        """Initialize and start the timer to update the clock every second."""
        self.timer.timeout.connect(self._update_datetime)
        self.timer.start(1000)  # Update every 1000ms (1 second)
        self._update_datetime()  # Initial update

    def _update_datetime(self):
        """Update the datetime label with current date, day, and time."""
        now = datetime.now()
        date_str = now.strftime("%m/%d/%Y")
        day_str = now.strftime("%A")
        time_str = now.strftime("%H:%M:%S")
        self.datetime_label.setText(f"{date_str} | {day_str} | TIME: {time_str}")

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
            self.dragging = True
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

    def closeEvent(self, event):
        """Stop the timer when the widget is closed."""
        self.timer.stop()
        super().closeEvent(event)
