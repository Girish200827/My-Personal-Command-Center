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
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from core.state import AppState
from models.task import TaskCategory
from config.config import Config
from components.button_pop_up import ButtonPopUp


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

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Shape.NoFrame)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.frame)

        # make the label a child of the frame so the frame's layout can center it
        self.image_label = QLabel(self.frame)
        pixmap = QPixmap(str(Config.BACKGROUNDS["ep_jar_bg"]))
        self._orig_pixmap = pixmap
        self.sized = self._orig_pixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        self.image_label.setPixmap(self.sized)
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignCenter)

        # center the label inside the frame using a layout
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        self.add_btn = QPushButton("+", self.frame)
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

        self.btn_pop = ButtonPopUp(self)
        self.add_btn.clicked.connect(self.btn_pop.show)

        self.btn_pop.task_clicked.connect(self.addTask)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # scale from the original pixmap so scaling isn't compounded
        self.sized = self._orig_pixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(self.sized)

    def addTask(self, category):
        print(f"Selected: {category}")

        # create rock label
        self.rock = QLabel(self.frame)
        rock_pixmap = QPixmap(str(Config.TASKCARDS[category]))
        # image scalling required here
        self.rock.setPixmap(rock_pixmap)
        self.rock.setScaledContents(True)

        if category == "Big Rocks":
            self.rock.resize(350, 350)
        elif category == "Pebbles":
            self.rock.resize(50, 50)
        elif category == "Sand":
            self.rock.resize(200, 200)
        else:
            self.rock.resize(100, 100)

        # Start position
        start_x = self.width() // 2 - 20
        start_y = -50

        # End position
        end_x = self.width() // 2 - 20
        end_y = self.height() // 2 + 40

        self.rock.move(start_x, start_y)
        self.rock.show()

        # Create animation
        self.anim = QPropertyAnimation(self.rock, b"pos")
        self.anim.setDuration(800)
        self.anim.setStartValue(QPoint(start_x, start_y))
        self.anim.setEndValue(QPoint(end_x, end_y))
        self.anim.setEasingCurve(QEasingCurve.OutBounce)

        self.anim.start()
