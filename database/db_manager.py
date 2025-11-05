"""
Database Manager for Arcadia Planner
Author: Allyson Taylor
Purpose: Handles SQLite database connection and table creation
Last Modified: November 5, 2025
"""

import sqlite3
from datetime import datetime

class DatabaseManager:
    """Manages SQLite database connections and operations for Arcadia Planner"""
    def __init__(self, db_path='arcadia.db'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Dict-style results
            self.cursor = self.connection.cursor()
            print(f"✓ Connected to database: {self.db_path}")
            return self.connection
        except sqlite3.Error as e:
            print(f"✗ Error connecting to database: {e}")
            return None

    def disconnect(self):
        if self.connection:
            try:
                self.connection.close()
                print("✓ Database connection closed")
            except Exception as e:
                print(f"✗ Error closing DB: {e}")

    def create_tables(self):
        if not self.connection:
            print("✗ Error: No database connection. Call connect() first.")
            return False
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(40) UNIQUE NOT NULL,
                    password VARCHAR(64) NOT NULL,
                    points INTEGER DEFAULT 0,
                    xp INTEGER DEFAULT 0,
                    glitter INTEGER DEFAULT 0,
                    daily_goal INTEGER DEFAULT 10,
                    avatar_id INTEGER DEFAULT 1,
                    streak INTEGER DEFAULT 0,
                    last_login DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✓ Created table: users")

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title VARCHAR(80) NOT NULL,
                    description VARCHAR(255),
                    due_date DATE,
                    completed BOOLEAN DEFAULT 0,
                    xp_reward INTEGER DEFAULT 10,
                    priority VARCHAR(10),
                    category VARCHAR(30),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            print("✓ Created table: tasks")

            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_tasks_user_id 
                ON tasks(user_id)
            ''')
            print("✓ Created index: idx_tasks_user_id")

            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_tasks_completed 
                ON tasks(completed)
            ''')
            print("✓ Created index: idx_tasks_completed")

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_currency (
                    user_id INTEGER PRIMARY KEY,
                    xp INTEGER DEFAULT 0,
                    glitter INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    streak_days INTEGER DEFAULT 0,
                    last_login DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            print("✓ Created table: user_currency")

            self.connection.commit()
            print("\n✓✓✓ ALL TABLES CREATED SUCCESSFULLY ✓✓✓\n")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error creating tables: {e}")
            return False

    def verify_tables(self):
        try:
            required_tables = ['users', 'tasks', 'user_currency']
            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                ORDER BY name
            """)
            existing_tables = [row[0] for row in self.cursor.fetchall()]
            print("\n=== DATABASE VERIFICATION ===")
            print(f"Required tables: {required_tables}")
            print(f"Existing tables: {existing_tables}")
            all_exist = all(table in existing_tables for table in required_tables)
            if all_exist:
                print("✓ All required tables exist!")
                return True
            else:
                missing = [t for t in required_tables if t not in existing_tables]
                print(f"✗ Missing tables: {missing}")
                return False
        except sqlite3.Error as e:
            print(f"✗ Error verifying tables: {e}")
            return False

    def get_table_info(self, table_name):
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()
            print(f"\n=== TABLE: {table_name.upper()} ===")
            print(f"{'Column':<20} {'Type':<15} {'Not Null':<10} {'Default':<15}")
            print("-" * 60)
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                not_null = "YES" if col[3] else "NO"
                default = col[4] if col[4] else "None"
                print(f"{col_name:<20} {col_type:<15} {not_null:<10} {default:<15}")
            print("-" * 60)
        except sqlite3.Error as e:
            print(f"✗ Error getting table info: {e}")

    def drop_all_tables(self):
        try:
            tables = ['user_currency', 'tasks', 'users']  # for FK order
            for table in tables:
                self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"✓ Dropped table: {table}")
            self.connection.commit()
            print("\n✓ All tables dropped successfully")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error dropping tables: {e}")
            return False

    # === Error-handled user ops ===
    def insert_user(self, username, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            self.connection.commit()
            return {"success": True, "user_id": self.cursor.lastrowid}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def fetch_all_users(self):
        try:
            self.cursor.execute("SELECT user_id, username FROM users")
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"✗ Error fetching users: {e}")
            return []

# === Script testing block ===
def test_database_setup():
    print("\n" + "="*60)
    print("TESTING DATABASE SETUP")
    print("="*60 + "\n")
    db = DatabaseManager('arcadia.db')
    db.connect()
    db.create_tables()
    db.verify_tables()
    db.get_table_info('users')
    db.get_table_info('tasks')
    db.get_table_info('user_currency')
    db.disconnect()
    print("\n" + "="*60)
    print("DATABASE SETUP TEST COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_database_setup()
    # Insert and list a sample user
    db = DatabaseManager('arcadia.db')
    db.connect()
    res = db.insert_user("sampleuser", "securepassword123")
    print("Sample user insert:", res)
    users = db.fetch_all_users()
    print("All users:", users)
    db.disconnect()
