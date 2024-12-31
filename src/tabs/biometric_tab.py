from PySide6.QtCore import QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QDoubleSpinBox, QComboBox, QDateEdit, QPushButton, \
    QMessageBox

from src.modules.engine import Engine


class BiometricTab(QWidget):
    def __init__(self, db_handler, parent=None):
        super().__init__(parent)
        self.engine = Engine(db_handler)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        self.user_combo = QComboBox()
        self.load_users()

        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)

        self.height_spinbox = QDoubleSpinBox()
        self.height_spinbox.setDecimals(1)
        self.height_spinbox.setMinimum(0)
        self.height_spinbox.setMaximum(300)
        self.height_spinbox.setSuffix(" cm")
        self.height_spinbox.setFixedSize(100, 25)

        self.weight_spinbox = QDoubleSpinBox()
        self.weight_spinbox.setDecimals(1)
        self.weight_spinbox.setMinimum(0)
        self.weight_spinbox.setMaximum(300)
        self.weight_spinbox.setSuffix(" kg")
        self.weight_spinbox.setFixedSize(100, 25)

        self.shoulders_spinbox = QDoubleSpinBox()
        self.shoulders_spinbox.setDecimals(1)
        self.shoulders_spinbox.setMinimum(0)
        self.shoulders_spinbox.setMaximum(300)
        self.shoulders_spinbox.setSuffix(" cm")
        self.shoulders_spinbox.setFixedSize(100, 25)

        self.chest_spinbox = QDoubleSpinBox()
        self.chest_spinbox.setDecimals(1)
        self.chest_spinbox.setMinimum(0)
        self.chest_spinbox.setMaximum(300)
        self.chest_spinbox.setSuffix(" cm")
        self.chest_spinbox.setFixedSize(100, 25)

        self.upper_arm_left_spinbox = QDoubleSpinBox()
        self.upper_arm_left_spinbox.setDecimals(1)
        self.upper_arm_left_spinbox.setMinimum(0)
        self.upper_arm_left_spinbox.setMaximum(100)
        self.upper_arm_left_spinbox.setSuffix(" cm")
        self.upper_arm_left_spinbox.setFixedSize(100, 25)

        self.upper_arm_right_spinbox = QDoubleSpinBox()
        self.upper_arm_right_spinbox.setDecimals(1)
        self.upper_arm_right_spinbox.setMinimum(0)
        self.upper_arm_right_spinbox.setMaximum(100)
        self.upper_arm_right_spinbox.setSuffix(" cm")
        self.upper_arm_right_spinbox.setFixedSize(100, 25)

        self.forearm_left_spinbox = QDoubleSpinBox()
        self.forearm_left_spinbox.setDecimals(1)
        self.forearm_left_spinbox.setMinimum(0)
        self.forearm_left_spinbox.setMaximum(100)
        self.forearm_left_spinbox.setSuffix(" cm")
        self.forearm_left_spinbox.setFixedSize(100, 25)

        self.forearm_right_spinbox = QDoubleSpinBox()
        self.forearm_right_spinbox.setDecimals(1)
        self.forearm_right_spinbox.setMinimum(0)
        self.forearm_right_spinbox.setMaximum(100)
        self.forearm_right_spinbox.setSuffix(" cm")
        self.forearm_right_spinbox.setFixedSize(100, 25)

        self.waist_spinbox = QDoubleSpinBox()
        self.waist_spinbox.setDecimals(1)
        self.waist_spinbox.setMinimum(0)
        self.waist_spinbox.setMaximum(200)
        self.waist_spinbox.setSuffix(" cm")
        self.waist_spinbox.setFixedSize(100, 25)

        self.hips_spinbox = QDoubleSpinBox()
        self.hips_spinbox.setDecimals(1)
        self.hips_spinbox.setMinimum(0)
        self.hips_spinbox.setMaximum(200)
        self.hips_spinbox.setSuffix(" cm")
        self.hips_spinbox.setFixedSize(100, 25)

        self.upper_leg_left_spinbox = QDoubleSpinBox()
        self.upper_leg_left_spinbox.setDecimals(1)
        self.upper_leg_left_spinbox.setMinimum(0)
        self.upper_leg_left_spinbox.setMaximum(100)
        self.upper_leg_left_spinbox.setSuffix(" cm")
        self.upper_leg_left_spinbox.setFixedSize(100, 25)

        self.upper_leg_right_spinbox = QDoubleSpinBox()
        self.upper_leg_right_spinbox.setDecimals(1)
        self.upper_leg_right_spinbox.setMinimum(0)
        self.upper_leg_right_spinbox.setMaximum(100)
        self.upper_leg_right_spinbox.setSuffix(" cm")
        self.upper_leg_right_spinbox.setFixedSize(100, 25)

        self.calf_left_spinbox = QDoubleSpinBox()
        self.calf_left_spinbox.setDecimals(1)
        self.calf_left_spinbox.setMinimum(0)
        self.calf_left_spinbox.setMaximum(100)
        self.calf_left_spinbox.setSuffix(" cm")
        self.calf_left_spinbox.setFixedSize(100, 25)

        self.calf_right_spinbox = QDoubleSpinBox()
        self.calf_right_spinbox.setDecimals(1)
        self.calf_right_spinbox.setMinimum(0)
        self.calf_right_spinbox.setMaximum(100)
        self.calf_right_spinbox.setSuffix(" cm")
        self.calf_right_spinbox.setFixedSize(100, 25)

        self.save_btn = QPushButton("Save Biometric Data")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_biometric_data)

        form_layout = QFormLayout()
        form_layout.addRow("User:", self.user_combo)
        form_layout.addRow("Date:", self.date_edit)
        form_layout.addRow("Height:", self.height_spinbox)
        form_layout.addRow("Weight:", self.weight_spinbox)
        form_layout.addRow("Shoulders:", self.shoulders_spinbox)
        form_layout.addRow("Chest:", self.chest_spinbox)
        form_layout.addRow("Left Upper Arm:", self.upper_arm_left_spinbox)
        form_layout.addRow("Right Upper Arm:", self.upper_arm_right_spinbox)
        form_layout.addRow("Left Forearm:", self.forearm_left_spinbox)
        form_layout.addRow("Right Forearm:", self.forearm_right_spinbox)
        form_layout.addRow("Waist:", self.waist_spinbox)
        form_layout.addRow("Hips:", self.hips_spinbox)
        form_layout.addRow("Left Upper Leg:", self.upper_leg_left_spinbox)
        form_layout.addRow("Right Upper Leg:", self.upper_leg_right_spinbox)
        form_layout.addRow("Left Calf:", self.calf_left_spinbox)
        form_layout.addRow("Right Calf:", self.calf_right_spinbox)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.save_btn)
        self.setLayout(main_layout)

    def load_users(self):
        users = self.engine.load_users()
        self.user_combo.addItems(users)

    def save_biometric_data(self):
        user = self.user_combo.currentText()
        if not user:
            QMessageBox.warning(self, "Warning", "Please select a user.")
            return

        date = self.date_edit.date().toString("yyyy-MM-dd")
        height = self.height_spinbox.value()
        weight = self.weight_spinbox.value()
        shoulders = self.shoulders_spinbox.value()
        chest = self.chest_spinbox.value()
        upper_arm_left = self.upper_arm_left_spinbox.value()
        upper_arm_right = self.upper_arm_right_spinbox.value()
        forearm_left = self.forearm_left_spinbox.value()
        forearm_right = self.forearm_right_spinbox.value()
        waist = self.waist_spinbox.value()
        hips = self.hips_spinbox.value()
        upper_leg_left = self.upper_leg_left_spinbox.value()
        upper_leg_right = self.upper_leg_right_spinbox.value()
        calf_left = self.calf_left_spinbox.value()
        calf_right = self.calf_right_spinbox.value()

        user_id_query = self.engine.execute_query("SELECT id FROM users WHERE name = :name", {":name": user})
        if user_id_query:
            user_id = user_id_query[0][0]
            self.engine.execute_query("""
                INSERT INTO biometric_data (user, date, height, weight, shoulders, chest, upper_arm_left, upper_arm_right, forearm_left, forearm_right, waist, hips, upper_leg_left, upper_leg_right, calf_left, calf_right)
                VALUES (:user, :date, :height, :weight, :shoulders, :chest, :upper_arm_left, :upper_arm_right, :forearm_left, :forearm_right, :waist, :hips, :upper_leg_left, :upper_leg_right, :calf_left, :calf_right)
            """, {
                ":user": user,
                ":date": date,
                ":height": height,
                ":weight": weight,
                ":shoulders": shoulders,
                ":chest": chest,
                ":upper_arm_left": upper_arm_left,
                ":upper_arm_right": upper_arm_right,
                ":forearm_left": forearm_left,
                ":forearm_right": forearm_right,
                ":waist": waist,
                ":hips": hips,
                ":upper_leg_left": upper_leg_left,
                ":upper_leg_right": upper_leg_right,
                ":calf_left": calf_left,
                ":calf_right": calf_right
            })
            QMessageBox.information(self, "Success", "Biometric data saved to database.")
        else:
            QMessageBox.critical(self, "Error", "User not found.")
