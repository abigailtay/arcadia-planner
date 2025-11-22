"""
File: E-8.py
Author: Allyson Taylor
Date: 2025-11-22
Description:
    Backend tests for PomodoroModel config validation.
    Verifies timer cannot run or log a session with unsupported config; error is returned.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.pomodoromodel import PomodoroModel
from datetime import datetime, timedelta

@pytest.fixture
def model():
    return PomodoroModel()

def iso(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def test_invalid_config(model):
    # Unsupported config should block session creation
    start = datetime(2025, 11, 22, 18, 0, 0)
    end = start + timedelta(minutes=25)
    result = model.log_study_session(
        user_id=1,
        start_time=iso(start),
        end_time=iso(end),
        config="20/5"  # Not allowed
    )
    assert not result["success"]
    assert "invalid config" in result["error"].lower()

def test_supported_config(model):
    # Allowed config works as expected
    start = datetime(2025, 11, 22, 18, 0, 0)
    end = start + timedelta(minutes=25)
    result = model.log_study_session(
        user_id=1,
        start_time=iso(start),
        end_time=iso(end),
        config="25/5"
    )
    assert result["success"]

def test_wrong_duration_config(model):
    # Duration does not match config window (should trigger error)
    start = datetime(2025, 11, 22, 18, 0, 0)
    end = start + timedelta(minutes=15)
    result = model.log_study_session(
        user_id=1,
        start_time=iso(start),
        end_time=iso(end),
        config="25/5"
    )
    assert not result["success"]
    assert "duration" in result["error"].lower()
