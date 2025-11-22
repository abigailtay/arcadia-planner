# File: tests/Backend/B-29.py
# Author: Allyson Taylor
# Date: 2025-11-22
# Description:
#   Unit test for StudySession XP calculation logic.
#   Verifies: XP logic returns correct XP for a range of durations and streaks.
#   Test Case: B-29 calculate_xp

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.studysessionmodel import StudySessionModel

def test_calculate_xp_logic():
    model = StudySessionModel()
    cases = [
        # (duration_minutes, streak, expected_xp)
        (25, 1, 10+5),               # 1x pom, streak 1
        (60, 2, 20+10),              # 2x poms, streak 2
        (50, 3, 20+15),
        (0, 4, 0+20),                # 0min, streak 4 (should get bonus, but no base)
        (100, 5, 40+25),
        (37, 2, 10+10),              # 37min => 1x 25min = 10 base
        (120, 4, 40+20),             # 4x poms, streak 4
        (12, 3, 0+15),               # <1 pom, streak 3
        (26, 5, 10+25),              # Just over 1 pom
    ]
    for duration, streak, expected in cases:
        result = model._calculate_xp(duration, streak)
        assert result == expected, f"XP ({result}) did not match ({expected}) for duration={duration}, streak={streak}"

    # Clean up model connection
    model.close()
