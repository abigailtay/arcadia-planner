from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt

class NavigationBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        bar_layout = QHBoxLayout(self)  # Set layout directly on self
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.setSpacing(0)
        bar_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        buttons = [
            ("Dashboard", "dashboard button"),
            ("Tasks", "tasks button"),
            ("Habits", "habits button"),
            ("Budget", "budget button"),
            ("Recipe Box", "recipe box button"),
            ("Store", "store button")
        ]

        self.button_widgets = []
        for name, aria in buttons:
            btn = QPushButton(name)
            btn.setObjectName(f"navBtn_{name.lower().replace(' ', '_')}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(42)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Expands horizontally
            btn.setAccessibleName(name)
            btn.setAccessibleDescription(f"Navigate to {aria}")
            btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: #f5f0f9;
                    color: #5a3a6a;
                    font-size: 15px;
                    padding: 12px 18px;
                }
                QPushButton:hover, QPushButton:focus {
                    background: #ede2f5;
                    color: #8b5fa8;
                    border-top: 2px solid #8b5fa8;
                }
                QPushButton:pressed {
                    background: #dbc9eb;
                    color: #6a4585;
                }
            """)
            bar_layout.addWidget(btn)
            self.button_widgets.append(btn)

        self.setFixedHeight(62)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
