# import json
# from PySide6.QtSql import QSqlQuery, QSqlError


# class Engine:
#     def __init__(self, db_handler):
#         self.db_handler = db_handler

#     def load_users(self):
#         headers, users = self.execute_query("SELECT name FROM users")
#         return [user[0] for user in users if user]

#     def execute_query(self, query_text, params=None):
#         # print(f"Executing Query: {query_text} with Params: {params}")  # Debug print
#         query = QSqlQuery()
#         query.prepare(query_text)
#         if params:
#             for key, value in params.items():
#                 query.bindValue(key, value)
#         if not query.exec():
#             # print(f"Query Error: {query.lastError().text()}")
#             raise Exception(f"Query Error: {query.lastError().text()}")

#         headers = []
#         results = []
#         for index in range(query.record().count()):
#             headers.append(query.record().fieldName(index))

#         while query.next():
#             row = []
#             for col in range(query.record().count()):
#                 row.append(query.value(col))
#             results.append(row)

#         # print(f"Query Headers: {headers}, Results: {results}")  # Enhanced Debug print
#         return headers, results

#     def export_user_data(self, user_id, output_file):
#         query_text = """
#         SELECT * FROM weights WHERE user_id = :user_id
#         UNION ALL
#         SELECT * FROM cardio WHERE user_id = :user_id
#         UNION ALL
#         SELECT * FROM conditioning WHERE user_id = :user_id
#         UNION ALL
#         SELECT * FROM technical WHERE user_id = :user_id
#         UNION ALL
#         SELECT * FROM biometric_data WHERE user = (SELECT name FROM users WHERE id = :user_id)
#         """
#         params = {":user_id": user_id}
#         headers, data = self.execute_query(query_text, params)

#         with open(output_file, 'w') as file:
#             file.write(','.join(headers) + '\n')
#             for row in data:
#                 file.write(','.join(map(str, row)) + '\n')
#         # print(f"User data exported to {output_file}")

import csv
#     def load_random_workouts(self):
#         with open("data/random_workouts.json", "r") as file:
#             data = json.load(file)
#         exercises = []
#         for body_part, exercises_list in data.items():
#             for exercise in exercises_list:
#                 exercise['body_part'] = body_part
#                 exercises.append(exercise)
#         return exercises
import json

from PySide6.QtSql import QSqlQuery


class Engine:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def load_users(self):
        headers, users = self.execute_query("SELECT name FROM users")
        return [user[0] for user in users if user]

    @staticmethod
    def execute_query(query_text, params=None):
        query = QSqlQuery()
        query.prepare(query_text)
        if params:
            for key, value in params.items():
                query.bindValue(key, value)
        if not query.exec():
            raise Exception(f"Query Error: {query.lastError().text()}")

        headers = []
        results = []
        for index in range(query.record().count()):
            headers.append(query.record().fieldName(index))

        while query.next():
            row = []
            for col in range(query.record().count()):
                row.append(query.value(col))
            results.append(row)

        return headers, results

    def export_user_data(self, user_id, output_file):
        query_text = """
        SELECT * FROM weights WHERE user_id = :user_id
        UNION ALL
        SELECT * FROM cardio WHERE user_id = :user_id
        UNION ALL
        SELECT * FROM conditioning WHERE user_id = :user_id
        UNION ALL
        SELECT * FROM technical WHERE user_id = :user_id
        UNION ALL
        SELECT * FROM biometric_data WHERE user = (SELECT name FROM users WHERE id = :user_id)
        """
        params = {":user_id": user_id}
        headers, data = self.execute_query(query_text, params)

        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write headers
            for row in data:
                writer.writerow(row)  # Write data rows

    @staticmethod
    def load_random_workouts():
        with open("data/json/random_workouts.json", "r") as file:
            data = json.load(file)
        exercises = []
        for body_part, exercises_list in data.items():
            for exercise in exercises_list:
                exercise['body_part'] = body_part
                exercises.append(exercise)
        return exercises
