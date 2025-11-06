import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.controllers.auth_manager import AuthManager

auth = AuthManager()
print("Register user:", auth.create_user("demouser1", "TestPass123!"))
print("Register invalid user:", auth.create_user("bad!user", "abc"))
print("Login with correct password:", auth.login_user("demouser1", "TestPass123!"))
print("Login with wrong password:", auth.login_user("demouser1", "nope"))
print("Logout:", auth.logout_user())
