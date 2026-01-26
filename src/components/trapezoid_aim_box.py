from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout
from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtGui import (
    QPainter,
    QPainterPath,
    QColor,
    QFont,
    QPen,
    QRegion,
    QLinearGradient,
)


class TrapezoidAimBox(QWidget):
    goal_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.goal_text = "Click to set your ONE goal..."
        self.is_editing = False
        self.setFixedHeight(60)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.text_edit = QLineEdit(self)
        self.text_edit.hide()
        self.text_edit.setAlignment(Qt.AlignCenter)
        self.text_edit.returnPressed.connect(self._finish_editing)
        self.text_edit.editingFinished.connect(self._finish_editing)

        self.setStyleSheet(
            """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.3);
                border: 2px solid white;
                border-radius: 5px;
                color: rgb(229, 215, 189);
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
            }
        """
        )

        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

        width = self.width()
        height = self.height()
        top_indent = 15
        bottom_indent = 5

        path = QPainterPath()
        path.moveTo(top_indent, 5)
        path.lineTo(width - top_indent, 5)
        path.lineTo(width - bottom_indent, height - 5)
        path.lineTo(bottom_indent, height - 5)
        path.closeSubpath()

        shadow_path = QPainterPath(path)
        shadow_path.translate(0, 3)
        painter.fillPath(shadow_path, QColor(0, 0, 0, 60))

        # Create a mask to clip the widget to only show the trapezoid
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

        gradient = QLinearGradient(0, 5, 0, height - 5)
        gradient.setColorAt(0, QColor("#000000"))
        gradient.setColorAt(1, QColor("#000000"))
        painter.fillPath(path, gradient)

        pen = QPen(QColor("#1a1a1a"), 3)
        painter.setPen(pen)
        painter.drawPath(path)

        if not self.is_editing:
            painter.setPen(QColor("#E5D7BD"))
            font = QFont("Segoe UI", 16, QFont.Bold)
            painter.setFont(font)

            text_rect = QRect(top_indent, 0, width - (top_indent * 2), height)
            painter.drawText(text_rect, Qt.AlignCenter, self.goal_text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._start_editing()

    def _start_editing(self):
        self.is_editing = True

        margin = 60
        self.text_edit.setGeometry(margin, 20, self.width() - (margin * 2), 35)
        self.text_edit.setText(self.goal_text)
        self.text_edit.show()
        self.text_edit.setFocus()
        self.text_edit.selectAll()

        self.update()

    def _finish_editing(self):
        self.is_editing = False

        new_text = self.text_edit.text().strip()
        if new_text:
            self.goal_text = new_text
            self.goal_changed.emit(self.goal_text)

        self.text_edit.hide()
        self.update()

    def set_goal(self, goal_text: str):
        self.goal_text = goal_text
        self.update()

    def get_goal(self) -> str:
        return self.goal_text
