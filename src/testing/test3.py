import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.state import AppState


class Add():
    def __init__(self):
        self.app_state = AppState

        self.sections = {}

    def _on_task_added(self, task):
        section = self.sections[task.category]
        section.add_task_card(
            task,
            on_completed=self._on_task_completed,
            on_deleted=self._on_task_deleted,
            on_clicked=self._on_task_clicked,
        )
