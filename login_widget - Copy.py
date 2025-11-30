from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # Outer background (stretch and center everything)
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QWidget {
                background: #fae2f7;
            }
            #arcadiaCard {
                background: #fff;
                border-radius: 32px;
                border: 3px solid #e0b5db;
                box-shadow: 0 12px 48px 0 #95506322;
            }
            QLabel {
                color: #22172e;
                font-size: 19px;
                font-family: Arial, Verdana, sans-serif;
                font-weight: 600;
            }
            QLineEdit {
                background: #fff;
                border: 3px solid #e3b6e9;
                border-radius: 27px;
                color: #22172e;
                font-size: 18px;
                padding-left: 22px;
                margin-bottom: 18px;
                outline: none;
                font-family: Arial, Verdana, sans-serif;
                transition: border-color 0.2s;
            }
            QLineEdit:focus {
                border: 3px solid #d72660;
                background: #fcf7fa;
                box-shadow: 0 0 0 3px #f5c7e4aa;
            }
            QLineEdit[echoMode="2"] {
                color: #180d29;
                letter-spacing: 2px;
            }
            QLineEdit::placeholder {
                color: #786088;
                font-size: 18px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #d72660, stop:1 #f88379);
                color: #fff;
                border-radius: 27px;
                font-weight: bold;
                font-size: 18px;
                padding: 12px 40px;
                border: none;
                letter-spacing: 1.5px;
                box-shadow: 0 2px 8px #ecc4e099;
                outline: none;
                transition: background 0.2s, box-shadow 0.2s;
            }
            QPushButton:focus {
                box-shadow: 0 0 0 4px #fff0edbb;
                border: 2px solid #d72660;
            }
            QPushButton:hover {
                background: #e24785;
            }
        """)

        # Logo above card, adaptive size
        logo = QLabel()
        pixmap = QPixmap("assets/logo.jpeg")
        if not pixmap.isNull():
            logo_width = min(max(self.width() // 5, 70), 130)
            pixmap = pixmap.scaled(logo_width, logo_width, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        logo.setStyleSheet("margin-bottom: 30px; margin-top:20px;")
        outer.addWidget(logo, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Card (strong white pill w/ soft shadow), grows with window
        card = QWidget()
        card.setObjectName("arcadiaCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(28)
        card_layout.setContentsMargins(64, 38, 64, 38)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Inputs (pill, large, high contrast, responsive)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumHeight(54)
        self.username_input.setFont(QFont("Arial", 18))
        self.username_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.username_input.setAccessibleName("Username")
        self.username_input.setToolTip("Enter your username")
        card_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(54)
        self.password_input.setFont(QFont("Arial", 18))
        self.password_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.password_input.setAccessibleName("Password")
        self.password_input.setToolTip("Enter your password")
        card_layout.addWidget(self.password_input)

        # Pill-gradient buttons row
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        self.login_button.setAccessibleName("Login")
        self.login_button.setToolTip("Submit your login credentials")
        self.register_button.setAccessibleName("Register")
        self.register_button.setToolTip("Go to registration form")
        for btn in [self.login_button, self.register_button]:
            btn.setMinimumHeight(54)
            btn.setMinimumWidth(160)
            btn.setFont(QFont("Arial", 17, QFont.Weight.Bold))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn_row.addWidget(btn)
        btn_row.setSpacing(46)
        card_layout.addLayout(btn_row)
        outer.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch(1)

    # Optionally, dynamically adjust logo on resize
    def resizeEvent(self, event):
        logo = self.findChild(QLabel)
        pixmap = QPixmap("assets/logo.jpeg")
        if logo and not pixmap.isNull():
            width = self.width()
            logo_w = min(max(width // 6, 80), 170)
            logo.setPixmap(pixmap.scaled(logo_w, logo_w, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        super().resizeEvent(event)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = LoginWidget()
    w.showMaximized()
    sys.exit(app.exec())
