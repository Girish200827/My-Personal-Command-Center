from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton
from PySide6.QtCore import Qt, Signal
from components.task_card import TaskCard
from models.task import Task, TaskCategory


class SectionContainer(QWidget):

    add_task_requested = Signal(TaskCategory)

    def __init__(self, category: TaskCategory, parent=None):
        super().__init__(parent)
        self.category = category
        self.task_cards = {}
        self._init_ui()

    def _init_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        header_layout = QVBoxLayout()

        title = QLabel(self.category.value)
        title.setStyleSheet("font-size: 18px; font-weight: bold")
        header_layout.addWidget(title)

        add_btn = QPushButton("+ Add Task")
        add_btn.clicked.connect(self._on_add_task_clicked)
        add_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """
        )
        header_layout.addWidget(add_btn)

        layout.addLayout(header_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.setAlignment(Qt.AlignTop)
        self.tasks_layout.setSpacing(10)

        scroll.setWidget(self.tasks_container)
        layout.addWidget(scroll)

        self.setStyleSheet(
            """
            SectionContainer {
                background-color: #f5f5f5;
                border-radius: 8px;
                }
        """
        )

    def add_task_card(self, task: Task, on_completed, on_deleted, on_clicked):
        card = TaskCard(task)

        card.task_completed.connect(on_completed)
        card.task_deleted.connect(on_deleted)
        card.task_clicked.connect(on_clicked)

        self.tasks_layout.addWidget(card)

        self.task_cards[task.id] = card

    def remove_task_card(self, task_id: str):
        if task_id in self.task_cards:
            card = self.task_cards[task_id]
            self.task_cards[task_id]
            card.deleteLater()
            del self.task_cards[task_id]

    def clear_tasks(self):
        for task_id in list(self.task_cards.keys()):
            self.remove_task_card(task_id)

    def _on_add_task_clicked(self):
        self.add_task_requested.emit(self.category)
