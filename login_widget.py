from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, 
    QSizePolicy, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal


class LoginWidget(QWidget):
    """Professional login form with accessibility features."""
    
    # Signals for parent widget to connect to
    login_requested = pyqtSignal(str, str)  # username, password
    register_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.logo_label = None
        self.username_input = None
        self.password_input = None
        self.login_button = None
        self.register_button = None
        self.setup_ui()
        
    def get_stylesheet(self):
        """Centralized stylesheet with industry-standard design."""
        return """
            QWidget {
                background: white;
            }
            #arcadiaCard {
                background: #f5f0f9;
                border-radius: 16px;
                border: 2px solid #e0d0e8;
            }
            #logoContainer {
                background: white;
                border-radius: 20px;
                padding: 24px;
                border: 3px solid #e0d0e8;
            }
            QLabel {
                color: #2d2d2d;
                font-size: 16px;
                font-weight: 600;
            }
            QLineEdit {
                background: white;
                border: 2px solid #d8cfe0;
                border-radius: 12px;
                color: #2d2d2d;
                font-size: 16px;
                padding: 0px 20px;
                min-height: 48px;
            }
            QLineEdit:focus {
                border: 2px solid #8b5fa8;
                background: #fdfcfe;
            }
            QLineEdit:hover {
                border: 2px solid #b89fc8;
            }
            QLineEdit[error="true"] {
                border: 2px solid #d32f2f;
                background: #fff5f5;
            }
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8b5fa8,
                    stop:1 #a67fc6
                );
                color: white;
                border-radius: 12px;
                font-weight: bold;
                font-size: 16px;
                padding: 14px 32px;
                border: none;
                min-height: 48px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7a4f96,
                    stop:1 #9566b5
                );
            }
            QPushButton:pressed {
                background: #6a4585;
                padding: 15px 31px 13px 33px;
            }
            QPushButton:disabled {
                background: #d0d0d0;
                color: #888888;
            }
            QPushButton:focus {
                border: 2px solid #5a3a6a;
            }
        """

    def setup_ui(self):
        """Initialize and configure all UI elements."""
        self.setStyleSheet(self.get_stylesheet())
        
        # Main outer layout - centers everything
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.setContentsMargins(40, 40, 40, 40)
        
        # Logo container with white background for better visibility
        logo_container = QWidget()
        logo_container.setObjectName("logoContainer")
        logo_container_layout = QVBoxLayout(logo_container)
        logo_container_layout.setContentsMargins(0, 0, 0, 0)
        
        self.logo_label = QLabel()
        self._load_logo()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        logo_container_layout.addWidget(self.logo_label)
        
        outer.addWidget(logo_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addSpacing(32)
        
        # Card container
        card = QWidget()
        card.setObjectName("arcadiaCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(24)
        card_layout.setContentsMargins(48, 40, 48, 40)
        card.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        card.setMaximumWidth(480)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(QFont("Arial", 16))
        self.username_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.username_input.setAccessibleName("Username")
        self.username_input.setAccessibleDescription("Enter your username to log in")
        self.username_input.setToolTip("Enter your username")
        self.username_input.returnPressed.connect(self._focus_password)
        card_layout.addWidget(self.username_input)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Arial", 16))
        self.password_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.password_input.setAccessibleName("Password")
        self.password_input.setAccessibleDescription("Enter your password")
        self.password_input.setToolTip("Enter your password")
        self.password_input.returnPressed.connect(self._handle_login)
        card_layout.addWidget(self.password_input)
        
        # Button row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.login_button.setAccessibleName("Login")
        self.login_button.setAccessibleDescription("Submit your login credentials")
        self.login_button.setToolTip("Click to log in")
        self.login_button.clicked.connect(self._handle_login)
        
        self.register_button = QPushButton("Register")
        self.register_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.register_button.setAccessibleName("Register")
        self.register_button.setAccessibleDescription("Create a new account")
        self.register_button.setToolTip("Click to create a new account")
        self.register_button.clicked.connect(self._handle_register)
        
        btn_row.addWidget(self.login_button)
        btn_row.addWidget(self.register_button)
        card_layout.addLayout(btn_row)
        
        # Add card to outer layout
        outer.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch(1)
        
        # Set tab order for keyboard navigation
        self.setTabOrder(self.username_input, self.password_input)
        self.setTabOrder(self.password_input, self.login_button)
        self.setTabOrder(self.login_button, self.register_button)
        
    def _load_logo(self):
        """Load logo with fallback to emoji if file not found."""
        pixmap = QPixmap("assets/logo.jpeg")
        if pixmap.isNull():
            # Fallback if logo file doesn't exist
            self.logo_label.setText("🔐")
            self.logo_label.setStyleSheet("font-size: 280px;")
        else:
            logo_size = 720
            scaled = pixmap.scaled(
                logo_size, logo_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled)
    
    def _focus_password(self):
        """Move focus to password field."""
        self.password_input.setFocus()
        
    def _handle_login(self):
        """Validate and emit login request."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        # Clear any previous errors
        self.username_input.setProperty("error", False)
        self.password_input.setProperty("error", False)
        self.username_input.setStyle(self.username_input.style())
        self.password_input.setStyle(self.password_input.style())
        
        # Basic validation
        if not username:
            self._show_error(self.username_input, "Username is required")
            return
            
        if not password:
            self._show_error(self.password_input, "Password is required")
            return
        
        if len(password) < 4:
            self._show_error(self.password_input, "Password is too short")
            return
        
        # Emit signal for parent to handle actual authentication
        self.login_requested.emit(username, password)
        
    def _handle_register(self):
        """Emit register request."""
        self.register_requested.emit()
        
    def _show_error(self, field, message):
        """Display validation error on a field."""
        field.setProperty("error", True)
        field.setStyle(field.style())  # Refresh style
        field.setFocus()
        field.setToolTip(f"⚠️ {message}")
        
        # Optional: Show message box for more visible feedback
        QMessageBox.warning(self, "Validation Error", message)
    
    def set_loading(self, is_loading):
        """Disable inputs during authentication."""
        self.username_input.setEnabled(not is_loading)
        self.password_input.setEnabled(not is_loading)
        self.login_button.setEnabled(not is_loading)
        self.register_button.setEnabled(not is_loading)
        
        if is_loading:
            self.login_button.setText("Logging in...")
        else:
            self.login_button.setText("Login")
    
    def clear_fields(self):
        """Clear all input fields."""
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()
        
    def resizeEvent(self, event):
        """Dynamically resize logo based on window size."""
        if self.logo_label:
            pixmap = QPixmap("assets/logo.jpeg")
            if not pixmap.isNull():
                # Scale based on SMALLER dimension to prevent overflow
                # Logo takes max 40% of screen height or width
                available_height = self.height() * 0.40
                available_width = self.width() * 0.45
                logo_size = min(available_height, available_width, 700)
                logo_size = max(logo_size, 450)  # Minimum size
                
                scaled = pixmap.scaled(
                    int(logo_size), int(logo_size),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.logo_label.setPixmap(scaled)
        super().resizeEvent(event)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create login widget
    login_widget = LoginWidget()
    
    # Connect signals to test handlers
    def handle_login(username, password):
        print(f"Login attempt - Username: {username}, Password: {'*' * len(password)}")
        # Simulate authentication delay
        login_widget.set_loading(True)
        # In real app, perform authentication here
        # Then call: login_widget.set_loading(False)
        
    def handle_register():
        print("Register button clicked")
        # Navigate to registration form
        
    login_widget.login_requested.connect(handle_login)
    login_widget.register_requested.connect(handle_register)
    
    login_widget.resize(800, 600)
    login_widget.show()
    
    sys.exit(app.exec())