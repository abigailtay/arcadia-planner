"""
File: E-7.py
Author: Allyson Taylor
Date: 2024-06-10
Description:
    Backend test for StudySessionModel session time validation.
    Verifies that sessions <5 min or reversed times are blocked.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.studysessionmodel import StudySessionModel
from datetime import datetime, timedelta

@pytest.fixture
def model():
    return StudySessionModel()

def iso(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def test_session_too_short(model):
    start = datetime(2024, 6, 10, 14, 0, 0)
    end = start + timedelta(minutes=4)
    result = model.log_session(
        user_id=1,
        start_time=iso(start),
        end_time=iso(end),
        pomodoro_setting="Pomodoro"
    )
    assert result is False

def test_session_reversed(model):
    start = datetime(2024, 6, 10, 14, 0, 0)
    end = start - timedelta(minutes=10)
    result = model.log_session(
        user_id=1,
        start_time=iso(start),
        end_time=iso(end),
        pomodoro_setting="Pomodoro"
    )
    assert result is False

def test_session_valid(model):
    start = datetime(2024, 6, 10, 14, 0, 0)
    end = start + timedelta(minutes=25)
    result = model.log_session(
        user_id=1,
        start_time=iso(start),
        end_time=iso(end),
        pomodoro_setting="Pomodoro"
    )
    assert result is True
    model.close()
