"""
File: pomodoromodel.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    Core Pomodoro streak and timer backend logic,
    supporting various timer configurations (25/5, 30/5, 45/10).
    Includes streak validation and eligibility checks.
"""

import sqlite3
from datetime import datetime, timedelta

DB_PATH = "arcadia.db"
ALLOWED_CONFIGS = {
    "25/5": (25, 5),
    "30/5": (30, 5),
    "45/10": (45, 10)
}
MAX_STREAK = 5

class PomodoroModel:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def is_valid_config(self, config: str) -> bool:
        return config in ALLOWED_CONFIGS

    def log_study_session(self, user_id: int, start_time: str, end_time: str, config: str) -> dict:
        if not self.is_valid_config(config):
            return {"success": False, "error": "Invalid config"}

        work_len, break_len = ALLOWED_CONFIGS[config]
        fmt = "%Y-%m-%d %H:%M:%S"
        st = datetime.strptime(start_time, fmt)
        et = datetime.strptime(end_time, fmt)
        duration = (et - st).total_seconds() / 60

        if not (work_len - 1 <= duration <= work_len + 1):
            return {"success": False, "error": "Session duration does not match timer"}

        with self._get_conn() as conn:
            cursor = conn.cursor()
            last_streak = self._get_last_streak(cursor, user_id)
            if self._session_valid_for_streak(cursor, user_id, et):
                new_streak = min(last_streak + 1, MAX_STREAK)
            else:
                new_streak = 1

            self._update_user_streak(cursor, user_id, new_streak)
            if new_streak == MAX_STREAK:
                self._award_glitter(cursor, user_id, 10)

            xp_earned = (work_len // 25) * 10 + new_streak * 5

            try:
                cursor.execute("""
                    INSERT INTO study_sessions (userId, startTime, endTime, duration, streakTimer, xpEarned, pomodoroSetting)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, start_time, end_time, int(duration), new_streak, xp_earned, config))
                conn.commit()
                return {"success": True, "streak": new_streak, "xp": xp_earned}
            except Exception as e:
                return {"success": False, "error": f"Error logging pomodoro session: {e}"}

    def _get_last_streak(self, cursor, user_id: int) -> int:
        cursor.execute("""
            SELECT streakTimer, endTime FROM study_sessions
            WHERE userId = ? ORDER BY endTime DESC LIMIT 1
        """, (user_id,))
        row = cursor.fetchone()
        if row:
            return row['streakTimer'] or 0
        return 0

    def _session_valid_for_streak(self, cursor, user_id: int, new_end_time: datetime) -> bool:
        cursor.execute("""
            SELECT endTime FROM study_sessions
            WHERE userId = ? ORDER BY endTime DESC LIMIT 1
        """, (user_id,))
        row = cursor.fetchone()
        if not row:
            return True
        last_end_time = datetime.strptime(row['endTime'], "%Y-%m-%d %H:%M:%S")
        diff = new_end_time - last_end_time
        return diff <= timedelta(days=1)

    def _update_user_streak(self, cursor, user_id: int, streak: int):
        cursor.execute("UPDATE user SET streak = ? WHERE userId = ?", (streak, user_id))

    def _award_glitter(self, cursor, user_id: int, amount: int):
        cursor.execute("UPDATE user SET glitter = glitter + ? WHERE userId = ?", (amount, user_id))
