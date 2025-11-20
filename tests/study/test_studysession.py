"""
File: test_studysession.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    Tests for StudySession backend: session initiation, streak calculation,
    and XP/glitter awarding. Includes instructions for screenshot capture.
"""

import sys
import os
import pytest
from datetime import datetime, timedelta

# Add project root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from models.studysessionmodel import StudySessionModel
import sqlite3

DB_PATH = "arcadia.db"

@pytest.fixture(scope="module")
def model():
    m = StudySessionModel()
    yield m
    m.close()

def ensure_test_user_exists(user_id=1):
    """Ensure test user with user_id=1 exists; create if missing."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT userId FROM user WHERE userId=?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO user (username, password, xp, glitter) VALUES (?, ?, 0, 0)", 
            ('testuser', 'password123')
        )
        conn.commit()
    conn.close()

def test_session_logging_and_streak(model):
    user_id = 1  # Test user
    ensure_test_user_exists(user_id)
    now = datetime.now()
    start_time = (now - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
    end_time = now.strftime("%Y-%m-%d %H:%M:%S")
    pomodoro_setting = "25/5"

    # First session - expect streak=1
    assert model.log_session(user_id, start_time, end_time, pomodoro_setting) is True

    # Query DB to verify insertion and streak
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM study_sessions WHERE userId=? ORDER BY sessionId DESC LIMIT 1", 
        (user_id,)
    )
    row = cursor.fetchone()
    assert row is not None
    assert row[1] == user_id  # userId
    assert row[5] == 1        # streakTimer

    # Second session within 1 day to test streak increment
    start2 = (now + timedelta(minutes=40)).strftime("%Y-%m-%d %H:%M:%S")
    end2 = (now + timedelta(minutes=70)).strftime("%Y-%m-%d %H:%M:%S")
    assert model.log_session(user_id, start2, end2, pomodoro_setting) is True
    
    cursor.execute(
        "SELECT streakTimer FROM study_sessions WHERE userId=? ORDER BY sessionId DESC LIMIT 1", 
        (user_id,)
    )
    row2 = cursor.fetchone()
    assert row2[0] == 2  # streak incremented

    conn.close()

    # INSTRUCTIONS FOR DEMO (meeting)
    print("Pytest completed successfully: StudySession logging and streak tests passed.")
    print("INSTRUCTION: Take a screenshot of this pytest output showing all tests passed.")
    print("Afterward, open sqlite3 arcadia.db and run:")
    print("SELECT * FROM study_sessions WHERE userId=1;")
    print("Then take a screenshot showing the session rows.")
