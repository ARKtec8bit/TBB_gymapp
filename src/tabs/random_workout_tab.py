import random

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QDateEdit, QLabel, QScrollArea, QFormLayout, QGridLayout, \
    QDoubleSpinBox, QSpinBox, QMessageBox

from src.modules.engine import Engine


class RandomWorkoutTab(QWidget):
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

        self.generate_btn = QPushButton("Generate Random Workout")
        self.generate_btn.setObjectName("generate_btn")
        self.generate_btn.clicked.connect(self.generate_workout)

        self.save_btn = QPushButton("Save to Database")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_to_database)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QGridLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        main_layout.addWidget(QLabel("Select User:"))
        main_layout.addWidget(self.user_combo)
        main_layout.addWidget(QLabel("Select Date:"))
        main_layout.addWidget(self.date_edit)
        main_layout.addWidget(self.generate_btn)
        main_layout.addWidget(self.save_btn)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def load_users(self):
        users = self.engine.load_users()
        self.user_combo.addItems(users)

    def generate_workout(self):
        # Clear existing layout content
        for i in reversed(range(self.scroll_layout.count())):
            widget_to_remove = self.scroll_layout.itemAt(i).widget()
            self.scroll_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        data = self.engine.load_random_workouts()
        body_parts = set(exercise['body_part'] for exercise in data)
        selected_exercises = {body_part: random.choice([exercise for exercise in data if exercise['body_part'] == body_part]) for body_part in body_parts}

        row, col = 0, 0
        for exercise in selected_exercises.values():
            exercise_widget = QWidget()
            exercise_layout = QVBoxLayout(exercise_widget)

            exercise_label = QLabel(f"{exercise['body_part']} - {exercise['exercise']}")
            exercise_label.setObjectName("exercise_label")
            exercise_layout.addWidget(exercise_label)

            set_details_layout = QFormLayout()
            sets = exercise['sets']
            total_volume = 0

            for i in range(sets):
                weight_spinbox = QDoubleSpinBox()
                weight_spinbox.setObjectName("weight_spinbox")
                weight_spinbox.setDecimals(2)
                weight_spinbox.setMinimum(0)
                weight_spinbox.setMaximum(999.99)
                weight_spinbox.setValue(exercise['weight'])
                weight_spinbox.setSuffix(" kg")
                weight_spinbox.setFixedSize(125, 40)

                reps_spinbox = QSpinBox()
                reps_spinbox.setObjectName("reps_spinbox")
                reps_spinbox.setMinimum(0)
                reps_spinbox.setMaximum(999)
                reps_spinbox.setValue(exercise['reps'])
                reps_spinbox.setFixedSize(125, 40)

                set_details_layout.addRow(f"Set {i + 1} Weight:", weight_spinbox)
                set_details_layout.addRow(f"Set {i + 1} Reps:", reps_spinbox)

                weight_spinbox.valueChanged.connect(self.update_total_volume)
                reps_spinbox.valueChanged.connect(self.update_total_volume)

                total_volume += weight_spinbox.value() * reps_spinbox.value()

            volume_label = QLabel(f"Total Volume: {total_volume:.2f} kg")
            volume_label.setObjectName("volume_label")
            exercise_layout.addLayout(set_details_layout)
            exercise_layout.addWidget(volume_label)

            self.scroll_layout.addWidget(exercise_widget, row, col)

            col += 1
            if col == 3:
                col = 0
                row += 1

    def update_total_volume(self):
        for i in range(self.scroll_layout.count()):
            exercise_widget = self.scroll_layout.itemAt(i).widget()
            if exercise_widget:
                set_details_layout = exercise_widget.layout().itemAt(1).layout()
                total_volume = 0
                for j in range(0, set_details_layout.rowCount(), 2):
                    weight_spinbox = set_details_layout.itemAt(j, QFormLayout.FieldRole).widget()
                    reps_spinbox = set_details_layout.itemAt(j + 1, QFormLayout.FieldRole).widget()
                    if weight_spinbox and reps_spinbox:
                        total_volume += weight_spinbox.value() * reps_spinbox.value()
                volume_label = exercise_widget.layout().itemAt(2).widget()
                volume_label.setText(f"Total Volume: {total_volume:.2f} kg")

    def save_to_database(self):
        user = self.user_combo.currentText()
        if not user:
            QMessageBox.warning(self, "Warning", "Please select a user.")
            return

        date = self.date_edit.date().toString("yyyy-MM-dd")

        # Retrieve the user_id corresponding to the selected user
        headers, user_id_query = self.engine.execute_query("SELECT id FROM users WHERE name = :name", {":name": user})
        if user_id_query:
            user_id = user_id_query[0][0]
            for i in range(self.scroll_layout.count()):
                exercise_widget = self.scroll_layout.itemAt(i).widget()
                if exercise_widget:
                    body_part, exercise_name = exercise_widget.layout().itemAt(0).widget().text().split(" - ")
                    set_details_layout = exercise_widget.layout().itemAt(1).layout()
                    sets = set_details_layout.rowCount() // 2
                    weights_reps = {}
                    volume = 0

                    for j in range(sets):
                        weight_spinbox = set_details_layout.itemAt(j * 2, QFormLayout.FieldRole).widget()
                        reps_spinbox = set_details_layout.itemAt(j * 2 + 1, QFormLayout.FieldRole).widget()
                        weight = weight_spinbox.value()
                        reps = reps_spinbox.value()
                        volume += weight * reps
                        weights_reps[f"set{j + 1}_weight"] = weight
                        weights_reps[f"set{j + 1}_reps"] = reps

                    weights_reps = {f"set{j + 1}_weight": weights_reps.get(f"set{j + 1}_weight", None) for j in
                                    range(5)} | \
                                   {f"set{j + 1}_reps": weights_reps.get(f"set{j + 1}_reps", None) for j in range(5)}

                    self.engine.execute_query("""
                        INSERT INTO weights (date, user_id, exercise, set1_weight, set1_reps, set2_weight, set2_reps, set3_weight, set3_reps, set4_weight, set4_reps, set5_weight, set5_reps, volume)
                        VALUES (:date, :user_id, :exercise, :set1_weight, :set1_reps, :set2_weight, :set2_reps, :set3_weight, :set3_reps, :set4_weight, :set4_reps, :set5_weight, :set5_reps, :volume)
                    """, {
                        ":date": date,
                        ":user_id": user_id,
                        ":exercise": exercise_name,
                        ":set1_weight": weights_reps.get("set1_weight"),
                        ":set1_reps": weights_reps.get("set1_reps"),
                        ":set2_weight": weights_reps.get("set2_weight"),
                        ":set2_reps": weights_reps.get("set2_reps"),
                        ":set3_weight": weights_reps.get("set3_weight"),
                        ":set3_reps": weights_reps.get("set3_reps"),
                        ":set4_weight": weights_reps.get("set4_weight"),
                        ":set4_reps": weights_reps.get("set4_reps"),
                        ":set5_weight": weights_reps.get("set5_weight"),
                        ":set5_reps": weights_reps.get("set5_reps"),
                        ":volume": volume
                    })
            QMessageBox.information(self, "Success", "Workout saved to database.")
        else:
            QMessageBox.critical(self, "Error", "User not found.")
