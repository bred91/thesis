import logging
import sqlite3
from datetime import datetime

class SQLiteHandler(logging.Handler):
    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path

    def emit(self, record):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        log_entry = self.format(record)
        cursor.execute("""
            INSERT INTO logs (created, level, message) 
            VALUES (?, ?, ?)
        """, (datetime.fromtimestamp(record.created).isoformat(), record.levelname, log_entry))

        conn.commit()
        conn.close()
