import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from controllers.authmanager import AuthManager, AuthError

HOME = os.path.expanduser('~')
TOKEN_FILE = os.path.join(HOME, '.arcadia_token')

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return f.read().strip()
    return None

def delete_token():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print("Token file deleted.")

auth = AuthManager()
token = load_token()
if token:
    try:
        auth.logout(token)
        print("Logged out successfully!")
        delete_token()
    except AuthError as e:
        print("Logout failed:", e)
else:
    print("No token found. Already logged out?")
