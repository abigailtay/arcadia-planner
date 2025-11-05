"""
Database Manager for Arcadia Planner
Author: Allyson Taylor
Purpose: Handles SQLite database connection and table creation
Last Modified: November 5, 2025
"""

import sqlite3
from pathlib import Path
from datetime import datetime


class DatabaseManager:
    """Manages SQLite database connections and operations for Arcadia Planner"""
    
    def __init__(self, db_path='arcadia.db'):
        """
        Initialize database manager with specified database path.
        
        Parameters:
            db_path (str): Path to SQLite database file (default: 'arcadia.db')
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """
        Establish connection to SQLite database.
        Creates database file if it doesn't exist.
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Allows dict-like access to rows
            self.cursor = self.connection.cursor()
            print(f"✓ Connected to database: {self.db_path}")
            return self.connection
        except sqlite3.Error as e:
            print(f"✗ Error connecting to database: {e}")
            return None
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")
    
    def create_tables(self):
        """
        Create all required tables for Arcadia Planner.
        Tables: users, tasks, user_currency
        """
        if not self.connection:
            print("✗ Error: No database connection. Call connect() first.")
            return False
        
        try:
            # ============================================
            # TABLE 1: USERS
            # ============================================
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
            
            # ============================================
            # TABLE 2: TASKS
            # ============================================
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
            
            # Create index on user_id for faster queries
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_tasks_user_id 
                ON tasks(user_id)
            ''')
            print("✓ Created index: idx_tasks_user_id")
            
            # Create index on completed for filtering
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_tasks_completed 
                ON tasks(completed)
            ''')
            print("✓ Created index: idx_tasks_completed")
            
            # ============================================
            # TABLE 3: USER_CURRENCY (for easier querying)
            # ============================================
            # Note: This is technically redundant with users table,
            # but it makes currency queries cleaner
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
            
            # Commit all changes
            self.connection.commit()
            print("\n✓✓✓ ALL TABLES CREATED SUCCESSFULLY ✓✓✓\n")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Error creating tables: {e}")
            return False
    
    def verify_tables(self):
        """
        Verify that all required tables exist in the database.
        
        Returns:
            bool: True if all tables exist, False otherwise
        """
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
        """
        Display schema information for a specific table.
        
        Parameters:
            table_name (str): Name of the table to inspect
        """
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
        """
        WARNING: Drops all tables from the database.
        Use only for testing/reset purposes.
        """
        try:
            tables = ['user_currency', 'tasks', 'users']  # Order matters (foreign keys)
            
            for table in tables:
                self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"✓ Dropped table: {table}")
            
            self.connection.commit()
            print("\n✓ All tables dropped successfully")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Error dropping tables: {e}")
            return False


# ============================================
# TESTING FUNCTIONS
# ============================================

def test_database_setup():
    """Test function to verify database setup works correctly"""
    print("\n" + "="*60)
    print("TESTING DATABASE SETUP")
    print("="*60 + "\n")
    
    # Create database manager
    db = DatabaseManager('arcadia.db')
    
    # Connect to database
    db.connect()
    
    # Create tables
    db.create_tables()
    
    # Verify tables exist
    db.verify_tables()
    
    # Show table schemas
    db.get_table_info('users')
    db.get_table_info('tasks')
    db.get_table_info('user_currency')
    
    # Disconnect
    db.disconnect()
    
    print("\n" + "="*60)
    print("DATABASE SETUP TEST COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Run test when file is executed directly
    test_database_setup()
