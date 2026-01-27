from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
    QMessageBox,
    QPushButton,
)
from PySide6.QtGui import QCursor, QPixmap, QPalette, QBrush, QShortcut, QKeySequence
from PySide6.QtCore import Qt

bg_image_adr = (
    r"C:\Users\gsnis\Projects-2025\My-Personal-Command-Center\assets\blackboard_bg.png"
)


class MainView:
    def initUI(self):

        self.width, self.height = 1000, 600
        self.x, self.y = 200, 200

        self.setWindowTitle("My Personal Command Center")
        self.setGeometry(
            self.x, self.y, self.width, self.height
        )  # set position and size

        # Cursor customization
        pixmap_g_cursor = QPixmap("assets/cursor_g_white.png").scaled(40, 40)
        cursor_1 = QCursor(pixmap_g_cursor, -1, -1)
        self.setCursor(cursor_1)

        # App key shortcuts
        shortcut_1 = QShortcut(QKeySequence("Ctrl+F"), self)  # toggle fullscreen
        shortcut_1.activated.connect(self.toggle_fullscreen)

        shortcut_2 = QShortcut(QKeySequence("Ctrl+R"), self)  # reset geometry
        shortcut_2.activated.connect(self.resetGeo)

        shortcut_3 = QShortcut(QKeySequence("Ctrl+T"), self)  # toggle title bar
        shortcut_3.activated.connect(self.toggle_title_bar)

        # Set the background image
        bg_image = QPixmap("assets/blackboard_bg.png").scaled(self.width, self.height)
        palette = QPalette()
        palette.setBrush(
            QPalette.Window,
            QBrush(
                bg_image.scaled(
                    self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
                )
            ),
        )
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Testing label
        test_label = QLabel("My Personal Command Center")
        test_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setCentralWidget(test_label)

        # Testing push button
        test_button = QPushButton("Click Me")
        # test_button.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(test_label)
        layout.addWidget(test_button)

        # Create a verticle layout container
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    # function for app exit
    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        else:
            super().keyPressEvent(event)

    # toggle between fullscreen and normal window
    def toggle_fullscreen(self):
        if self.isFullScreen:
            self.showNormal()
        else:
            self.showFullScreen()
        self.isFullScreen = not self.isFullScreen

    def toggle_title_bar(self):
        if not self.title_bar_hidden:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.show()
            self.resetGeo()
        else:
            # Restore normal window with title bar
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
            self.show()
            self.resetGeo()

        self.title_bar_hidden = not self.title_bar_hidden

    # Reset the window size
    def resetGeo(self):
        rect = window.geometry()
        if (
            rect.x() != self.x
            or rect.y() != self.y
            or rect.width() != self.width
            or rect.height() != self.height
        ):
            self.setGeometry(
                self.x, self.y, self.width, self.height
            )  # reset window geometry
        else:
            pass
