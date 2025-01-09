import json
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog


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
        self.text_edit = QTextEdit()

        self.generate_button.clicked.connect(self.generate_document)
        self.output_button.clicked.connect(self.output_to_file)

        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.output_button)
        self.layout.addWidget(self.text_edit)

        self.setLayout(self.layout)

    def read_json_data(self):
        with open('data/json/karate_data.json', 'r') as file:
            data = json.load(file)
        return data

    def generate_document(self):
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
        a {
            color: #cb4b16;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
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
                document_content += f"<a href='{item['video_link']}'>Video Link</a>"

        document_content += "</body></html>"

        self.text_edit.setHtml(document_content)

    def output_to_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Document", "", "HTML Files (*.html);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.text_edit.toHtml())


if __name__ == '__main__':
    app = QApplication([])
    window = KarateClassDocument()
    window.show()
    app.exec()
