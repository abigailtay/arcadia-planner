from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout
)
from src.ui.navigation_bar import NavigationBar
from PyQt6.QtCore import Qt

class DashboardFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboardMain")
        self.setAccessibleName("Dashboard Main Frame")
        layout = QVBoxLayout(self)
        layout.addStretch(1)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arcadia Planner")
        self.setMinimumSize(900, 660)

        # Central stacked widget for navigation
        self.stacked = QStackedWidget()
        self.dashboard = DashboardFrame()
        self.tasks = QWidget()
        self.habits = QWidget()
        self.budget = QWidget()
        self.recipe_box = QWidget()
        self.store = QWidget()

        # Set ARIA-like accessible names for frames
        self.tasks.setAccessibleName("Tasks Main Frame")
        self.habits.setAccessibleName("Habits Main Frame")
        self.budget.setAccessibleName("Budget Main Frame")
        self.recipe_box.setAccessibleName("Recipe Box Main Frame")
        self.store.setAccessibleName("Store Main Frame")

        self.stacked.addWidget(self.dashboard)
        self.stacked.addWidget(self.tasks)
        self.stacked.addWidget(self.habits)
        self.stacked.addWidget(self.budget)
        self.stacked.addWidget(self.recipe_box)
        self.stacked.addWidget(self.store)

        # Set up layout
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 62)  # Reserve space for nav bar
        layout.addWidget(self.stacked)
        self.setCentralWidget(central)

        # Bottom navigation bar
        self.navbar = NavigationBar()
        self.navbar.setParent(self)
        self.navbar.setGeometry(0, self.height() - self.navbar.height(), self.width(), self.navbar.height())
        self.navbar.show()

        # Connect navigation buttons
        self.navbar.button_widgets[0].clicked.connect(lambda: self.navigate_to(0))  # Dashboard
        self.navbar.button_widgets[1].clicked.connect(lambda: self.navigate_to(1))  # Tasks
        self.navbar.button_widgets[2].clicked.connect(lambda: self.navigate_to(2))  # Habits
        self.navbar.button_widgets[3].clicked.connect(lambda: self.navigate_to(3))  # Budget
        self.navbar.button_widgets[4].clicked.connect(lambda: self.navigate_to(4))  # Recipe Box
        self.navbar.button_widgets[5].clicked.connect(lambda: self.navigate_to(5))  # Store

        # Accessibility: Set tab order for nav bar
        for i in range(len(self.navbar.button_widgets) - 1):
            QWidget.setTabOrder(self.navbar.button_widgets[i], self.navbar.button_widgets[i+1])

    def resizeEvent(self, event):
        self.navbar.setGeometry(0, self.height() - self.navbar.height(), self.width(), self.navbar.height())
        super().resizeEvent(event)

    def navigate_to(self, index):
        self.stacked.setCurrentIndex(index)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
