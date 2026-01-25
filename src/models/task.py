from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskCategory(Enum):
    BIG_ROCK = "Big Rocks"
    PEBBLE = "Pebbles"
    SAND = "Sand"


class TaskPriority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = " Low"


@dataclass
class Task:
    title: str
    id: str
    category: TaskCategory

    description: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    completed: bool = False
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    due_date: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def mark_complete(self):
        self.completed = True
        self.completed = datetime.now()

    def mark_incomplete(self):
        self.completed = False
        self.completed_at = None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category.value,
            "description": self.description,
            "priority": self.priority.value,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            category=TaskCategory(data["category"]),
            description=data.get("description", ""),
            priority=TaskPriority(data.get("priority", "Medium")),
            completed=data.get("completed", False),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else None
            ),
            completed_at=(
                datetime.fromisoformat(data["completed_at"])
                if data.get("completed_at")
                else None
            ),
            due_date=(
                datetime.fromisoformat(data["due_date"])
                if data.get("due_data")
                else None
            ),
        )
