"""
Title: Unit Tests for TaskManager
Author: Allyson Taylor
Purpose: Unit tests for CRUD and XP awarding functionality
Last Modified: November 7, 2025
"""

import unittest
import os
import sqlite3
from src.controllers.task_manager import TaskManager

TEST_DB = 'test_arcadia.db'

class TestTaskManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create test DB and tables
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        cls.conn = sqlite3.connect(TEST_DB)
        cls.conn.execute('''
            CREATE TABLE users (
                userID INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(40) NOT NULL UNIQUE,
                password VARCHAR(64) NOT NULL,
                xp INTEGER DEFAULT 0,
                glitter INTEGER DEFAULT 0
            )
        ''')
        cls.conn.execute('''
            CREATE TABLE tasks (
                taskId INTEGER PRIMARY KEY AUTOINCREMENT,
                userID INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                dueDate TEXT,
                completed INTEGER DEFAULT 0,
                xpReward INTEGER DEFAULT 50,
                FOREIGN KEY(userID) REFERENCES users(userID)
            )
        ''')

        # Insert test user
        cls.conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ('testuser', 'testpasshash')
        )
        cls.conn.commit()

        cls.task_mgr = TaskManager(TEST_DB)
        cls.userID = cls.conn.execute(
            "SELECT userID FROM users WHERE username=?", ('testuser',)
        ).fetchone()[0]

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_1_create_task_valid(self):
        task_data = {
            'title': 'Test Task',
            'description': 'This is a test task.',
            'due_date': '2025-12-01',
            'xpReward': 100
        }
        task_id = self.task_mgr.create_task(self.userID, task_data)
        self.assertIsInstance(task_id, int)

    def test_2_get_tasks_filter_completed(self):
        task_complete = {
            'title': 'Complete Task',
            'description': '',
            'due_date': '2025-12-01',
            'xpReward': 50
        }
        tid = self.task_mgr.create_task(self.userID, task_complete)
        self.task_mgr.complete_task(self.userID, tid)

        tasks = self.task_mgr.get_tasks(self.userID, filters={'completed': False})
        for t in tasks:
            self.assertFalse(t['completed'])

        completed_tasks = self.task_mgr.get_tasks(self.userID, filters={'completed': True})
        self.assertTrue(any(t['completed'] for t in completed_tasks))

    def test_3_update_task(self):
        task_data = {
            'title': 'Update Task',
            'description': 'Before update',
            'due_date': '2025-12-01',
            'xpReward': 50
        }
        tid = self.task_mgr.create_task(self.userID, task_data)
        updated = self.task_mgr.update_task(tid, {'title': 'Updated Task', 'description': 'After update'})
        self.assertTrue(updated)
        task = self.task_mgr.get_tasks(self.userID)[-1]
        self.assertEqual(task['title'], 'Updated Task')

    def test_4_complete_task_awards_xp(self):
        initial_xp = self.conn.execute("SELECT xp FROM users WHERE userID=?", (self.userID,)).fetchone()[0]
        task_data = {
            'title': 'XP Task',
            'description': '',
            'due_date': '2025-12-01',
            'xpReward': 75
        }
        tid = self.task_mgr.create_task(self.userID, task_data)
        success = self.task_mgr.complete_task(self.userID, tid)
        self.assertTrue(success)
        new_xp = self.conn.execute("SELECT xp FROM users WHERE userID=?", (self.userID,)).fetchone()[0]
        self.assertEqual(new_xp, initial_xp + 75)

    def test_5_delete_task(self):
        task_data = {
            'title': 'Delete Task',
            'description': '',
            'due_date': '2025-12-01',
            'xpReward': 50
        }
        tid = self.task_mgr.create_task(self.userID, task_data)
        success = self.task_mgr.delete_task(tid)
        self.assertTrue(success)
        tasks = self.task_mgr.get_tasks(self.userID)
        self.assertFalse(any(t['taskId'] == tid for t in tasks))


if __name__ == '__main__':
    unittest.main()
