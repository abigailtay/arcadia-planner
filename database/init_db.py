"""
Database Initialization Script for Arcadia Planner
Author: Allyson Taylor
Purpose: Initialize database and create all required tables
Last Modified: November 5, 2025
"""

from .db_manager import DatabaseManager
import sys


def initialize_database():
    """
    Initialize the Arcadia Planner database.
    Creates database file and all required tables.
    """
    print("\n" + "="*70)
    print(" " * 15 + "ARCADIA PLANNER DATABASE INITIALIZATION")
    print("="*70 + "\n")
    
    # Create database manager instance
    db = DatabaseManager('arcadia.db')
    
    # Step 1: Connect to database
    print("Step 1: Connecting to database...")
    if not db.connect():
        print("✗ Failed to connect to database. Exiting.")
        sys.exit(1)
    
    # Step 2: Create all tables
    print("\nStep 2: Creating database tables...")
    if not db.create_tables():
        print("✗ Failed to create tables. Exiting.")
        db.disconnect()
        sys.exit(1)
    
    # Step 3: Verify tables were created
    print("Step 3: Verifying table creation...")
    if not db.verify_tables():
        print("✗ Table verification failed. Exiting.")
        db.disconnect()
        sys.exit(1)
    
    # Step 4: Display table schemas
    print("\nStep 4: Displaying table schemas...")
    db.get_table_info('users')
    db.get_table_info('tasks')
    db.get_table_info('user_currency')
    
    # Step 5: Disconnect
    print("\nStep 5: Closing database connection...")
    db.disconnect()
    
    print("\n" + "="*70)
    print(" " * 20 + "DATABASE INITIALIZATION COMPLETE!")
    print("="*70 + "\n")
    print("✓ Database file created: arcadia.db")
    print("✓ All tables created successfully")
    print("✓ You can now implement the AuthManager\n")


if __name__ == "__main__":
    initialize_database()
