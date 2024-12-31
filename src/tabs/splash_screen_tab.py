from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtCore import Qt

class SplashScreenTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.logo_label = QLabel()
        self.pixmap = QPixmap("data/lbb.png")  # Replace with your logo path
        self.logo_label.setPixmap(self.pixmap)
        # self.logo_label.setScaledContents(True)
        self.logo_label.setAlignment(Qt.AlignCenter)

        version_label = QLabel("Gym app\nVersion 1.0")  # Adjust the version as needed
        version_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        layout.addWidget(version_label, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def resizeEvent(self, event: QResizeEvent):
        # Calculate the new size as 1/3 of the window size while maintaining the aspect ratio
        new_width = self.width() // 2
        new_height = self.height() // 2
        
        # Adjust the new width and height to maintain the aspect ratio
        if self.pixmap.width() > 0 and self.pixmap.height() > 0:
            aspect_ratio = self.pixmap.width() / self.pixmap.height()
            if new_width / new_height > aspect_ratio:
                new_width = int(new_height * aspect_ratio)
            else:
                new_height = int(new_width / aspect_ratio)
        
        scaled_pixmap = self.pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)
        super().resizeEvent(event)
