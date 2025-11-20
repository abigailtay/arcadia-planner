"""
File: studysessionmodel.py
Author: Allyson Taylor
Date: 2025-11-20
Description:
    Model for StudySession handling database interaction,
    session logging, streak calculation, XP and glitter awarding.
"""


import sqlite3
from datetime import datetime, timedelta


DB_PATH = "arcadia.db"


class StudySessionModel:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()


    def log_session(self, user_id:int, start_time:str, end_time:str, pomodoro_setting:str) -> bool:
        """Log a study session for a user with pomodoro timer setting."""
        duration = self._calculate_duration(start_time, end_time)
        streak = self._calculate_streak(user_id, end_time)
        xp_earned = self._calculate_xp(duration, streak)


        try:
            self.cursor.execute("""
                INSERT INTO study_sessions (userId, startTime, endTime, duration, streakTimer, xpEarned, pomodoroSetting)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, start_time, end_time, duration, streak, xp_earned, pomodoro_setting))
            self.conn.commit()
            self._update_user_rewards(user_id, xp_earned)
            return True
        except Exception as e:
            print(f"Error logging session: {e}")
            return False


    def _calculate_duration(self, start_time:str, end_time:str) -> int:
        fmt = "%Y-%m-%d %H:%M:%S"
        st = datetime.strptime(start_time, fmt)
        et = datetime.strptime(end_time, fmt)
        return int((et - st).total_seconds() // 60)


    def _calculate_streak(self, user_id:int, current_end_time:str) -> int:
        """Calculate the streakTimer (0-5) based on last sessions."""
        fmt = "%Y-%m-%d %H:%M:%S"
        current_time = datetime.strptime(current_end_time, fmt)


        self.cursor.execute("""
            SELECT endTime, streakTimer FROM study_sessions
            WHERE userId = ?
            ORDER BY endTime DESC LIMIT 1
        """, (user_id,))
        row = self.cursor.fetchone()


        if row:
            last_end_time = datetime.strptime(row['endTime'], fmt)
            last_streak = row['streakTimer']
            diff = current_time - last_end_time
            
            # Define max gap between sessions (e.g. 1 day)
            if diff <= timedelta(days=1) and last_streak < 5:
                return last_streak + 1
            else:
                return 1
        else:
            return 1


    def _calculate_xp(self, duration:int, streak:int) -> int:
        base_xp = duration // 25 * 10
        streak_bonus = streak * 5
        return base_xp + streak_bonus


    def _update_user_rewards(self, user_id:int, xp:int):
        """Update user's XP and glitter currency based on session."""
        # Glitter awarded every streak of 5
        glitter_reward = 10 if xp >= 50 else 0


        upd_xp = "UPDATE user SET xp = xp + ? WHERE userId = ?"
        self.cursor.execute(upd_xp, (xp, user_id))
        if glitter_reward > 0:
            upd_glitter = "UPDATE user SET glitter = glitter + ? WHERE userId = ?"
            self.cursor.execute(upd_glitter, (glitter_reward, user_id))
        self.conn.commit()


    def close(self):
        self.conn.close()
