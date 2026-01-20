from PySide6.QtWidgets import QWidget, QVBoxLayout

from components.task_card import TaskCard


class WarRoomView(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        task = TaskCard({"title": "Finish project architecture"})
        task.taskClicked.connect(self._on_task_clicked)

        layout.addWidget(task)
