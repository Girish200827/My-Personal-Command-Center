from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QFrame,
)
from PySide6.QtCore import Signal, Qt
from models.task import Task


class TaskCard(QWidget):

    task_clicked = Signal(str)
    task_deleted = Signal(str)
    task_completed = Signal(str, bool)

    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self.task = task
        self._init_ui()
        self._apply_styles()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.task.completed)
        self.checkbox.stateChanged.connect(self._on_checkbox_changed)

        info_layout = QVBoxLayout()

        self.title_label = QLabel(self.task.title)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        info_layout.addWidget(self.title_label)

        if self.task.description:
            self.description_label = QLabel(self.task.description)
            self.description_label.setStyleSheet("color: #666; font-size: 12px;")
            self.description_label.setWordWrap(True)
            info_layout.addWidget(self.description_label)

        layout.addLayout(info_layout, 1)

        self.priority_label = QLabel(self.task.priority.value)
        self.priority_label.setStyleSheet(
            "background-color: #3498db; color: white;"
            "padding: 5px 10px; border-radius: 3px; font-size: 11px;"
        )
        layout.addWidget(self.priority_label)

        self.delete_btn = QPushButton("×")
        self.delete_btn.setFixedSize(30, 30)
        self.delete_btn.setStyleSheet(
            "QPushButton { background-color: #e74c3c; color: white;"
            "border-radius: 15px; font-size: 20px; font-weight: bold; }"
            "QPushButton:hover { background-color: #c0392b; }"
        )
        self.delete_btn.clicked.connect(self._on_deleted_clicked)
        layout.addWidget(self.delete_btn)

    def _apply_styles(self):
        self.setStyleSheet(
            """
            TaskCard {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            TaskCard:hover {
                border: 1px solid #3498db;
            }
        """
        )
        self.setCursor(Qt.PointingHandCursor)

    def _on_checkbox_changed(self, state):
        is_completed = state == Qt.Checked
        self.task_completed.emit(self.task.id, is_completed)

        if is_completed:
            self.title_label.setStyleSheet(
                "font-weight: bold, font_size: 14px;"
                "text-decoration: line-through; color: #999;"
            )
        else:
            self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")

    def _on_deleted_clicked(self):
        self.task_deleted.emit(self.task.id)

    def mousePressEvent(self, event):
        self.task_clicked.emit(self.task.id)
        super().mousePressEvent(event)

    def update_task(self, task: Task):
        self.task = task
        self.title_label.setText(task.title)
        self.checkbox.setChecked(task.completed)
        self.priority_label.setText(task.priority.value)
