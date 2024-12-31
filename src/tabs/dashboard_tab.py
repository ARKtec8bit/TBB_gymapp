# from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QInputDialog, QMessageBox
# from src.modules.engine import Engine

# class DashboardTab(QWidget):
#     def __init__(self, db_handler, main_window, parent=None):
#         super().__init__(parent)
#         self.engine = Engine(db_handler)
#         self.main_window = main_window
#         self.initUI()

#     def initUI(self):
#         layout = QVBoxLayout(self)

#         self.create_user_btn = QPushButton("Create User")
#         self.create_user_btn.setObjectName("create_user_btn")
#         self.create_user_btn.clicked.connect(self.create_user)

#         self.theme_combo = QComboBox()
#         self.theme_combo.setObjectName("theme_combo")
#         self.theme_combo.addItems(["Dark Solarized", "Light Solarized"])
#         self.theme_combo.currentIndexChanged.connect(self.change_theme)

#         self.user_combo = QComboBox()
#         self.load_users()

#         self.export_btn = QPushButton("Export User Data")
#         self.export_btn.setObjectName("export_btn")
#         self.export_btn.clicked.connect(self.export_data)

#         layout.addWidget(self.create_user_btn)
#         layout.addWidget(self.theme_combo)
#         layout.addWidget(self.user_combo)
#         layout.addWidget(self.export_btn)
#         self.setLayout(layout)

#     def load_users(self):
#         users = self.engine.load_users()
#         self.user_combo.addItems(users)

#     def create_user(self):
#         name, ok = QInputDialog.getText(self, "Create New User", "Enter user name:")
#         if ok and name:
#             try:
#                 self.engine.execute_query("INSERT INTO users (name) VALUES (:name)", {":name": name})
#                 self.load_users()
#                 QMessageBox.information(self, "Success", f"User '{name}' created successfully")
#             except Exception as e:
#                 QMessageBox.critical(self, "Error", str(e))

#     def change_theme(self):
#         theme_name = self.theme_combo.currentText().lower().replace(" ", "_")
#         self.main_window.apply_theme(theme_name)

#     def export_data(self):
#         user = self.user_combo.currentText()
#         if user:
#             try:
#                 user_id_query = self.engine.execute_query("SELECT id FROM users WHERE name = :name", {":name": user})
#                 if user_id_query:
#                     user_id = user_id_query[0][0]
#                     output_file = f"{user}_data.csv"
#                     self.engine.export_user_data(user_id, output_file)
#                     QMessageBox.information(self, "Success", f"User data exported to {output_file}")
#                 else:
#                     QMessageBox.critical(self, "Error", "User not found")
#             except Exception as e:
#                 QMessageBox.critical(self, "Error", str(e))
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QInputDialog, QMessageBox
from src.modules.engine import Engine

class DashboardTab(QWidget):
    def __init__(self, db_handler, main_window, parent=None):
        super().__init__(parent)
        self.engine = Engine(db_handler)
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.create_user_btn = QPushButton("Create User")
        self.create_user_btn.setObjectName("create_user_btn")
        self.create_user_btn.clicked.connect(self.create_user)

        self.theme_combo = QComboBox()
        self.theme_combo.setObjectName("theme_combo")
        self.theme_combo.addItems(["Dark Solarized", "Light Solarized", "Gruvbox Dark", "Gruvbox Light"])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)

        self.user_combo = QComboBox()
        self.load_users()

        self.export_btn = QPushButton("Export User Data")
        self.export_btn.setObjectName("export_btn")
        self.export_btn.clicked.connect(self.export_data)

        layout.addWidget(self.create_user_btn)
        layout.addWidget(self.theme_combo)
        layout.addWidget(self.user_combo)
        layout.addWidget(self.export_btn)
        self.setLayout(layout)

    def load_users(self):
        users = self.engine.load_users()
        self.user_combo.addItems(users)

    def create_user(self):
        name, ok = QInputDialog.getText(self, "Create New User", "Enter user name:")
        if ok and name:
            try:
                self.engine.execute_query("INSERT INTO users (name) VALUES (:name)", {":name": name})
                self.load_users()
                QMessageBox.information(self, "Success", f"User '{name}' created successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def change_theme(self):
        theme_name = self.theme_combo.currentText().lower().replace(" ", "_")
        self.main_window.apply_theme(theme_name)

    def export_data(self):
        user = self.user_combo.currentText()
        if user:
            try:
                user_id_query = self.engine.execute_query("SELECT id FROM users WHERE name = :name", {":name": user})
                if user_id_query:
                    user_id = user_id_query[0][0]
                    output_file = f"{user}_data.csv"
                    self.engine.export_user_data(user_id, output_file)
                    QMessageBox.information(self, "Success", f"User data exported to {output_file}")
                else:
                    QMessageBox.critical(self, "Error", "User not found")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
