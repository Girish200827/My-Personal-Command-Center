import uuid
from datetime import datetime
from models.task import Task, TaskCategory, TaskPriority
from core.state import AppState
from services.database import Database


class TaskManager:
    def __init__(self, app_state: AppState, database: Database):
        self.state = app_state
        self.db = database

        self._load_task_from_db()

    def create_task(
        self,
        title: str,
        category: TaskCategory,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
    ):

        task_id = str(uuid.uuid4())

        task = Task(
            id=task_id,
            title=title,
            category=category,
            description=description,
            priority=priority,
        )

        self.state.add_task(task)

        self.db.save_task(task)

        return task

    def delete_task(self, task_id: str):
        self.state.remove_task(task_id)
        self.db.delete_task(task_id)

    def complete_task(self, task_id: str):
        task = self.state.get_task_by_id(task_id)
        if task:
            task.mark_complete()
            self.state.update_task(task)
            self.db.update_task(task)

    def update_task_details(self, task_id: str, **kwargs):
        task = self.state.get_task_by_id(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)

            self.state.update_task(task)
            self.db.update_task(task)

    def move_task_to_category(self, task_id: str, new_category: TaskCategory):
        self.update_task_details(task_id, category=new_category)

    def _load_task_from_db(self):
        tasks = self.db.load_all_tasks()
        self.state.load_tasks(tasks)
