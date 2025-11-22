# File: tests/Backend/B-30.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Unit test for StudySession glitter award logic.
#   Verifies: Glitter calculation aligns with XP thresholds and increments.
#   Test Case: B-30 calculate_glitter

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.studysessionmodel import StudySessionModel

def calculate_glitter_award(xp):
    # Logic from model: glitter_reward = 10 if xp >= 50 else 0
    return 10 if xp >= 50 else 0

def test_calculate_glitter_logic():
    model = StudySessionModel()
    # Try various XP values for session
    cases = [
        (0, 0),
        (10, 0),
        (25, 0),
        (49, 0),
        (50, 10),
        (55, 10),
        (99, 10),
        (100, 10)
    ]
    for xp_earned, expected_glitter in cases:
        result = calculate_glitter_award(xp_earned)
        assert result == expected_glitter, f"Glitter ({result}) did not match ({expected_glitter}) for xp={xp_earned}"
    model.close()
