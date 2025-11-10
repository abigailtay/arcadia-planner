"""
Title: Task Manager Test Script 
Author: Allyson Taylor
Purpose: Test TaskManager class functionality
Last Modified: November 7, 2025
"""

from src.controllers.task_manager import TaskManager

def main():
    # Initialize with the database path
    task_mgr = TaskManager('arcadia.db')

    # Simulate a user ID (ensure this user exists in the DB)
    user_id = 1

    # Create a new task
    new_task = {
        'title': 'Finish CS project',
        'description': 'Complete all coding and documentation',
        'due_date': '2025-11-30',
        'xpReward': 100
    }
    task_id = task_mgr.create_task(user_id, new_task)
    print(f"Created task with ID: {task_id}")

    # Get tasks for the user
    tasks = task_mgr.get_tasks(user_id)
    print("User tasks:", tasks)

    # Update the task title
    task_mgr.update_task(task_id, {'title': 'Finish CS project - updated'})
    print(f"Updated task {task_id}")

    # Mark the task as complete and award XP
    if task_mgr.complete_task(user_id, task_id):
        print(f"Task {task_id} marked complete and XP awarded.")
    else:
        print(f"Failed to complete task {task_id}")

    # Delete the task
    if task_mgr.delete_task(task_id):
        print(f"Task {task_id} deleted.")
    else:
        print(f"Failed to delete task {task_id}")

if __name__ == "__main__":
    main()
