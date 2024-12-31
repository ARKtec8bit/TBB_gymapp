import matplotlib.pyplot as plt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QLabel, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from src.modules.engine import Engine


class DataVisualizationTab(QWidget):
    def __init__(self, db_handler, parent=None):
        super().__init__(parent)
        self.engine = Engine(db_handler)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.user_combo = QComboBox()
        self.load_users()

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Workout", "Biometric Data"])
        self.category_combo.currentIndexChanged.connect(self.update_filters)

        self.filter_combo = QComboBox()

        self.plot_btn = QPushButton("Plot Data")
        self.plot_btn.setObjectName("plt_btn")
        self.plot_btn.clicked.connect(self.plot_data)

        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("User:"))
        control_layout.addWidget(self.user_combo)
        control_layout.addWidget(QLabel("Category:"))
        control_layout.addWidget(self.category_combo)
        control_layout.addWidget(QLabel("Filter:"))
        control_layout.addWidget(self.filter_combo)
        control_layout.addWidget(self.plot_btn)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout.addLayout(control_layout)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def load_users(self):
        # print("Loading users...")  # Debug print
        headers, users = self.engine.execute_query("SELECT name FROM users")
        self.user_combo.addItems([user[0] for user in users if user])
        # print("Users loaded")  # Debug print

    def update_filters(self):
        # print("Updating filters...")  # Debug print
        category = self.category_combo.currentText()
        self.filter_combo.clear()
        if category == "Workout":
            self.filter_combo.addItem("All")
            headers, exercises = self.engine.execute_query("SELECT DISTINCT exercise FROM weights")
            # print(f"Workout exercises fetched: {exercises}")  # Enhanced Debug print
            if exercises:
                self.filter_combo.addItems([exercise[0] for exercise in exercises])
            else:
                print("No exercises found.")  # Debug print for empty exercises list
        elif category == "Biometric Data":
            self.filter_combo.addItem("All")
            measurements = ["height", "weight", "shoulders", "chest", "upper_arm_left", "upper_arm_right", "forearm_left", "forearm_right", "waist", "hips", "upper_leg_left", "upper_leg_right", "calf_left", "calf_right"]
            # print(f"Biometric measurements: {measurements}")  # Debug print
            self.filter_combo.addItems(measurements)
        # print("Filters updated")  # Debug print


    def plot_data(self):
        plt.style.use("Solarize_Light2")
        user = self.user_combo.currentText()
        if not user:
            QMessageBox.warning(self, "Warning", "Please select a user.")
            return
        category = self.category_combo.currentText()
        filter_value = self.filter_combo.currentText()

        # print(f"Plotting data for User: {user}, Category: {category}, Filter: {filter_value}")  # Debug print

        if category == "Workout":
            query = "SELECT date, volume FROM weights WHERE user_id = (SELECT id FROM users WHERE name = :name)"
            params = {":name": user}
            if filter_value and filter_value != "All":
                query += " AND exercise = :exercise"
                params[":exercise"] = filter_value
        elif category == "Biometric Data":
            query = f"SELECT date, {filter_value} FROM biometric_data WHERE user = :name"
            params = {":name": user}
            if filter_value == "All":
                QMessageBox.warning(self, "Warning", "Please select a specific measurement to plot.")
                return

        headers, data = self.engine.execute_query(query, params)
        # print(f"Query Headers: {headers}, Data: {data}")  # Debug print

        if not data:
            QMessageBox.warning(self, "Warning", "No data available for the selected parameters.")
            return

        if category == "Workout":
            dates, volumes = zip(*data)
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(dates, volumes, marker='o')
            ax.set_xlabel("Date")
            ax.set_ylabel("Volume")
            ax.set_title(f"Volume over Time for {user}")
            self.canvas.draw()
            # print("Data plotted by volume")  # Debug print

        else:  # category == "Biometric Data"
            dates, values = zip(*data)
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(dates, values, marker='o')
            ax.set_xlabel("Date")
            ax.set_ylabel(filter_value)
            ax.set_title(f"{filter_value} over Time for {user}")
            self.canvas.draw()
            # print("Data plotted by biometric data")  # Debug print

