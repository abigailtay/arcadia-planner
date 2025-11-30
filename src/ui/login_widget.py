import sys
import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import QTimer, Qt

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.username_valid = False
        self.password_valid = False
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or Email")
        self.username_input.textChanged.connect(self.validate_email_username)
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.textChanged.connect(self.validate_password)
        layout.addWidget(self.password_input)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.login_button = QPushButton("Login")
        self.login_button.setEnabled(False)
        self.login_button.clicked.connect(self._handle_login)
        layout.addWidget(self.login_button)

    def validate_email_username(self, text):
        # Fixed regex
        valid = bool(text) and (re.match(r"[^@]+@[^@]+\.[^@]+", text) or len(text) >= 4)
        self.username_valid = valid
        self.update_submit_state()

    def validate_password(self, text):
        valid = bool(text) and len(text) >= 4
        self.password_valid = valid
        self.update_submit_state()

    def update_submit_state(self):
        self.login_button.setEnabled(self.username_valid and self.password_valid)

    def _handle_login(self):
        print("Login button pressed")
        username = self.username_input.text().strip()
        password = self.password_input.text()
        self.login_button.setText("Logging in...")
        self.login_button.setEnabled(False)
        QTimer.singleShot(1000, lambda: self._check_login(username, password))

    def _check_login(self, username, password):
        print("Checking login for:", username, password)
        if (username == "demo" or username == "demo@arcadia.com") and password == "1234":
            self.status_label.setText("Login successful!")
        else:
            self.status_label.setText("Invalid credentials. Try again.")
            QMessageBox.critical(self, "Login Failed", "Invalid credentials. Try again.")
        self.login_button.setText("Login")
        self.login_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = LoginWidget()
    w.resize(400, 200)
    w.show()
    sys.exit(app.exec())
