from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlError


class DBHandler:
    _instance = None

    def __new__(cls, db_name):
        if cls._instance is None:
            cls._instance = super(DBHandler, cls).__new__(cls)
            cls._instance._init_db(db_name)
        return cls._instance

    def _init_db(self, db_name):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_name)
        if not self.db.open():
            raise Exception(f"Database Error: {self.db.lastError().text()}")
        # print("Database connection established.")

    def create_tables(self):
        query = QSqlQuery()
        success = query.exec("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """)
        # print(f"Creating users table: {'Success' if success else 'Failure'} - {query.lastError().text()}")

        success = query.exec("""
        CREATE TABLE IF NOT EXISTS weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            user_id INTEGER,
            exercise TEXT,
            set1_weight REAL,
            set1_reps INTEGER,
            set2_weight REAL,
            set2_reps INTEGER,
            set3_weight REAL,
            set3_reps INTEGER,
            set4_weight REAL,
            set4_reps INTEGER,
            set5_weight REAL,
            set5_reps INTEGER,
            volume REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        # print(f"Creating weights table: {'Success' if success else 'Failure'} - {query.lastError().text()}")

        success = query.exec("""
        CREATE TABLE IF NOT EXISTS cardio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            user_id INTEGER,
            distance REAL,
            time TEXT,
            max_hr INTEGER,
            avg_hr INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        # print(f"Creating cardio table: {'Success' if success else 'Failure'} - {query.lastError().text()}")

        success = query.exec("""
        CREATE TABLE IF NOT EXISTS conditioning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            user_id INTEGER,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        # print(f"Creating conditioning table: {'Success' if success else 'Failure'} - {query.lastError().text()}")

        success = query.exec("""
        CREATE TABLE IF NOT EXISTS technical (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            user_id INTEGER,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        # print(f"Creating technical table: {'Success' if success else 'Failure'} - {query.lastError().text()}")

        success = query.exec("""
        CREATE TABLE IF NOT EXISTS biometric_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            date TEXT,
            height REAL,
            weight REAL,
            shoulders REAL,
            chest REAL,
            upper_arm_left REAL,
            upper_arm_right REAL,
            forearm_left REAL,
            forearm_right REAL,
            waist REAL,
            hips REAL,
            upper_leg_left REAL,
            upper_leg_right REAL,
            calf_left REAL,
            calf_right REAL
        )
        """)
        # print(f"Creating biometric_data table: {'Success' if success else 'Failure'} - {query.lastError().text()}")

    def execute_query(self, query_text, params=None):
        if not self.db.isOpen():
            raise Exception("Database is not open")

        query = QSqlQuery()
        query.prepare(query_text)
        # print(f"Executing Query: {query_text}")
        if params:
            for key, value in params.items():
                query.bindValue(key, value)
                # print(f"Binding: {key} -> {value}")
        if not query.exec():
            error = query.lastError()
            # print(f"Query Error: {error.text()}")
            raise Exception(f"Query Error: {error.text()}")
        return query

    def fetch_all(self, query_text, params=None):
        query = self.execute_query(query_text, params)
        results = []
        while query.next():
            row = []
            for col in range(query.record().count()):
                row.append(query.value(col))
            results.append(row)
        return results
