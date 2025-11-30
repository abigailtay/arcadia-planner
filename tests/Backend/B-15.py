# File: tests/Backend/B-15.py
# Author: Allyson taylor
# Date: 2025-11-22
# Description:
#   Backend unit test for habit color shade validation.
#   Verifies: ColorShade outside allowed range rejected, error recorded.
#   Test Case: B-15 create_habit: invalid color shade

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from models.habitmodel import HabitModel

def test_create_habit_invalid_color_shade():
    habit_model = HabitModel()
    user_id = 1  # must exist
    # Only values that are NOT None and incorrect types/range will error
    invalid_colors = [-1, 11, 100, -10, "blue", 1.5]
    for bad_color in invalid_colors:
        with pytest.raises(ValueError):
            habit_model.create_habit(
                user_id=user_id,
                habit_name="pytest B-15",
                color_shade=bad_color
            )
