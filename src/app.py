from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QFrame
from PySide6.QtGui import QPixmap, QPalette, QBrush
from PySide6.QtCore import Qt
from config.config import Config
from views.war_room_view import WarRoomView
from views.blue_view import BlueView
from components.custom_t_bar import CustomTitleBar
from components.circular_cursor import CustomCursor
from components.trapezoid_aim_box import TrapezoidAimBox
from core.state import AppState
from services.database import Database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.app_state = AppState()
        self.database = Database()

        self._init_ui()
        self._setup_connections()
        self._load_goal()

        CustomCursor(self, color="blue")

    def _init_ui(self):
        self.setWindowTitle(Config.APP_NAME)
        self.resize(Config.DEFAULT_WINDOW_WIDTH, Config.DEFAULT_WINDOW_HEIGHT)
        self.setMinimumSize(Config.MIN_WINDOW_WIDTH, Config.MIN_WINDOW_HEIGHT)
        self.setMaximumSize(Config.MAX_WINDOW_WIDTH, Config.MAX_WINDOW_HEIGHT)

        if hasattr(Config, "USE_CUSTOM_TITLEBAR") and Config.USE_CUSTOM_TITLEBAR:
            self._setup_custom_window()
        else:
            self._setup_normal_window()

    def _setup_normal_window(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.war_room = BlueView(self.app_state)
        layout.addWidget(self.war_room)

    def _setup_custom_window(self):
        self.setWindowFlags(Qt.FramelessWindowHint)

        central_widget = QWidget()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.goal_box = TrapezoidAimBox()
        layout.addWidget(self.goal_box)

        content_container = QFrame()
        content_container.setObjectName("contentContainer")

        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.titlebar = CustomTitleBar(self)
        content_layout.addWidget(self.titlebar)

        self.war_room = BlueView(self.app_state)
        content_layout.addWidget(self.war_room)

        layout.addWidget(content_container)

    def _setup_connections(self):
        self.goal_box.goal_changed.connect(self._on_goal_changed)

        self.app_state.tasks_changed.connect(self._on_tasks_changed)

    def _on_goal_changed(self, goal_text: str):
        self.database.save_user_goal(goal_text)

    def _load_goal(self):
        goal = self.database.load_user_goal()
        if goal:
            self.goal_box.set_goal(goal)

    def _on_tasks_changed(self, tasks):
        task_count = len(tasks)
        self.setWindowTitle(f"{Config.APP_NAME} - {task_count} tasks")
