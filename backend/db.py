import mysql.connector
from mysql.connector import Error
import bcrypt
import config

class UserAuth:
    def __init__(self):
        """Establish a connection to the database using config settings."""
        try:
            self.connection = mysql.connector.connect(
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(buffered=True)
                print("Connected to MySQL database")
        except Error as e:
            print(f"Database connection error: {e}")
            self.connection = None

    def register_user(self, email, password):
        """Register a new user with a hashed password."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            query = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
            # Store the hash as a string (decode the bytes)
            self.cursor.execute(query, (email, hashed_password.decode('utf-8')))
            self.connection.commit()
            return True, "Account Created"
        except Error as e:
            # You might want to check for duplicate key errors here
            return False, f"Account creation failed: {e}"

    def login_user(self, email, password):
        """Verify login credentials; returns success flag and message."""
        try:
            query = "SELECT password_hash FROM users WHERE email = %s"
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                return True, "Login successful"
            else:
                return False, "Invalid credentials"
        except Error as e:
            return False, f"Login failed: {e}"

    def close(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")