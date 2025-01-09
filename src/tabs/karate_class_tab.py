import json
import random
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QScrollArea, QSlider, QHBoxLayout
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl, QDir


class KarateClassDocument(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.generate_button = QPushButton('Generate Document')
        self.generate_button.setObjectName('generate_btn')
        self.output_button = QPushButton('Output to File')
        self.output_button.setObjectName('save_btn')
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.scroll_area.setWidget(self.content_widget)

        self.generate_button.clicked.connect(self.generate_document)
        self.output_button.clicked.connect(self.output_to_file)

        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.output_button)
        self.layout.addWidget(self.scroll_area)

        self.setLayout(self.layout)

    def read_json_data(self):
        with open('data/json/karate_data.json', 'r') as file:
            data = json.load(file)
        return data

    def generate_document(self):
        data = self.read_json_data()
        self.clear_content()

        title_label = QLabel("Karate Class")
        title_label.setStyleSheet("""
            color: #d33682;
            text-align: center;
            font-size: 24px;
        """)
        self.content_layout.addWidget(title_label)

        for category, items in data.items():
            category_label = QLabel(category)
            category_label.setStyleSheet("""
                color: #2aa198;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5px;
                font-size: 18px;
            """)
            self.content_layout.addWidget(category_label)

            item = random.choice(items)
            name_label = QLabel(item['name'])
            name_label.setStyleSheet("""
                color: #268bd2;
                font-size: 16px;
            """)
            description_label = QLabel(item['description'])
            description_label.setStyleSheet("""
                margin-bottom: 10px;
                font-size: 14px;
            """)
            self.content_layout.addWidget(name_label)
            self.content_layout.addWidget(description_label)

            if 'video_link' in item:
                video_button = QPushButton('Play Video')
                video_button.setFixedSize(100, 30)
                video_button.clicked.connect(lambda _, url=item['video_link']: self.open_video_link(url))
                self.content_layout.addWidget(video_button)

    def clear_content(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def open_video_link(self, video_filename):
        video_path = QDir.current().filePath(f"{video_filename}")
        if os.path.exists(video_path):
            player_window = VideoPlayerWindow(video_path)
            player_window.show()
        else:
            QMessageBox.warning(self, "Warning", f"Video file not found: {video_filename}")

    def output_to_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Document", "", "HTML Files (*.html);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                html_content = self.generate_html_content()
                file.write(html_content)

    def generate_html_content(self):
        data = self.read_json_data()
        document_content = """
        <html>
        <head>
        <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #d33682;
            text-align: center;
        }
        h2 {
            color: #2aa198;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }
        h3 {
            color: #268bd2;
        }
        p {
            margin-bottom: 10px;
        }
        </style>
        </head>
        <body>
        <h1>Karate Class</h1>
        """

        for category, items in data.items():
            document_content += f"<h2>{category}</h2>"
            item = random.choice(items)
            document_content += f"<h3>{item['name']}</h3>"
            document_content += f"<p>{item['description']}</p>"
            if 'video_link' in item:
                document_content += f"<p>Video Link: {item['video_link']}</p>"

        document_content += "</body></html>"
        return document_content


class VideoPlayerWindow(QWidget):
    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.video_widget = QVideoWidget(self)

        # Ensure URL is valid
        url = QUrl.fromLocalFile(video_path)
        if not url.isValid():
            QMessageBox.critical(self, "Error", f"Invalid video path: {video_path}")
            return

        self.media_player.setSource(url)
        self.media_player.setVideoOutput(self.video_widget)

        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)

        self.play_button.clicked.connect(self.media_player.play)
        self.pause_button.clicked.connect(self.media_player.pause)
        self.stop_button.clicked.connect(self.media_player.stop)
        self.volume_slider.valueChanged.connect(lambda value: self.audio_output.setVolume(value / 100.0))

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(QLabel("Volume"))
        control_layout.addWidget(self.volume_slider)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_widget)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)

        # Connect to error signal
        self.media_player.errorOccurred.connect(self.handle_error)

    def closeEvent(self, event):
        self.media_player.stop()
        event.accept()

    def handle_error(self, error):
        QMessageBox.critical(self, "Error", f"Media Player Error: {self.media_player.errorString()}")


if __name__ == '__main__':
    app = QApplication([])
    window = KarateClassDocument()
    window.show()
    app.exec()
