# Database Schema: Arcadia Planner

## users
- user_id: INTEGER PRIMARY KEY AUTOINCREMENT
- username: VARCHAR(40), UNIQUE, NOT NULL
- password: VARCHAR(64), NOT NULL
- points: INTEGER DEFAULT 0
- xp: INTEGER DEFAULT 0
- glitter: INTEGER DEFAULT 0
- daily_goal: INTEGER DEFAULT 10
- avatar_id: INTEGER DEFAULT 1
- streak: INTEGER DEFAULT 0
- last_login: DATETIME, nullable
- created_at: DATETIME DEFAULT CURRENT_TIMESTAMP

## tasks
- task_id: INTEGER PRIMARY KEY AUTOINCREMENT
- user_id: INTEGER, NOT NULL, FOREIGN KEY
- title: VARCHAR(80), NOT NULL
- description: VARCHAR(255), nullable
- due_date: DATE, nullable
- completed: BOOLEAN DEFAULT 0
- xp_reward: INTEGER DEFAULT 10
- priority: VARCHAR(10), nullable
- category: VARCHAR(30), nullable
- created_at: DATETIME DEFAULT CURRENT_TIMESTAMP

## user_currency
- user_id: INTEGER PRIMARY KEY, FOREIGN KEY
- xp: INTEGER DEFAULT 0
- glitter: INTEGER DEFAULT 0
- level: INTEGER DEFAULT 1
- streak_days: INTEGER DEFAULT 0
- last_login: DATETIME, nullable

## Indexes
- idx_tasks_user_id ON tasks(user_id)
- idx_tasks_completed ON tasks(completed)
