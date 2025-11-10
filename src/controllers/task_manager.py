"""
Title: Task Manager Controller
Author: Allyson Taylor
Purpose: Provides CRUD operations and task management logic for user tasks.
Last Modified: November 7, 2025
"""

import sqlite3
from typing import List, Dict, Optional


class TaskManager:
    """
    Controller class to manage user tasks including creation,
    retrieval with filtering, updates, deletion, and task completion logic.
    """

    def __init__(self, db_path: str):
        """
        Initialize TaskManager with path to SQLite database.

        :param db_path: str SQLite database file path
        """
        self.db_path = db_path

    def _connect(self):
        """Create and return a new database connection."""
        return sqlite3.connect(self.db_path)

    def create_task(self, user_id: int, task_data: dict) -> int:
        """
        Insert a new task into the database for given user.

        :param user_id: int User identifier
        :param task_data: dict Task details including title, description,
                          due_date (YYYY-MM-DD), category, subcategories, etc.
        :return: int Newly created task ID
        """
        conn = self._connect()
        cursor = conn.cursor()
        query = """
        INSERT INTO tasks (userId, title, description, dueDate, completed, xpReward)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        # Default xpReward can be set here, e.g., 50 points
        cursor.execute(query, (
            user_id,
            task_data.get('title', ''),
            task_data.get('description', ''),
            task_data.get('due_date', None),
            False,
            task_data.get('xpReward', 50)
        ))
        conn.commit()
        task_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return task_id

    def get_tasks(self, user_id: int, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Retrieve tasks for a user with optional filtering by category or completion status.

        :param user_id: int User identifier to fetch tasks for
        :param filters: Optional[Dict] Filters e.g., {'category': 'dinner', 'completed': False}
        :return: List[Dict] List of task dictionaries
        """
        conn = self._connect()
        cursor = conn.cursor()

        base_query = "SELECT taskId, title, description, dueDate, completed, xpReward FROM tasks WHERE userId = ?"
        params = [user_id]

        if filters:
            if 'category' in filters:
                base_query += " AND category = ?"
                params.append(filters['category'])
            if 'completed' in filters:
                base_query += " AND completed = ?"
                params.append(int(filters['completed']))

        cursor.execute(base_query, params)
        rows = cursor.fetchall()

        tasks = []
        for row in rows:
            tasks.append({
                'taskId': row[0],
                'title': row[1],
                'description': row[2],
                'dueDate': row[3],
                'completed': bool(row[4]),
                'xpReward': row[5]
            })

        cursor.close()
        conn.close()
        return tasks

    def update_task(self, task_id: int, update_data: dict) -> bool:
        """
        Update task fields by task ID.

        :param task_id: int Identifier of the task to update
        :param update_data: dict Fields to update, e.g., {'title': 'New Title', 'dueDate': 'YYYY-MM-DD'}
        :return: bool True if update was successful
        """
        conn = self._connect()
        cursor = conn.cursor()

        fields = []
        params = []

        for key, value in update_data.items():
            fields.append(f"{key} = ?")
            params.append(value)

        params.append(task_id)

        query = f"UPDATE tasks SET {', '.join(fields)} WHERE taskId = ?"
        cursor.execute(query, params)
        conn.commit()

        success = cursor.rowcount > 0

        cursor.close()
        conn.close()
        return success

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        :param task_id: int Task identifier to delete
        :return: bool True if deletion was successful
        """
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks WHERE taskId = ?", (task_id,))
        conn.commit()

        success = cursor.rowcount > 0

        cursor.close()
        conn.close()
        return success

    def complete_task(self, user_id: int, task_id: int) -> bool:
        """
        Mark a task as complete and award XP to the user.

        :param user_id: int User identifier completing the task
        :param task_id: int Task identifier to mark complete
        :return: bool True if task completion and XP award were successful
        """
        conn = self._connect()
        cursor = conn.cursor()

        # Mark task as completed
        cursor.execute("UPDATE tasks SET completed = 1 WHERE taskId = ? AND userId = ?", (task_id, user_id))
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return False  # Task not found or no update

        # Get XP reward value for the task
        cursor.execute("SELECT xpReward FROM tasks WHERE taskId = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return False  # Task not found

        xp_reward = row[0]

        # Update user's XP by adding the XP reward
        cursor.execute("UPDATE users SET xp = xp + ? WHERE userId = ?", (xp_reward, user_id))
        # Optionally, implement streak checks and glitter awards here as per the full gamification logic

        conn.commit()
        cursor.close()
        conn.close()
        return True
