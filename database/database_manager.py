import sqlite3
import os

class DatabaseManager:
    """Manages SQLite database connections and schema setup."""
    
    def __init__(self, db_path="data/pc_smart.db"):
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.initialize_database()

    def get_connection(self):
        """Returns a new database connection."""
        return sqlite3.connect(self.db_path)

    def initialize_database(self):
        """Creates required tables for users and system logs."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            
            # System logs table for history and analytics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    cpu_usage REAL,
                    ram_usage REAL,
                    disk_usage REAL,
                    timestamp TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            conn.commit()