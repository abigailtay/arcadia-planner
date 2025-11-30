from controllers.authmanager import AuthManager
from controllers.authmanager import AuthError

def register_demo_users():
    auth = AuthManager()
    try:
        auth.register_user('alice', 'password1')
        print('Registered Alice')
    except Exception as e:
        print('Alice:', e)
    try:
        auth.register_user('bob', 'password2')
        print('Registered Bob')
    except Exception as e:
        print('Bob:', e)
    try:
        auth.register_user('carol', 'password3')
        print('Registered Carol')
    except Exception as e:
        print('Carol:', e)

if __name__ == '__main__':
    register_demo_users()
