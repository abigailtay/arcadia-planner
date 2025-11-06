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
        self.setStyleSheet("background: #fae2f7;")  # Only as frame accent

        # Logo above card, adaptive size
        logo = QLabel()
        pixmap = QPixmap("assets/logo.jpeg")
        if not pixmap.isNull():
            logo_width = min(max(self.width() // 5, 70), 130)  # responsive to window size
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
        card_layout.setContentsMargins(64, 38, 64, 38) # Responsive padding
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        card.setStyleSheet('''
            #arcadiaCard {
                background: #fff;
                border-radius: 32px;
                border: 3px solid #e0b5db;
                box-shadow: 0 12px 48px 0 #95506322;
            }
        ''')

        # Inputs (pill, large, high contrast, responsive)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumHeight(54)
        self.username_input.setFont(QFont("Arial", 18))
        self.username_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        card_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(54)
        self.password_input.setFont(QFont("Arial", 18))
        self.password_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        card_layout.addWidget(self.password_input)

        # Pill-gradient buttons row
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        for btn in [self.login_button, self.register_button]:
            btn.setMinimumHeight(54)
            btn.setMinimumWidth(160)
            btn.setFont(QFont("Arial", 17, QFont.Weight.Bold))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setStyleSheet('''
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
                }
                QPushButton:hover {
                    background: #e24785;
                }
            ''')
            btn_row.addWidget(btn)
        btn_row.setSpacing(46)
        card_layout.addLayout(btn_row)
        outer.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch(1)

        # Inputs: maximum readable, responsive, accent on focus, visually separated
        self.setStyleSheet(self.styleSheet() + '''
        QLineEdit {
            background: #fff; border: 3px solid #e3b6e9; border-radius: 27px;
            color: #22172e; font-size: 18px; padding-left: 20px; margin-bottom: 18px;
        }
        QLineEdit:focus {
            border: 3px solid #d72660; background: #fcf7fa;
        }
        QLineEdit::placeholder {
            color: #786088; font-size: 18px;
        }
        ''')

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
    w.showMaximized()  # Show the effect in a big window
    sys.exit(app.exec())
