from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QLabel
from src.modules.engine import Engine

class DatabaseViewTab(QWidget):
    def __init__(self, db_handler, parent=None):
        super().__init__(parent)
        self.engine = Engine(db_handler)
        self.category_combo = None  # Ensure attribute is declared
        self.initUI()
        self.filter_data()  # Update the table upon opening the tab

    def initUI(self):
        main_layout = QVBoxLayout(self)

        self.user_combo = QComboBox()
        self.user_combo.currentIndexChanged.connect(self.filter_data)
        self.load_users()

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Workout", "Biometric Data"])
        self.category_combo.currentIndexChanged.connect(self.update_filters)

        self.filter_combo = QComboBox()
        self.filter_combo.currentIndexChanged.connect(self.filter_data)

        self.table_view = QTableWidget()

        self.delete_btn = QPushButton("Delete Row")
        self.delete_btn.setObjectName("delete_btn")
        self.delete_btn.clicked.connect(self.delete_row)

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_changes)

        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.setObjectName("generate_btn")
        self.refresh_btn.clicked.connect(self.refresh_data)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("User:"))
        filter_layout.addWidget(self.user_combo)
        filter_layout.addWidget(QLabel("Category:"))
        filter_layout.addWidget(self.category_combo)
        filter_layout.addWidget(QLabel("Filter:"))
        filter_layout.addWidget(self.filter_combo)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        # print("UI Initialized")  # Debug print

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
        self.filter_data()
        # print("Filters updated")  # Debug print

    def filter_data(self):
        # print("Filtering data...")  # Debug print
        user = self.user_combo.currentText()
        if not self.category_combo:  # Check if category_combo is None
            # print("category_combo is not initialized")
            return
        category = self.category_combo.currentText()
        filter_value = self.filter_combo.currentText()

        # print(f"User: {user}, Category: {category}, Filter: {filter_value}")  # Debug print

        if category == "Workout":
            query = "SELECT * FROM weights WHERE user_id = (SELECT id FROM users WHERE name = :name)"
            params = {":name": user}
            if filter_value and filter_value != "All":
                query += " AND exercise = :exercise"
                params[":exercise"] = filter_value
        elif category == "Biometric Data":
            query = "SELECT * FROM biometric_data WHERE user = :name"
            params = {":name": user}
            if filter_value and filter_value != "All":
                query += f" AND {filter_value} IS NOT NULL"

        headers, data = self.engine.execute_query(query, params)
        # print(f"Query Headers: {headers}, Data: {data}")  # Debug print

        self.table_view.setRowCount(0)
        self.table_view.setColumnCount(len(headers) if headers else 0)
        self.table_view.setHorizontalHeaderLabels(headers)

        for row_data in data:
            row = self.table_view.rowCount()
            self.table_view.insertRow(row)
            for col, value in enumerate(row_data):
                if value is not None:  # Ensure we handle None values
                    self.table_view.setItem(row, col, QTableWidgetItem(str(value)))
                else:
                    self.table_view.setItem(row, col, QTableWidgetItem(""))
        # print("Data filtered and table updated")  # Debug print

    # Debug print

    def delete_row(self):
        current_row = self.table_view.currentRow()
        if current_row >= 0:
            confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this row?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                item = self.table_view.item(current_row, 0)
                if item:
                    record_id = item.text()
                    category = self.category_combo.currentText()
                    if category == "Workout":
                        table = "weights"
                    elif category == "Biometric Data":
                        table = "biometric_data"
                    self.engine.execute_query(f"DELETE FROM {table} WHERE id = :id", {":id": record_id})
                    self.refresh_data()

    def save_changes(self):
        user = self.user_combo.currentText()
        category = self.category_combo.currentText()
        if category == "Workout":
            table = "weights"
        elif category == "Biometric Data":
            table = "biometric_data"

        for row in range(self.table_view.rowCount()):
            record_id = self.table_view.item(row, 0).text()
            column_values = {}
            for col in range(self.table_view.columnCount()):
                column_name = self.table_view.horizontalHeaderItem(col).text()
                column_value = self.table_view.item(row, col).text()
                column_values[column_name] = column_value
            set_clause = ", ".join([f"{col} = :{col}" for col in column_values.keys()])
            params = {f":{col}": val for col, val in column_values.items()}
            params[":id"] = record_id
            self.engine.execute_query(f"UPDATE {table} SET {set_clause} WHERE id = :id", params)
        QMessageBox.information(self, "Success", "Changes saved successfully")

    def refresh_data(self):
        self.filter_data()
