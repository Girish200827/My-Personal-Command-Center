from PySide6.QtGui import QCursor, QPixmap


class CustomCursor(QWidget):
    def __init__(self):
        pixmap_circle_cursor = QPixmap()
        cursor_1 = QCursor(pixmap_circle_cursor, -1, -1)
        self.setCursor(cursor_1)
