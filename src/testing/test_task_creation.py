"""Test script to debug task creation without GUI"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.state import AppState
from core.task_manager import TaskManager
from services.database import Database
from models.task import TaskCategory, TaskPriority


def test_task_creation():
    print("=" * 60)
    print("Testing Task Creation Without GUI")
    print("=" * 60)
    
    # Initialize components
    print("\n1. Initializing AppState, Database, and TaskManager...")
    app_state = AppState()
    database = Database()
    task_manager = TaskManager(app_state, database)
    print("   ✓ Initialization complete")
    
    # Create a task
    print("\n2. Creating a new task...")
    try:
        task = task_manager.create_task(
            title="Test Task",
            category=TaskCategory.BIG_ROCK,
            description="This is a test task",
            priority=TaskPriority.HIGH
        )
        print(f"   ✓ Task created: {task.id}")
        print(f"   Title: {task.title}")
        print(f"   Category: {task.category.value}")
        print(f"   Priority: {task.priority.value}")
    except Exception as e:
        print(f"   ✗ Error creating task: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Verify task in state
    print("\n3. Verifying task in AppState...")
    all_tasks = app_state.tasks
    print(f"   Total tasks in state: {len(all_tasks)}")
    
    if task in all_tasks:
        print("   ✓ Task found in AppState")
    else:
        print("   ✗ Task NOT found in AppState")
    
    # Check tasks by category
    print("\n4. Checking tasks by category...")
    big_rock_tasks = app_state.get_tasks_by_category(TaskCategory.BIG_ROCK)
    print(f"   BIG_ROCK tasks: {len(big_rock_tasks)}")
    
    if task in big_rock_tasks:
        print("   ✓ Task found in BIG_ROCK category")
    else:
        print("   ✗ Task NOT found in BIG_ROCK category (THIS IS A BUG!)")
        print("      See the get_tasks_by_category method in state.py")
    
    # Verify in database
    print("\n5. Verifying task in Database...")
    try:
        db_tasks = database.load_all_tasks()
        print(f"   Total tasks in database: {len(db_tasks)}")
        
        if any(t.id == task.id for t in db_tasks):
            print("   ✓ Task found in Database")
        else:
            print("   ✗ Task NOT found in Database")
    except Exception as e:
        print(f"   ✗ Error reading database: {e}")
        import traceback
        traceback.print_exc()
    
    # Mark task complete and verify
    print("\n6. Testing mark_complete...")
    try:
        task.mark_complete()
        print(f"   Task completed: {task.completed}")
        if hasattr(task, 'completed_at') and task.completed_at:
            print(f"   Completed at: {task.completed_at}")
        else:
            print("   ✗ Warning: completed_at not set (check mark_complete method)")
    except Exception as e:
        print(f"   ✗ Error marking complete: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_task_creation()
