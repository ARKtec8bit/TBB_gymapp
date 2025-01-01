import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTabWidget, QWidget

from src.modules.db_handler import DBHandler
from src.tabs.biometric_tab import BiometricTab
from src.tabs.custom_workout_tab import CustomWorkoutTab
from src.tabs.dashboard_tab import DashboardTab
from src.tabs.data_visualization_tab import DataVisualizationTab
from src.tabs.database_view_tab import DatabaseViewTab
from src.tabs.random_workout_tab import RandomWorkoutTab
from src.tabs.timer_tab import BoxingTimer
from src.tabs.karate_class_tab import KarateClassDocument
from src.tabs.splash_screen_tab import SplashScreenTab

class WorkoutApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loser Barbell Workout App")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("data/lbb.png"))
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()  # Use vertical layout
        # self.showFullScreen()
        # Initialize database handler and create tables
        self.db_handler = DBHandler("data/workout_db.sqlite")
        self.db_handler.create_tables()

        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(SplashScreenTab(), "Welcome")
        self.tabs.addTab(DashboardTab(self.db_handler, self), "Dashboard")
        self.tabs.addTab(RandomWorkoutTab(self.db_handler), "Random Workout")
        self.tabs.addTab(CustomWorkoutTab(self.db_handler), "Custom Workout")
        self.tabs.addTab(BoxingTimer(), "Boxing Timer")
        self.tabs.addTab(KarateClassDocument(), "Karate Class")
        self.tabs.addTab(BiometricTab(self.db_handler), "Biometric Data")
        self.tabs.addTab(DataVisualizationTab(self.db_handler, self), "Data Visualization")
        self.tabs.addTab(DatabaseViewTab(self.db_handler), "Data Tables")

        # Add tabs to the main layout
        self.main_layout.addWidget(self.tabs)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Apply the default theme
        self.apply_theme("dark_solarized")

    def apply_theme(self, theme_name):
        match theme_name:
            case "dark_solarized":
                with open("data/themes/dark_solarized.qss", "r") as f:
                    stylesheet = f.read()
            case "light_solarized":
                with open("data/themes/light_solarized.qss", "r") as f:
                    stylesheet = f.read()
            case "gruvbox_dark":
                with open("data/themes/gruvbox_dark.qss", "r") as f:
                    stylesheet = f.read()
            case "gruvbox_light":
                with open("data/themes/gruvbox_light.qss", "r") as f:
                    stylesheet = f.read()
            case _:
                pass
        self.setStyleSheet(stylesheet)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WorkoutApp()
    window.show()
    sys.exit(app.exec())
