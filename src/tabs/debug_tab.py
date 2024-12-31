from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from src.modules.engine import Engine

class DebuggingTab(QWidget):
    def __init__(self, db_handler, parent=None):
        super().__init__(parent)
        self.engine = Engine(db_handler)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.table_combo = QComboBox()
        self.table_combo.addItems(["users", "weights", "cardio", "conditioning", "technical", "biometric_data"])

        self.user_combo = QComboBox()
        self.load_users()

        self.load_btn = QPushButton("Load Table Data")
        self.load_btn.clicked.connect(self.load_table_data)

        self.table_view = QTableWidget()

        layout.addWidget(QLabel("Select Table:"))
        layout.addWidget(self.table_combo)
        layout.addWidget(QLabel("Select User (Optional):"))
        layout.addWidget(self.user_combo)
        layout.addWidget(self.load_btn)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def load_users(self):
        print("Loading users...")  # Debug print
        headers, users = self.engine.execute_query("SELECT name FROM users")
        self.user_combo.addItem("All Users")  # Add option to view all users
        self.user_combo.addItems([user[0] for user in users if user])
        print("Users loaded")  # Debug print

    def load_table_data(self):
        table_name = self.table_combo.currentText()
        user = self.user_combo.currentText()

        if user != "All Users" and table_name != "users":
            query = f"SELECT * FROM {table_name} WHERE user_id = (SELECT id FROM users WHERE name = :name)"
            params = {":name": user}
        else:
            query = f"SELECT * FROM {table_name}"
            params = None

        headers, data = self.engine.execute_query(query, params)
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
