"""
File: test_pomodoromodel.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    Tests for Pomodoro streak and timer backend logic verifying:
    - Various allowed timer configurations
    - Streak increments only on valid sessions
    - Rejection of invalid configs or durations
    Includes instructions for screenshot captures.
"""

import sys
import os
import pytest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from models.pomodoromodel import PomodoroModel
import sqlite3

DB_PATH = "arcadia.db"

@pytest.fixture(scope="module")
def pomodoro_model():
    model = PomodoroModel()
    yield model
    model.close()

def ensure_user_exists(user_id=1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT userId FROM user WHERE userId=?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO user (username, password, xp, glitter, streak) VALUES (?, ?, 0, 0, 0)", ('testuser', 'password123'))
        conn.commit()
    conn.close()

def test_valid_configs_and_streak_increment(pomodoro_model):
    user_id = 1
    ensure_user_exists(user_id)
    base_time = datetime.now()

    # Test all valid configurations with proper session duration
    for config in ['25/5', '30/5', '45/10']:
        start_time = (base_time - timedelta(minutes=int(config.split('/')[0]))).strftime("%Y-%m-%d %H:%M:%S")
        end_time = base_time.strftime("%Y-%m-%d %H:%M:%S")
        result = pomodoro_model.log_study_session(user_id, start_time, end_time, config)
        assert result is True

    # The streak should now be 3 (after three valid sessions)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT streak FROM user WHERE userId=?", (user_id,))
    streak = cursor.fetchone()[0]
    conn.close()
    assert streak == 3

def test_invalid_config_rejected(pomodoro_model):
    user_id = 1
    base_time = datetime.now()
    start_time = (base_time - timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S")
    end_time = base_time.strftime("%Y-%m-%d %H:%M:%S")
    assert not pomodoro_model.log_study_session(user_id, start_time, end_time, "15/5")

def test_invalid_duration_rejected(pomodoro_model):
    user_id = 1
    base_time = datetime.now()
    # Pass duration much shorter than allowed 25 minutes
    start_time = (base_time - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
    end_time = base_time.strftime("%Y-%m-%d %H:%M:%S")
    assert not pomodoro_model.log_study_session(user_id, start_time, end_time, "25/5")

def test_streak_reset_after_timeout(pomodoro_model):
    user_id = 1
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Manually reset streak to 1 and last session time to 3 days ago
    old_time = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE user SET streak = 1 WHERE userId=?", (user_id,))
    cursor.execute("INSERT INTO study_sessions (userId, startTime, endTime, duration, streakTimer, xpEarned, pomodoroSetting) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (user_id, old_time, old_time, 25, 1, 10, "25/5"))
    conn.commit()
    conn.close()

    # Attempt logging a valid 25/5 session now, streak should reset to 1
    base_time = datetime.now()
    start_time = (base_time - timedelta(minutes=25)).strftime("%Y-%m-%d %H:%M:%S")
    end_time = base_time.strftime("%Y-%m-%d %H:%M:%S")
    result = pomodoro_model.log_study_session(user_id, start_time, end_time, "25/5")
    assert result is True

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT streak FROM user WHERE userId=?", (user_id,))
    streak = cursor.fetchone()[0]
    conn.close()
    # Streak reset to 1 because last session too old
    assert streak == 1

    # Instruction for demo (meeting)
    print("Pytest completed: Pomodoro streak edge cases tested successfully.")
    print("Instruction: Capture this output screenshot with all tests passing.")
