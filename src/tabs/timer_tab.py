import json
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox
from pygame import mixer


class BoxingTimer(QWidget):
    def __init__(self):
        super().__init__()
        mixer.init()
        self.setWindowTitle("Boxing Round Timer")

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        font = QFont()
        font.setPointSize(8)
        # Left layout for controls
        self.controls_layout = QVBoxLayout()
        self.controls_layout.setContentsMargins(0, 0, 0, 0)

        self.workout_label = QLabel("Select Workout:")
        self.workout_label.setAlignment(Qt.AlignCenter)
        self.workout_label.setMaximumWidth(150)
        self.workout_selector = QComboBox()
        self.workout_selector.setObjectName("workout_selector")
        self.workout_selector.setMaximumWidth(150)
        self.workout_selector.setFont(font)

        self.controls_layout.addWidget(self.workout_label)
        self.controls_layout.addWidget(self.workout_selector)

        self.round_number_label = QLabel("Round Number:")
        self.round_number_label.setMaximumWidth(150)
        self.round_number_label.setAlignment(Qt.AlignCenter)
        self.round_number_input = QLineEdit()
        self.round_number_input.setMaximumWidth(150)
        self.round_number_input.setAlignment(Qt.AlignCenter)

        self.controls_layout.addWidget(self.round_number_label)
        self.controls_layout.addWidget(self.round_number_input)

        self.round_length_label = QLabel("Round Length(s):")
        self.round_length_label.setAlignment(Qt.AlignCenter)
        self.round_length_label.setMaximumWidth(150)
        self.round_length_input = QLineEdit()
        self.round_length_input.setAlignment(Qt.AlignCenter)
        self.round_length_input.setMaximumWidth(150)

        self.controls_layout.addWidget(self.round_length_label)
        self.controls_layout.addWidget(self.round_length_input)

        self.rest_time_label = QLabel("Rest Time(s):")
        self.rest_time_label.setAlignment(Qt.AlignCenter)
        self.rest_time_label.setMaximumWidth(150)
        self.rest_time_input = QLineEdit()
        self.rest_time_input.setAlignment(Qt.AlignCenter)
        self.rest_time_input.setMaximumWidth(150)

        self.controls_layout.addWidget(self.rest_time_label)
        self.controls_layout.addWidget(self.rest_time_input)

        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("timer_start_btn")
        self.pause_button = QPushButton("Pause")
        self.pause_button.setObjectName("timer_pause_btn")
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("timer_reset_btn")

        self.controls_layout.addWidget(self.start_button)
        self.controls_layout.addWidget(self.pause_button)
        self.controls_layout.addWidget(self.reset_button)

        main_layout.addLayout(self.controls_layout)

        # Right layout for display
        self.display_layout = QVBoxLayout()

        self.timer_display = QLabel("Time Remaining:\n00:00")
        self.timer_display.setStyleSheet("font-size: 60px; color: #50fa7b;")
        self.timer_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display_layout.addWidget(self.timer_display)

        self.round_info_display = QLabel("Rounds Remaining:\n1")
        self.round_info_display.setStyleSheet("font-size: 30px; color: #bd93f9")
        self.round_info_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display_layout.addWidget(self.round_info_display)

        self.exercise_display = QLabel("Exercise:\n--")
        self.exercise_display.setStyleSheet("font-size: 40px; color:#ffb86c ")
        self.exercise_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display_layout.addWidget(self.exercise_display)

        main_layout.addLayout(self.display_layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # Timer state
        self.time_remaining = 0
        self.round_number = 1
        self.in_rest = False
        self.is_paused = False
        self.current_exercise_index = 0

        # Load workouts
        self.workouts = []
        self.load_workouts()

        # Connect buttons to functions
        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.reset_button.clicked.connect(self.reset_timer)
        self.workout_selector.currentTextChanged.connect(self.load_selected_workout)

        # Populate workout selector
        self.populate_workout_selector()



    def start_timer(self):
        self.time_remaining = int(self.round_length_input.text())
        self.round_number = int(self.round_number_input.text())
        self.in_rest = False
        self.is_paused = False
        self.current_exercise_index = 0
        self.update_display()
        self.timer.start(1000)
        self.play_sound("round_start")

    def pause_timer(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.timer.stop()
        else:
            self.timer.start(1000)

    def reset_timer(self):
        self.timer.stop()
        self.time_remaining = 0
        self.update_display()

    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_display()
        else:
            if not self.in_rest:
                self.in_rest = True
                self.time_remaining = int(self.rest_time_input.text())
                self.play_sound("rest_start")
            else:
                self.in_rest = False
                self.current_exercise_index += 1
                if self.current_exercise_index < len(self.workouts[self.current_workout_index]["exercises"]):
                    self.time_remaining = int(
                        self.workouts[self.current_workout_index]["exercises"][self.current_exercise_index][
                            "round_time"])
                    self.round_number -= 1
                    self.play_sound("round_start")
                else:
                    self.timer.stop()

    def update_display(self):
        minutes, seconds = divmod(self.time_remaining, 60)
        self.timer_display.setText(f"Time Remaining:\n{minutes:02d}:{seconds:02d}")
        self.round_info_display.setText(f"Rounds Remaining:\n{self.round_number}")
        if self.current_exercise_index < len(self.workouts[self.current_workout_index]["exercises"]):
            current_exercise = self.workouts[self.current_workout_index]["exercises"][self.current_exercise_index][
                "exercise"]
        else:
            current_exercise = "--"
        self.exercise_display.setText("Resting" if self.in_rest else f"Exercise:\n{current_exercise}")

    def play_sound(self, sound_type):
        if sound_type == "round_start":
            mixer.music.load("data/sounds/coin-recieved-230517.mp3")
            mixer.music.play()
        elif sound_type == "rest_start":
            mixer.music.load("data/sounds/achievement-video-game-type-1-230515.mp3")
            mixer.music.play()
        elif sound_type == "round_end":
            mixer.music.load("data/sounds/power-up-type-1-230548.mp3")
            mixer.music.play()

    def populate_workout_selector(self):
        self.workout_selector.clear()
        for workout in self.workouts:
            self.workout_selector.addItem(workout["name"])

    def load_workouts(self, filename="data/json/timer_workouts.json"):
        
        try:
            with open(filename, "r") as file:
                self.workouts = json.load(file)
                
        except FileNotFoundError:
            self.workouts = []

    def load_selected_workout(self):
        selected_workout = self.workout_selector.currentText()
        self.current_workout_index = -1
        for index, workout in enumerate(self.workouts):
            if workout["name"] == selected_workout:
                self.current_workout_index = index
                self.round_number_input.setText(str(len(workout["exercises"])))
                self.round_length_input.setText(str(workout["exercises"][0]["round_time"]))
                self.rest_time_input.setText(str(workout["exercises"][0]["rest_time"]))
                break


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = BoxingTimer()
    window.show()
    sys.exit(app.exec())
