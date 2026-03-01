from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QPalette, QBrush
from PySide6.QtCore import Qt, Signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import Config
from components.circular_cursor import CustomCursor


class ButtonPopUp(QWidget):

    task_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setWindowTitle("Select Task Category")
        self.setFixedSize(450, 200)

        CustomCursor(self, color="red")

        # build the UI once during initialization rather than every time the
        # popup is shown.  ``Config.TASKCARDS`` already contains both the
        # category names and the corresponding image paths, so iterate over
        # its items.
        main_layout = QVBoxLayout(self)
        layout_1 = QHBoxLayout()
        layout_2 = QHBoxLayout()
        for category, taskcard in Config.TASKCARDS.items():
            label = QLabel(category)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(
                "QLabel { background-color: transparent, color: white, border-radius: None; }"
            )
            label.setFixedSize(135, 20)
            layout_1.addWidget(label)

            btn = QLabel()
            btn.setAlignment(Qt.AlignCenter)
            btn.setStyleSheet(
                "QLabel { background-color: #3498db; color: white; padding: 10px; border-radius: 5px; }"
                "QLabel:hover { background-color: #2980b9; }"
            )
            btn.mousePressEvent = lambda event, cat=category: self._on_category_clicked(
                cat
            )
            layout_2.addWidget(btn)

            self._orig_pixmap = QPixmap(str(taskcard))

            if category == "Big Rocks":
                btn.setMargin(5)
            elif category == "Pebbles":
                btn.setMargin(40)
            elif category == "Sand":
                btn.setMargin(25)
            else:
                pass

            self.sized = self._orig_pixmap.scaled(
                btn.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            btn.setPixmap(self.sized)
            btn.setScaledContents(True)

        main_layout.addLayout(layout_1)
        main_layout.addLayout(layout_2)

    def showEvent(self, event):
        super().showEvent(event)

        parent = self.parentWidget()

        if parent:
            r_pos = parent.rect()
            a_pos = parent.mapToGlobal(r_pos.topLeft())

            x = a_pos.x() - (self.width() - parent.width()) // 2
            y = a_pos.y() - (self.height() - parent.height()) // 2

            self.move(x, y)

    def _on_category_clicked(self, category):
        self.task_clicked.emit(category)
        self.close()
