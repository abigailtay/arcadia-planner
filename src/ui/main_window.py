import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arcadia Planner")
        self.setGeometry(100, 100, 900, 600)
        
        # Color palette (soft pinks, white, grey)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#fae2f7"))  # Light pink background
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#353535"))  # Grey-black font
        self.setPalette(palette)
        
        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Placeholder: Add a label or login widget below
        from src.ui.login_widget import LoginWidget
        self.login = LoginWidget()
        self.main_layout.addWidget(self.login)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
