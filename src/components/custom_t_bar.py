from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QMouseEvent
from datetime import datetime
from config.config import Config
from .search_bar import SearchBar


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
        self.setObjectName("CustomTitleBar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            """
        #CustomTitleBar {
            background-color: rgba(26, 26, 26, 0.9);
        }
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)

        # Left side: Date and Time
        self.datetime_label = QLabel()
        self.datetime_label.setStyleSheet(
            "color: white; font-weight: bold; font-size: 12px;"
        )
        self.datetime_label.setMinimumWidth(200)
        layout.addWidget(self.datetime_label)

        # Center: WAR ROOM title
        layout.addStretch()

        self.search_bar = SearchBar(pages=Config.PAGES)
        self.search_bar.move((self.width() - self.search_bar.width()) // 2, 10)
        self.search_bar.page_selected.connect(lambda page: print(f"Selected: {page}"))
        self.search_bar.set_pages(["War Room", "New page"])

        layout.addWidget(self.search_bar)
        layout.addStretch()

        # Right side: Buttons
        self._create_button("——", self._on_minimize, layout)
        self._create_button("□□", self._on_maximize, layout)
        self._create_button("x", self._on_close, layout)

    def _create_button(self, text: str, callback, layout):
        btn = QPushButton(text)
        btn.setFixedSize(22, Config.TITLEBAR_HEIGHT)
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
        self.timer.timeout.connect(self._update_datetime)
        self.timer.start(1000)  # Update every second
        self._update_datetime()  # initial update

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
