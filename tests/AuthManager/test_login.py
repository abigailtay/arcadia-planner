import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))
from controllers.authmanager import AuthManager, AuthError

HOME = os.path.expanduser('~')
TOKEN_FILE = os.path.join(HOME, '.arcadia_token')

def save_token(token):
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)
    os.chmod(TOKEN_FILE, 0o600)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return f.read().strip()
    return None

auth = AuthManager()

token = load_token()
if token:
    use_saved = input('Saved session found. Use it? (y/n): ').lower() == 'y'
    if use_saved:
        try:
            user_id = auth.validate_token(token)
            print(f"Welcome back! You are logged in as user ID: {user_id}")
            exit()
        except AuthError as e:
            print('Saved session invalid, please log in. (', e, ')')

username = input('Username: ')
password = input('Password: ')
remember = input('Remember Me? (y/n): ').lower() == 'y'

try:
    token = auth.login(username, password, remember_me=remember)
    print("Login successful! Session token:", token)
    if remember:
        save_token(token)
        print(f"Token saved for next time at {TOKEN_FILE}")
except AuthError as e:
    print("Login failed:", e)