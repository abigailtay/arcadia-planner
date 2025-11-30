import re
from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout,
    QLabel, QMessageBox
)
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette
from PyQt6.QtCore import Qt

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.init_ui()

    def init_ui(self):
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email / Username")
        self.email_input.setFont(QFont("Arial", 15))
        self.email_input.textChanged.connect(self.validate_email)
        self.email_input.setMinimumHeight(38)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFont(QFont("Arial", 15))
        self.password_input.textChanged.connect(self.validate_password)
        self.password_input.setMinimumHeight(38)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #d32f2f; font-size:14px;")

        self.submit_btn = QPushButton("Log In")
        self.submit_btn.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        self.submit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_btn.clicked.connect(self.handle_login)
        self.submit_btn.setEnabled(False)
        self.submit_btn.setMinimumHeight(38)

        form = QFormLayout()
        form.addRow("Email / Username:", self.email_input)
        form.addRow("Password:", self.password_input)

        vbox = QVBoxLayout(self)
        vbox.addLayout(form)
        vbox.addWidget(self.submit_btn)
        vbox.addWidget(self.status_label)

        self.setLayout(vbox)
        self.email_valid = False
        self.password_valid = False

    def validate_email(self, text):
        valid = bool(text) and (re.match(r"[^@]+@[^@]+\.[^@]+", text) or len(text) >= 4)
        self.set_field_color(self.email_input, valid)
        self.email_valid = valid
        self.update_submit_state()
        if text and not valid:
            self.status_label.setText("Please enter a valid email or username")
        else:
            self.status_label.setText("")

    def validate_password(self, text):
        valid = bool(text) and len(text) >= 4
        self.set_field_color(self.password_input, valid)
        self.password_valid = valid
        self.update_submit_state()
        if text and not valid:
            self.status_label.setText("Password must be at least 4 characters")
        elif self.email_valid:
            self.status_label.setText("")

    def set_field_color(self, field, valid):
        if not field.text():
            field.setStyleSheet("")
        elif valid:
            field.setStyleSheet("border:2px solid #5bbe5b;")
        else:
            field.setStyleSheet("border:2px solid #d32f2f;")

    def update_submit_state(self):
        self.submit_btn.setEnabled(self.email_valid and self.password_valid)

    def handle_login(self):
        # Mock API: Accept 'demo@arcadia.com' + '1234'
        email = self.email_input.text()
        password = self.password_input.text()
        if (email == "demo@arcadia.com" or email == "demo") and password == "1234":
            self.status_label.setStyleSheet("color: #5bbe5b; font-size:14px;")
            self.status_label.setText("Login successful!")
        else:
            self.status_label.setStyleSheet("color: #d32f2f; font-size:14px;")
            self.status_label.setText("Invalid credentials. Try again.")
            QMessageBox.critical(self, "Login Failed", "Invalid credentials.")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = LoginForm()
    win.resize(340, 200)
    win.show()
    sys.exit(app.exec())
