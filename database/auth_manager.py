from database.database_manager import DatabaseManager
from models.user import User
import sqlite3

class AuthManager:
    """Manages user registration, login authentication, and active sessions."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.current_user = None

    def register_user(self, name, email, password):
        """Registers a new user in the database."""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, password)
                )
                conn.commit()
                return True, "Registration successful."
        except sqlite3.IntegrityError:
            return False, "Email already exists. Please use a different email."

    def login_user(self, email, password):
        """Authenticates credentials and sets the active user session."""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, email, password FROM users WHERE email = ? AND password = ?",
                (email, password)
            )
            row = cursor.fetchone()
            if row:
                self.current_user = User(user_id=row[0], name=row[1], email=row[2], password=row[3])
                return True, f"Welcome back, {row[1]}!"
            return False, "Invalid email or password."

    def logout_user(self):
        """Clears the active user session."""
        self.current_user = None
        return True, "Logged out successfully."