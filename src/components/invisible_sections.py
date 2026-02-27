from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QGridLayout,
    QInputDialog,
)
from PySide6.QtGui import QCursor, QPixmap
from PySide6.QtCore import Qt, Signal
from .task_card import TaskCard
from models.task import Task, TaskCategory
from config.config import Config
from pathlib import Path


class InvisibleSections(QWidget):

    add_task_requested = Signal(TaskCategory)

    def __init__(self, category: TaskCategory, parent=None):
        super().__init__(parent)
        self.category = category
        self.task_cards = {}
        self._init_ui()

    def _init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        section_layout = QGridLayout()

        add_btn = QPushButton("+")
        add_btn.clicked.connect(self._on_add_task_clicked)
        add_btn.setStyleSheet(
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

        section_layout.addWidget(add_btn, 0, 0, Qt.AlignTop | Qt.AlignLeft)

        main_layout.addLayout(section_layout)

    def add_task_card(self, task: Task, on_completed, on_deleted, on_clicked):
        card = TaskCard(task)

        card.task_completed.connect(on_completed)
        card.task_deleted.connect(on_deleted)
        card.task_clicked.connect(on_clicked)

        # self.tasks_layout.addWidget(card)

        self.task_cards[task.id] = card

    def _on_add_task_clicked(self, category: TaskCategory):
        title, ok = QInputDialog.getText(
            self, "New Mission Order", f"Enter task title for {self.category.value}:"
        )

        if ok and title.strip():
            task = self.task_manager.create_task(self.category, title)
