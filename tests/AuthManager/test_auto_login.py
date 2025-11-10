import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from controllers.authmanager import AuthManager, AuthError

import os
import sqlite3

HOME = os.path.expanduser('~')
TOKEN_FILE = os.path.join(HOME, '.arcadia_token')
DB_PATH = 'arcadia.db' # Set this to your actual DB file

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return f.read().strip()
    return None

def get_username(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT username FROM user WHERE id=?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    else:
        return None

auth = AuthManager()
token = load_token()

if token:
    try:
        user_id = auth.validate_token(token)
        username = get_username(user_id)
        if username:
            print(f"Welcome back, {username}! You are logged in.")
        else:
            print(f"Welcome back! (User ID {user_id} not found)")
    except AuthError as e:
        print("Session expired or invalid:", e)
else:
    print("No saved login token. Please log in.")
