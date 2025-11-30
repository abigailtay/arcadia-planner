# File: tests/Backend/B-28.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for logging study sessions and XP, with full test DB cleanup.
#   Verifies: Valid session logs row and XP, invalid session rejected.
#   Test Case: B-28 log_study_session

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import sqlite3
from datetime import datetime, timedelta
from models.studysessionmodel import StudySessionModel

def test_log_study_session():
    model = StudySessionModel()
    db_path = "arcadia.db"
    # Use a unique test-only user for this test
    user_id = 13337
    username = "pytestuser_13337"
    password = "pw"
    # Clean up previous test user and sessions (precaution)
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("DELETE FROM study_sessions WHERE userId=?", (user_id,))
        c.execute("DELETE FROM user WHERE userId=?", (user_id,))
        db.commit()

    # Create test user
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute(
            "INSERT INTO user (userId, username, password, xp, glitter) VALUES (?, ?, ?, 0, 0)",
            (user_id, username, password)
        )
        db.commit()

    # Use now as reference time
    now = datetime.now()
    start_time = (now - timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")
    end_time = now.strftime("%Y-%m-%d %H:%M:%S")
    pomodoro_setting = "25/5 classic"

    # Save XP before
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT xp FROM user WHERE userId=?", (user_id,))
        row = c.fetchone()
        xp_before = row[0] if row else 0

    # Valid session logs
    ok = model.log_session(user_id, start_time, end_time, pomodoro_setting)
    assert ok is True

    # Check session row
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT duration, xpEarned FROM study_sessions WHERE userId=? AND startTime=?", (user_id, start_time))
        row = c.fetchone()
        assert row is not None
        duration, xp_earned = row
        assert duration > 0
        assert xp_earned > 0

    # Check XP is incremented for user
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("SELECT xp FROM user WHERE userId=?", (user_id,))
        row2 = c.fetchone()
        xp_after = row2[0] if row2 else 0
        assert xp_after >= xp_before + xp_earned

    # Invalid (missing) session log (should return False)
    bad_cases = [
        (None, start_time, end_time, pomodoro_setting),
        (user_id, None, end_time, pomodoro_setting),
        (user_id, start_time, None, pomodoro_setting),
        (user_id, start_time, end_time, None),
    ]
    for args in bad_cases:
        try:
            result = model.log_session(*args)
        except Exception:
            result = False
        assert not result

    # Final cleanup: remove test user and any of its sessions
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute("DELETE FROM study_sessions WHERE userId=?", (user_id,))
        c.execute("DELETE FROM user WHERE userId=?", (user_id,))
        db.commit()
