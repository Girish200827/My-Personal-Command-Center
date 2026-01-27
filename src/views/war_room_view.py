from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox,
    QInputDialog,
    QHBoxLayout,
)
from PySide6.QtCore import Qt
from components.section_container import SectionContainer
from models.task import TaskCategory, TaskPriority
from core.state import AppState
from core.task_manager import TaskManager
from services.database import Database


class WarRoomView(QWidget):
    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)

        self.app_state = app_state

        self.database = Database()
        self.task_manager = TaskManager(self.app_state, self.database)

        self.sections = {}

        self._init_ui()
        self._setup_connection()
        self._load_tasks()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        for category in TaskCategory:
            section = SectionContainer(category)
            self.sections[category] = section
            layout.addWidget(section)

    def _setup_connection(self):
        self.app_state.task_added.connect(self._on_task_added)
        self.app_state.task_removed.connect(self._on_task_removed)
        self.app_state.task_updated.connect(self._on_task_updated)

        for section in self.sections.values():
            section.add_task_requested.connect(self._on_add_task_requested)

    def _load_tasks(self):

        for category in TaskCategory:
            tasks = self.app_state.get_tasks_by_category(category)
            section = self.sections[category]

            for task in tasks:
                section.add_task_card(
                    task,
                    on_completed=self._on_task_completed,
                    on_deleted=self._on_task_deleted,
                    on_clicked=self._on_task_clicked,
                )

    def _on_add_task_requested(self, category: TaskCategory):
        title, ok = QInputDialog.getText(
            self, "New Task", f"Enter task title for {category.value}:"
        )

        if ok and title.strip():
            task = self.task_manager.create_task(
                title=title.strip(), category=category, priority=TaskPriority.MEDIUM
            )

    def _on_task_added(self, task):
        section = self.sections[task.category]
        section.add_task_card(
            task,
            on_completed=self._on_task_completed,
            on_deleted=self._on_task_deleted,
            on_clicked=self._on_task_clicked,
        )

    def _on_task_removed(self, task_id: str):
        for section in self.sections.values():
            section.remove_task_card(task_id)

    def _on_task_updated(self, task):
        for section in self.sections.values():
            section.remove_task_card(task.id)

        section = self.sections[task.category]
        section.add_task_card(
            task,
            on_completed=self._on_task_completed,
            on_deleted=self._on_task_deleted,
            on_clicked=self._on_task_clicked,
        )

    def _on_task_completed(self, task_id: str, is_completed: bool):
        if is_completed:
            self.task_manager.complete_task(task_id)
        else:
            task = self.app_state.get_task_by_id(task_id)
            if task:
                task.mark_incomplete()
                self.app_state.update_task(task)
                self.database.update_task(task)

    def _on_task_deleted(self, task_id: str):
        reply = QMessageBox.question(
            self,
            "Delete Task",
            "Are you sure you want to delete this task?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.task_manager.delete_task(task_id)

    def _on_task_clicked(self, task_id: str):
        print(f"Task clicked: {task_id}")
