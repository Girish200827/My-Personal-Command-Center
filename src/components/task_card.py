from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal


class TaskCard(QWidget):

    taskClicked = Signal(str)
    taskDeleted = Signal(str)

    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        self.title_label = QLabel(self.task_data.get("title", ""))
        layout.addWidget(self.title_label)

        self.setLayout(layout)

    def update_task(self, new_data):
        self.task_data = new_data
        self.title_label.setText(new_data.get("title", ""))
