import sqlite3
from typing import List, Optional
from pathlib import Path
from models.task import Task, TaskCategory, TaskPriority
from config.config import Config


class Database:
    def __init__(self, db_path: Path = None):
        self.db_path = db_path or Config.DATABASE_PATH

        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(str(self.db_path))

        self.connection.row_factory = sqlite3.Row

        self._create_tables()

    def _create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                       id TEXT PRIMARY KEY,
                       title TEXT NOT NULL,
                       description TEXT,
                       category TEXT NOT NULL,
                       priority TEXT NOT NULL,
                       completed INTEGER NOT NULL DEFAULT 0,
                       created_at TEXT NOT NULL,
                       completed_at TEXT,
                       due_date TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                       key TEXT PRIMARY KEY,
                       value TEXT
                    )
        """
        )

        self.connection.commit()

    def save_user_goal(self, goal: str):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO settings (key, value)
            VALUES ('user_goal', ?)
        """,
            (goal,),
        )
        self.connection.commit()

    def load_user_goal(self) -> str:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT value FROM  settings WHERE key = 'user_goal'
        """
        )
        result = cursor.fetchone()
        return result[0] if result else ""

    def save_task(self, task: Task):
        try:
            cursor = self.connection.cursor()

            cursor.execute(
                """
                INSERT INTO tasks (id, title, description, category, priority,
                        completed, created_at, completed_at, due_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    task.id,
                    task.title,
                    task.description,
                    task.category.value,
                    task.priority.value,
                    1 if task.completed else 0,
                    task.created_at.isoformat() if task.created_at else None,
                    task.completed_at.isoformat() if task.completed_at else None,
                    task.due_date.isoformat() if task.due_date else None,
                ),
            )

            self.connection.commit()
        except sqlite3.OperationalError as e:
            print(
                f"Error saving task: {e}. Please ensure all required fields are provided."
            )
            self.connection.rollback()
        except Exception as e:
            print(f"Unexpected error saving task: {e}")
            self.connection.rollback()

    def update_task(self, task: Task):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, category = ?, priority = ?,
                       completed = ?, completed_at = ?, due_date = ?
            WHERE id = ?
        """,
            (
                task.title,
                task.description,
                task.category.value,
                task.priority.value,
                1 if task.completed else 0,
                task.completed_at.isoformat() if task.completed_at else None,
                task.due_date.isoformat() if task.due_date else None,
                task.id,
            ),
        )

        self.connection.commit()

    def delete_task(self, task_id: str):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.connection.commit()

    def load_all_tasks(self) -> List[Task]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks")

        tasks = []
        for row in cursor.fetchall():
            task_dict = dict(row)
            tasks.append(Task.from_dict(task_dict))

        return tasks

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))

        row = cursor.fetchone()
        if row:
            return Task.from_dict(dict(row))
        return None

    def close(self):
        self.connection.close()
