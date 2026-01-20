from PySide6.QtCore import QObject, Signal
from typing import List, Optional
from models.task import Task, TaskCategory


class AppState(QObject):
    tasks_changed = Signal(list)
    task_added = Signal(Task)
    task_removed = Signal(str)
    task_updated = Signal(Task)

    def __init__(self):
        super().__init__()
        self._task: List[Task] = []

    @property
    def tasks(self) -> List[Task]:
        return self._tasks.copy()

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def get_tasks_by_category(self, category: TaskCategory) -> List[Task]:
        return [task for task in self._tasks if task.completed]

    def get_incompleted_tasks(self) -> List[Task]:
        return [task for task in self._tasks if not task.completed]

    def add_task(self, task: Task):
        self._tasks.append(task)
        self.task_added.emit(task)
        self.tasks_changed.emit(self._tasks.copy())

    def remove_task(self, task_id: str):
        self._tasks = [t for t in self._tasks if t.id != task_id]
        self.task_removed.emit(task_id)
        self.tasks_changed.emit(self._tasks.copy())

    def update_task(self, task: Task):
        for i, t in enumerate(self._tasks):
            if t.id == task.id:
                self._tasks[i] = task
                self.task_updated.emit(task)
                self.tasks_changed.emit(self._tasks.copy())
                break

    def clear_all_tasks(self):
        self._tasks.clear()
        self.tasks_changed.emit([])

    def load_tasks(self, tasks: List[Task]):
        self._tasks = tasks
        self.tasks_changed.emit(self.tasks.copy())
