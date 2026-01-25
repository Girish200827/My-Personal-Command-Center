from datetime import datetime
from src.models.task import Task, TaskCategory, TaskPriority
from src.services.database import Database
from pathlib import Path

# Create a dummy task with all required fields
dummy_task = Task(
    id="test_task_002",
    title="HSBDC Video Editing",
    description="This is a test task",
    category=TaskCategory.BIG_ROCK,
    priority=TaskPriority.HIGH,
    completed=False,
    created_at=datetime.now(),
    completed_at=None,
    due_date=datetime(2025, 12, 31),
)

# Initialize the database
db = Database()

# Try to save the task
print("Attempting to save task...")
db.save_task(dummy_task)
print("Task saved successfully!")

# Verify by loading it back
loaded_task = db.get_task_by_id("test_task_002")
if loaded_task:
    print(f"Task retrieved: {loaded_task.title}")
else:
    print("Failed to retrieve task")

db.close()
