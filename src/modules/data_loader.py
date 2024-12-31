import json

class DataLoader:
    def __init__(self, json_file):
        self.json_file = json_file
        self.load_data()

    def load_data(self):
        try:
            with open(self.json_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            raise Exception(f"JSON file '{self.json_file}' not found")

    def get_data(self):
        return self.data
