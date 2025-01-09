
import json

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QDateEdit, QLabel, QScrollArea, QFormLayout, \
    QDoubleSpinBox, QSpinBox, QMessageBox

from src.modules.engine import Engine


class CustomWorkoutTab(QWidget):
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

        self.workout_combo = QComboBox()
        self.week_combo = QComboBox()
        self.day_combo = QComboBox()

        self.load_workout_data()

        self.workout_combo.currentIndexChanged.connect(self.load_weeks)
        self.week_combo.currentIndexChanged.connect(self.load_days)
        self.day_combo.currentIndexChanged.connect(self.load_workout)

        self.save_btn = QPushButton("Save to Database")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_to_database)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        # Ensure the layout is set
        scroll_content.setLayout(self.scroll_layout)
        scroll_area.setWidget(scroll_content)

        main_layout.addWidget(QLabel("Select User:"))
        main_layout.addWidget(self.user_combo)
        main_layout.addWidget(QLabel("Select Date:"))
        main_layout.addWidget(self.date_edit)
        main_layout.addWidget(QLabel("Select Workout:"))
        main_layout.addWidget(self.workout_combo)
        main_layout.addWidget(QLabel("Select Week:"))
        main_layout.addWidget(self.week_combo)
        main_layout.addWidget(QLabel("Select Day:"))
        main_layout.addWidget(self.day_combo)
        main_layout.addWidget(self.save_btn)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        # print("UI Initialized")  # Debug print

    def load_users(self):
        users = self.engine.load_users()
        self.user_combo.addItems(users)

    def load_workout_data(self):
        with open('data/json/custom_workouts.json', 'r') as file:
            self.custom_workout_data = json.load(file)
        # print("Loaded workout data:", self.custom_workout_data.keys())  # Debug print

        workout_names = self.custom_workout_data["Workouts"].keys()
        self.workout_combo.addItems(workout_names)
        self.load_weeks()  # Ensure weeks are loaded on initialization

    def load_weeks(self):
        self.week_combo.clear()
        selected_workout = self.workout_combo.currentText()
        # print("Selected workout:", selected_workout)  # Debug print
        if selected_workout:
            weeks = self.custom_workout_data["Workouts"][selected_workout].keys(
            )
            # print("Available weeks:", weeks)  # Debug print
            self.week_combo.addItems(weeks)
            self.load_days()  # Ensure days are loaded on week change

    def load_days(self):
        self.day_combo.clear()
        selected_workout = self.workout_combo.currentText()
        selected_week = self.week_combo.currentText()
        # print("Selected week:", selected_week)  # Debug print
        if selected_workout and selected_week:
            days = self.custom_workout_data["Workouts"][selected_workout][selected_week].keys(
            )
            # print("Available days:", days)  # Debug print
            self.day_combo.addItems(days)
            self.load_workout()  # Ensure workouts are loaded on day change

    def load_workout(self):
        if hasattr(self, 'scroll_layout'):
            self.clear_layout(self.scroll_layout)
        else:
            self.scroll_layout = QVBoxLayout()
        selected_workout = self.workout_combo.currentText()
        selected_week = self.week_combo.currentText()
        selected_day = self.day_combo.currentText()
        # print("Selected day:", selected_day)  # Debug print

        if selected_workout and selected_week and selected_day:
            workout_data = self.custom_workout_data["Workouts"][
                selected_workout][selected_week][selected_day]["Weights"]
            # print("Workout data for selected day:", workout_data)  # Debug print

            for exercise in workout_data:
                exercise_widget = QWidget()
                exercise_layout = QVBoxLayout(exercise_widget)

                exercise_label = QLabel(f"{exercise['exercise']}")
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

                    set_details_layout.addRow(
                        f"Set {i + 1} Weight:", weight_spinbox)
                    set_details_layout.addRow(
                        f"Set {i + 1} Reps:", reps_spinbox)

                    weight_spinbox.valueChanged.connect(
                        self.update_total_volume)
                    reps_spinbox.valueChanged.connect(self.update_total_volume)

                    total_volume += weight_spinbox.value() * reps_spinbox.value()

                volume_label = QLabel(f"Total Volume: {total_volume:.2f} kg")
                volume_label.setObjectName("volume_label")
                exercise_layout.addLayout(set_details_layout)
                exercise_layout.addWidget(volume_label)
                # exercise_layout.addLayout(set_details_layout)

                self.scroll_layout.addWidget(exercise_widget)

    def update_total_volume(self):
        for i in range(self.scroll_layout.count()):
            exercise_widget = self.scroll_layout.itemAt(i).widget()
            if exercise_widget:
                set_details_layout = exercise_widget.layout().itemAt(1).layout()
                total_volume = 0
                for j in range(0, set_details_layout.rowCount(), 2):
                    weight_spinbox = set_details_layout.itemAt(
                        j, QFormLayout.FieldRole).widget()
                    reps_spinbox = set_details_layout.itemAt(
                        j + 1, QFormLayout.FieldRole).widget()
                    if weight_spinbox and reps_spinbox:
                        total_volume += weight_spinbox.value() * reps_spinbox.value()
                volume_label = exercise_widget.layout().itemAt(2).widget()
                volume_label.setText(f"Total Volume: {total_volume:.2f} kg")

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget_to_remove = layout.itemAt(i).widget()
            layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

    def save_to_database(self):
        user = self.user_combo.currentText()
        if not user:
            QMessageBox.warning(self, "Warning", "Please select a user.")
            return

        date = self.date_edit.date().toString("yyyy-MM-dd")

        headers, user_id_query = self.engine.execute_query(
            "SELECT id FROM users WHERE name = :name", {":name": user})
        if user_id_query:
            user_id = user_id_query[0][0]
            selected_workout = self.workout_combo.currentText()
            selected_week = self.week_combo.currentText()
            selected_day = self.day_combo.currentText()

            if selected_workout and selected_week and selected_day:
                workout_data = self.custom_workout_data["Workouts"][
                    selected_workout][selected_week][selected_day]["Weights"]

                for i in range(self.scroll_layout.count()):
                    exercise_widget = self.scroll_layout.itemAt(i).widget()
                    if exercise_widget:
                        exercise_name = exercise_widget.layout().itemAt(0).widget().text()
                        set_details_layout = exercise_widget.layout().itemAt(1).layout()
                        sets = set_details_layout.rowCount() // 2
                        weights_reps = {}
                        volume = 0

                        for j in range(sets):
                            weight_spinbox = set_details_layout.itemAt(
                                j * 2, QFormLayout.FieldRole).widget()
                            reps_spinbox = set_details_layout.itemAt(
                                j * 2 + 1, QFormLayout.FieldRole).widget()
                            weight = weight_spinbox.value()
                            reps = reps_spinbox.value()
                            volume += weight * reps
                            weights_reps[f"set{j + 1}_weight"] = weight
                            weights_reps[f"set{j + 1}_reps"] = reps

                        weights_reps = {f"set{j + 1}_weight": weights_reps.get(f"set{j + 1}_weight", None) for j in
                                        range(5)} | \
                                       {f"set{j + 1}_reps": weights_reps.get(f"set{j + 1}_reps", None) for j in
                                        range(5)}

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

                QMessageBox.information(
                    self, "Success", "Workout saved to database.")
            else:
                QMessageBox.critical(self, "Error", "User not found.")
