# Arcadia Planner API Contract
**Version:** 1.0  
**Date:** November 4, 2025  
**Sprint:** Sprint 1 (Foundation – Authentication & Task Management)  
**Authors:** Allyson Taylor (Backend), Xavier Nixon (Frontend)

---

## Table of Contents
1. [Data Models](#1-data-models)
2. [Authentication API](#2-authentication-api-authcontroller)
3. [Task Management API](#3-task-management-api-taskcontroller)
4. [Currency Management API](#4-currency-management-api-currencycontroller)
5. [Error Handling](#5-error-handling)
6. [Frontend-Backend Communication Examples](#6-frontend-backend-communication-examples)
7. [Testing Guidelines](#7-testing-guidelines)
8. [Change Log](#8-change-log)

---

## 1. Data Models

### 1.1 User Model

**Description:** Represents a registered user in Arcadia Planner.

{
"user_id": int, # Unique identifier (Primary Key)
"username": str, # Display name (3-40 chars, alphanumeric + underscore)
"password": str, # Hashed password (SHA-256, 64 chars)
"points": int, # Legacy points system (default: 0)
"xp": int, # Experience points (default: 0)
"glitter": int, # In-game currency (default: 0)
"daily_goal": int, # Daily XP target (default: 10)
"avatar_id": int, # Current avatar (Foreign Key to Avatar)
"streak": int, # Consecutive days active (default: 0)
"last_login": datetime, # Last successful login timestamp
"created_at": datetime # Account creation timestamp
}


**Example:**
{
"user_id": 1,
"username": "allyson_t",
"password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", # hashed
"points": 0,
"xp": 150,
"glitter": 15,
"daily_goal": 10,
"avatar_id": 2,
"streak": 5,
"last_login": "2025-11-04T09:15:00",
"created_at": "2025-11-01T14:30:00"
}


---

### 1.2 Task Model

**Description:** Represents a user's task with associated rewards.

{
"task_id": int, # Unique identifier (Primary Key)
"user_id": int, # Owner (Foreign Key to User)
"title": str, # Task name (1-80 chars)
"description": str, # Full details (max 255 chars, optional)
"due_date": date, # Deadline (YYYY-MM-DD format, optional)
"completed": bool, # Completion status (0=False, 1=True)
"xp_reward": int, # XP awarded on completion (default: 10)
"priority": str, # "low", "medium", "high" (optional)
"category": str, # "academic", "cleaning", "personal", "finance", "other"
"created_at": datetime # When task was created
}


**Example:**
{
"task_id": 11,
"user_id": 1,
"title": "Finish Chemistry Homework",
"description": "Complete Chapter 7 problems 1-20",
"due_date": "2025-11-10",
"completed": False,
"xp_reward": 50,
"priority": "high",
"category": "academic",
"created_at": "2025-11-04T10:00:00"
}


---

### 1.3 Currency/Rewards Summary

**Description:** User's current currency and progression status.

{
"user_id": int,
"xp": int, # Total experience points
"glitter": int, # Spendable currency
"level": int, # Calculated from XP (XP / 100)
"streak_days": int # Consecutive login days
}

**XP to Level Calculation:**
Level = XP ÷ 100
Example: 150 XP = Level 1, 250 XP = Level 2


**XP to Glitter Conversion:**
Glitter = XP ÷ 10
Example: 50 XP = 5 Glitter


---

## 2. Authentication API (AuthController)

**Module:** `controllers/auth_controller.py`  
**Owner:** Allyson  
**Sprint:** Sprint 1, Days 2-3

---

### 2.1 `create_user()`

**Description:** Registers a new user account with hashed password.

**Function Signature:**
def create_user(username: str, password: str) -> dict

**Parameters:**
| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `username` | str | Yes | 3-40 chars, alphanumeric + underscore, unique | Display name |
| `password` | str | Yes | Min 8 chars, must include letter + number + symbol | Plain password (will be hashed) |

**Returns:**
{
"success": bool, # True if user created, False otherwise
"user_id": int, # Only present if success=True
"message": str # Success message or error details
}


**Success Example:**
result = create_user("allyson_t", "SecureP@ss123")

Returns:
{
"success": True,
"user_id": 1,
"message": "User created successfully"
}

**Error Examples:**
Username already exists
{
"success": False,
"message": "Username already exists"
}

Validation error
{
"success": False,
"message": "Password must be at least 8 characters"
}


**Validation Rules:**
- Username: 3-40 chars, alphanumeric + underscore only, must be unique
- Password: Min 8 chars, at least 1 letter, 1 number, 1 special char

---

### 2.2 `login_user()`

**Description:** Authenticates a user and returns their full profile.

**Function Signature:**
def login_user(username: str, password: str) -> dict


**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | str | Yes | Username or email |
| `password` | str | Yes | Plain password (will be verified against hash) |

**Returns:**
{
"success": bool, # True if authenticated
"user": dict, # Full User model if success=True
"message": str # Error message if success=False
}

**Success Example:**
result = login_user("allyson_t", "SecureP@ss123")

Returns:
{
"success": True,
"user": {
"user_id": 1,
"username": "allyson_t",
"xp": 150,
"glitter": 15,
"level": 1,
"streak": 5,
#... full user object
},
"message": "Login successful"
}

**Error Example:**
{
"success": False,
"message": "Invalid username or password"
}

---

### 2.3 `hash_password()`

**Description:** Hashes a plain password using SHA-256.

**Function Signature:**
def hash_password(password: str) -> str


**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `password` | str | Yes | Plain text password |

**Returns:**
- `str`: 64-character hexadecimal hash string

**Example:**
hashed = hash_password("SecureP@ss123")

Returns: "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"


**Implementation Note:** Uses `hashlib.sha256()` in Python.

---

### 2.4 `check_password()`

**Description:** Verifies if a plain password matches a stored hash.

**Function Signature:**
def check_password(username: str, password: str) -> bool

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | str | Yes | Username to check |
| `password` | str | Yes | Plain password to verify |

**Returns:**
- `bool`: True if password matches, False otherwise

**Example:**
is_valid = check_password("allyson_t", "SecureP@ss123")

Returns: True
is_valid = check_password("allyson_t", "WrongPassword")

Returns: False

---

### 2.5 `get_user()`

**Description:** Retrieves a user's full profile by user_id.

**Function Signature:**
def get_user(user_id: int) -> dict

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | int | Yes | Unique user identifier |

**Returns:**
{
"success": bool,
"user": dict, # Full User model if found
"message": str # Error message if not found
}

**Example:**
result = get_user(user_id=1)

Returns:
{
"success": True,
"user": {
"user_id": 1,
"username": "allyson_t",
# ... full user object
},
"message": "User found"
}

---

## 3. Task Management API (TaskController)

**Module:** `controllers/task_controller.py`  
**Owner:** Allyson  
**Sprint:** Sprint 1, Days 4-5

---

### 3.1 `create_task()`

**Description:** Creates a new task for a user.

**Function Signature:**
def create_task(user_id: int, task_data: dict) -> dict


**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | int | Yes | Owner of the task |
| `task_data` | dict | Yes | Task details (see structure below) |

**`task_data` Structure:**
{
"title": str, # Required, 1-80 chars
"description": str, # Optional, max 255 chars
"due_date": str, # Optional, format: "YYYY-MM-DD"
"priority": str, # Optional, "low"/"medium"/"high", default: "medium"
"category": str, # Optional, "academic"/"cleaning"/"personal"/"finance"/"other"
"xp_reward": int # Optional, calculated if not provided (10-100 based on size)
}

**Returns:**
{
"success": bool,
"task_id": int, # Only if success=True
"message": str
}

**Example:**
task_data = {
"title": "Finish Chemistry Homework",
"description": "Complete Chapter 7 problems 1-20",
"due_date": "2025-11-10",
"priority": "high",
"category": "academic",
"xp_reward": 50
}

result = create_task(user_id=1, task_data=task_data)

Returns:
{
"success": True,
"task_id": 11,
"message": "Task created successfully"
}


**Validation Rules:**
- `title`: Required, 1-80 characters
- `description`: Optional, max 255 characters
- `due_date`: Optional, must be valid date in YYYY-MM-DD format
- `priority`: Must be "low", "medium", or "high"
- `xp_reward`: If not provided, auto-calculated: small task=10 XP, medium=30 XP, large=50 XP

---

### 3.2 `get_tasks()`

**Description:** Retrieves all tasks for a user with optional filtering.

**Function Signature:**
def get_tasks(user_id: int, filter: str = "all") -> list


**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `user_id` | int | Yes | - | User whose tasks to retrieve |
| `filter` | str | No | "all" | Filter option (see below) |

**Filter Options:**
- `"all"` - All tasks (default)
- `"pending"` - Only incomplete tasks (completed=False)
- `"completed"` - Only completed tasks (completed=True)
- `"today"` - Tasks due today
- `"overdue"` - Tasks past due date
- `"academic"` - Tasks in academic category
- `"high"` - High priority tasks only

**Returns:**
- `list`: List of Task dictionaries (Full Task model for each)

**Example:**
tasks = get_tasks(user_id=1, filter="pending")

Returns:
[
{
"task_id": 11,
"title": "Finish Chemistry Homework",
"due_date": "2025-11-10",
"completed": False,
"xp_reward": 50,
# ... rest of task fields
},
{
"task_id": 12,
"title": "Clean Room",
"due_date": "2025-11-05",
"completed": False,
"xp_reward": 20,
# ... rest of task fields
}
]

---

### 3.3 `update_task()`

**Description:** Updates specific fields of an existing task.

**Function Signature:**
def update_task(task_id: int, updates: dict) -> dict

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | int | Yes | Task to update |
| `updates` | dict | Yes | Fields to change (see structure below) |

**`updates` Structure (all fields optional):**
{
"title": str, # Update title
"description": str, # Update description
"due_date": str, # Update deadline (YYYY-MM-DD)
"priority": str, # Update priority
"category": str, # Update category
"completed": bool # Mark as complete/incomplete
}

**Returns:**
{
"success": bool,
"message": str
}

**Example:**
updates = {
"priority": "high",
"due_date": "2025-11-08"
}

result = update_task(task_id=11, updates=updates)

Returns:
{
"success": True,
"message": "Task updated successfully"
}

---

### 3.4 `delete_task()`

**Description:** Permanently deletes a task.

**Function Signature:**
def delete_task(task_id: int) -> dict


**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | int | Yes | Task to delete |

**Returns:**
{
"success": bool,
"message": str
}

**Example:**
result = delete_task(task_id=11)

Returns:
{
"success": True,
"message": "Task deleted successfully"
}

---

### 3.5 `complete_task()`

**Description:** Marks a task as complete and awards XP/Glitter to the user.

**Function Signature:**
def complete_task(task_id:int) -> dict

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | int | Yes | Task to complete |

**Returns:**
{
"success": bool,
"xp_earned": int, # XP awarded for completion
"glitter_earned": int, # Glitter awarded (xp_earned / 10)
"new_xp": int, # User's total XP after award
"new_glitter": int, # User's total Glitter after award
"message": str
}

**Example:**
result = complete_task(task_id=11)

Returns:
{
"success": True,
"xp_earned": 50,
"glitter_earned": 5,
"new_xp": 200,
"new_glitter": 20,
"message": "Task completed! +50 XP, +5 Glitter"
}


**Business Logic:**
1. Mark task as completed (`completed=True`)
2. Award XP from `xp_reward` field
3. Convert XP to Glitter (divide by 10)
4. Update user's XP and Glitter totals
5. Check if user leveled up (every 100 XP = 1 level)

---

## 4. Currency Management API (CurrencyController)

**Module:** `controllers/currency_controller.py`  
**Owner:** Allyson  
**Sprint:** Sprint 1 (integrated with tasks)

---

### 4.1 `add_xp()`

**Description:** Awards XP to a user and updates level if threshold reached.

**Function Signature:**
def add_xp(user_id:int, amount:int) -> dict

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | int | Yes | User receiving XP |
| `amount` | int | Yes | XP to add (must be > 0) |

**Returns:**
{
"success": bool,
"new_xp": int, # User's total XP after addition
"new_level": int, # User's new level (calculated from XP)
"leveled_up": bool, # True if level increased
"message": str
}

**Example:**
result = add_xp(user_id=1, amount=50)

Returns (if user had 180 XP, now has 230 XP):
{
"success": True,
"new_xp": 230,
"new_level": 2, # 230 / 100 = 2
"leveled_up": True, # Went from level 1 to 2
"message": "Level up! You are now level 2"
}

---

### 4.2 `convert_xp_to_glitter()`

**Description:** Converts user's XP to Glitter currency (10 XP = 1 Glitter).

**Function Signature:**
def convert_xp_to_glitter(user_id:int) -> dict

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | int | Yes | User whose XP to convert |

**Returns:**
{
"success": bool,
"glitter_earned": int, # Amount of Glitter added
"remaining_xp": int, # XP left after conversion (< 10)
"total_glitter": int, # User's total Glitter after conversion
"message": str
}

**Example:**
User has 235 XP
result = convert_xp_to_glitter(user_id=1)

Returns:
{
"success": True,
"glitter_earned": 23, # 235 / 10 = 23
"remaining_xp": 5, # 235 % 10 = 5
"total_glitter": 50, # Previous glitter + 23
"message": "Converted 230 XP to 23 Glitter"
}


**Note:** This is typically called automatically when tasks are completed, but can be called manually.

---

### 4.3 `get_balance()`

**Description:** Retrieves user's current currency and progression status.

**Function Signature:**
def get_balance(user_id: int) -> dict


**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | int | Yes | User to check |

**Returns:**
{
"success": bool,
"xp": int,
"glitter": int,
"level": int,
"streak_days": int,
"message": str
}

**Example:**
esult = get_balance(user_id=1)

Returns:
{
"success": True,
"xp": 235,
"glitter": 50,
"level": 2,
"streak_days": 5,
"message": "Balance retrieved successfully"
}

---

### 4.4 `update_streak()`

**Description:** Checks and updates daily login streak.

**Function Signature:**
def update_streak(user_id: int) -> dict


**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | int | Yes | User to update |

**Returns:**
{
"success": bool,
"streak_days": int, # Current streak count
"bonus_xp": int, # Bonus XP awarded for streak
"message": str
}

**Example:**
result = update_streak(user_id=1)

Returns (if user logged in yesterday):
{
"success": True,
"streak_days": 6, # Streak continued
"bonus_xp": 5, # 5 XP bonus for streak
"message": "Streak continued! 6 days"
}

If user skipped a day:
{
"success": True,
"streak_days": 1, # Streak reset
"bonus_xp": 0,
"message": "Streak reset. Start a new streak today!"
}

**Business Logic:**
- If last_login was yesterday → increment streak, award bonus XP
- If last_login was today → no change
- If last_login was 2+ days ago → reset streak to 1

---

## 5. Error Handling

All API functions return consistent error structures for easy handling.

### 5.1 Standard Error Response
{
"success": False,
"message": str, # Human-readable error message
"error_code": str # Optional: Machine-readable error code
}


### 5.2 Common Error Codes

| Error Code | HTTP Equivalent | Message | When It Occurs |
|------------|-----------------|---------|----------------|
| `USER_NOT_FOUND` | 404 | "User not found" | Invalid user_id |
| `TASK_NOT_FOUND` | 404 | "Task not found" | Invalid task_id |
| `INVALID_CREDENTIALS` | 401 | "Invalid username or password" | Login failed |
| `VALIDATION_ERROR` | 400 | "Validation failed: [details]" | Invalid input format |
| `DUPLICATE_USERNAME` | 409 | "Username already exists" | create_user with existing username |
| `DATABASE_ERROR` | 500 | "Database error occurred" | SQL/database failure |
| `INSUFFICIENT_PERMISSION` | 403 | "Permission denied" | User trying to access another user's data |

### 5.3 Example Error Handling in Frontend (Xavier)
In tasks_widget.py (Xavier's code)

def on_add_task_clicked(self):
task_data = {
"title": self.title_input.text(),
"description": self.description_input.toPlainText(),
"due_date": self.date_picker.date().toString("yyyy-MM-dd"),
"priority": self.priority_dropdown.currentText()
}

result = self.task_controller.create_task(
    user_id=self.current_user_id,
    task_data=task_data
)

# Handle response
if result["success"]:
    self.show_success_popup(result["message"])
    self.refresh_task_list()
else:
    # Display error to user
    if result.get("error_code") == "VALIDATION_ERROR":
        self.show_validation_error(result["message"])
    else:
        self.show_error_popup(result["message"])

---

## 6. Frontend-Backend Communication Examples

### 6.1 Login Flow Example

**Xavier's UI Code (`ui/login_widget.py`):**
from controllers.auth_controller import AuthController

class LoginWidget:
def init(self):
self.auth_controller = AuthController()

def on_login_button_clicked(self):
    # Get input from UI
    username = self.username_input.text()
    password = self.password_input.text()
    
    # Call Allyson's backend function
    result = self.auth_controller.login_user(username, password)
    
    # Handle response
    if result["success"]:
        self.current_user = result["user"]
        self.show_dashboard()
    else:
        self.show_error_message(result["message"])

**Allyson's Controller Code (`controllers/auth_controller.py`):**

from models.user_model import UserModel
from utils.crypto import hash_password

class AuthController:
def init(self):
self.user_model = UserModel()
def login_user(self, username: str, password: str) -> dict:
    # Hash the provided password
    password_hash = hash_password(password)
    
    # Query database
    user = self.user_model.get_by_username_and_password(username, password_hash)
    
    if user:
        return {
            "success": True,
            "user": user,
            "message": "Login successful"
        }
    else:
        return {
            "success": False,
            "message": "Invalid username or password"
        }

---

### 6.2 Task Completion Flow Example

**Xavier's UI Code (`ui/tasks_widget.py`):**
from controllers.task_controller import TaskController

class TasksWidget:
def init(self):
self.task_controller = TaskController()

def on_complete_checkbox_clicked(self, task_id):
    # Call Allyson's complete_task function
    result = self.task_controller.complete_task(task_id)
    
    # Handle response
    if result["success"]:
        xp = result["xp_earned"]
        glitter = result["glitter_earned"]
        
        # Show reward popup
        self.show_reward_animation(f"+{xp} XP, +{glitter} Glitter!")
        
        # Update currency display
        self.update_xp_display(result["new_xp"])
        self.update_glitter_display(result["new_glitter"])
        
        # Refresh task list
        self.refresh_tasks()
    else:
        self.show_error(result["message"])

**Allyson's Controller Code (`controllers/task_controller.py`):**

from models.task_model import TaskModel
from models.user_model import UserModel

class TaskController:
def init(self):
self.task_model = TaskModel()
self.user_model = UserModel()
def complete_task(self, task_id: int) -> dict:
    # Get the task
    task = self.task_model.get_by_id(task_id)
    
    if not task:
        return {
            "success": False,
            "message": "Task not found",
            "error_code": "TASK_NOT_FOUND"
        }
    
    # Mark as complete
    self.task_model.update(task_id, {"completed": True})
    
    # Award XP
    xp_earned = task["xp_reward"]
    glitter_earned = xp_earned // 10
    
    # Update user currency
    user = self.user_model.get_by_id(task["user_id"])
    new_xp = user["xp"] + xp_earned
    new_glitter = user["glitter"] + glitter_earned
    
    self.user_model.update(task["user_id"], {
        "xp": new_xp,
        "glitter": new_glitter
    })
    
    return {
        "success": True,
        "xp_earned": xp_earned,
        "glitter_earned": glitter_earned,
        "new_xp": new_xp,
        "new_glitter": new_glitter,
        "message": f"Task completed! +{xp_earned} XP, +{glitter_earned} Glitter"
    }

---

## 7. Testing Guidelines

### 7.1 Allyson's Backend Tests

Create `tests/test_task_controller.py`:

import pytest
from controllers.task_controller import TaskController
from database.db_manager import DatabaseManager

def setup_test_db():
"""Create a test database with sample data"""
db = DatabaseManager(db_path='test_arcadia.db')
db.connect()
db.create_tables()
return db

def test_create_task():
"""Test creating a new task"""
controller = TaskController()
task_data = {
    "title": "Test Task",
    "description": "Test description",
    "due_date": "2025-12-01",
    "priority": "medium",
    "xp_reward": 30
}

result = controller.create_task(user_id=1, task_data=task_data)

assert result["success"] == True
assert "task_id" in result
assert result["message"] == "Task created successfully"
def test_complete_task():
"""Test completing a task and awarding XP"""
controller = TaskController()

# Create a task first
task_data = {"title": "Test Task", "xp_reward": 50}
create_result = controller.create_task(user_id=1, task_data=task_data)
task_id = create_result["task_id"]

# Complete the task
result = controller.complete_task(task_id)

assert result["success"] == True
assert result["xp_earned"] == 50
assert result["glitter_earned"] == 5
assert "new_xp" in result
assert "new_glitter" in result

**Run tests:**
pytest tests/test_task_controller.py -v

---

### 7.2 Xavier's Frontend Tests (with Dummy Data)

Create `ui/dummy_controllers.py` for testing UI without backend:

class DummyTaskController
"""Mock controller for testing UI:::

def create_task(self, user_id, task_data):
    return {
        "success": True,
        "task_id": 999,
        "message": "Task created successfully"
    }

def get_tasks(self, user_id, filter="all"):
    return [
        {
            "task_id": 1,
            "title": "Sample Task 1",
            "description": "This is a test task",
            "due_date": "2025-11-10",
            "completed": False,
            "xp_reward": 30,
            "priority": "medium"
        },
        {
            "task_id": 2,
            "title": "Sample Task 2",
            "description": "Another test task",
            "due_date": "2025-11-12",
            "completed": False,
            "xp_reward": 50,
            "priority": "high"
        }
    ]

def complete_task(self, task_id):
    return {
        "success": True,
        "xp_earned": 50,
        "glitter_earned": 5,
        "new_xp": 200,
        "new_glitter": 20,
        "message": "Task completed! +50 XP, +5 Glitter"
    }

**Use in UI code:**
In tasks_widget.py
For testing without backend:
from ui.dummy_controllers import DummyTaskController
self.task_controller = DummyTaskController()

For production with real backend:
from controllers.task_controller import TaskController
self.task_controller = TaskController()


---

## 8. Change Log

Track all changes to the API contract here.

### Version 1.0 (November 4, 2025)
- Initial contract created for Sprint 1
- Defined User and Task models
- Implemented Authentication API (5 functions)
- Implemented Task Management API (5 functions)
- Implemented Currency Management API (4 functions)
- Defined error handling standards

### Version 1.1 (TBD)
- *Future changes will be documented here*
- Example: "Added `category` filter to `get_tasks()`"
- Example: "Changed `xp_reward` calculation formula"

---

## Agreement

**This contract is agreed upon by:**

- **Allyson Taylor (Backend Developer)**: ______________________ Date: __________
- **Xavier Nixon (Frontend Developer)**: ______________________ Date: __________

**Any changes to this contract must be:**
1. Discussed in daily standup or sprint meeting
2. Documented in Change Log section
3. Agreed upon by both team members
4. Updated in this document before implementation

---





