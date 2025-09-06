import mysql.connector
from mysql.connector import Error
import bcrypt

class UserAuth:
    def __init__(self):
        """Establish a connection to the database."""
        try:
            self.connection = mysql.connector.connect(
                host="db.cs.dal.ca",
                user="hajati", 
                password="hCfFcK659g6mnMGuet5xL3LWm",
                database="hajati"
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")

    def register_user(self, email, password):
        """Registers a new user with a hashed password."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            query = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
            self.cursor.execute(query, (email, hashed_password))
            self.connection.commit()
            print("User registered successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def login_user(self, email, password):
        """Authenticates user login by verifying password."""
        query = "SELECT password_hash FROM users WHERE email = %s"
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            print("Login successful!")
            return True
        else:
            print("Invalid email or password.")
            return False
    
    def get_users(self):
        """Retrieve all users."""
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Connection closed.")
            
    def create_playlist(self, user_id, playlist_name, height, sex):
        """Create a new playlist for a user."""
        query = "INSERT INTO playlists (user_id, playlist_name, height, sex) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (user_id, playlist_name, height, sex))
    
    def get_playlists_by_user(self, user_id):
        """Retrieve all playlists of a specific user."""
        query = "SELECT * FROM playlists WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def delete_playlist(self, playlist_id):
        """Delete a playlist."""
        query = "DELETE FROM playlists WHERE id = %s"
        self.cursor.execute(query, (playlist_id,))

# Example usage
if __name__ == "__main__":
    
    # Connect to MySQL
    db = mysql.connector.connect(
        host="db.cs.dal.ca",
        user="hajati", 
        password="hCfFcK659g6mnMGuet5xL3LWm",
        database="hajati"
    )
    cursor = db.cursor(buffered=True)

    # Read SQL file
    with open("schema.sql", "r") as file:
        sql_script = file.read()

    # Execute SQL script
    for statement in sql_script.split(";"):
        if statement.strip():
            print(f"Executing SQL: {statement}")  # Debugging print
            cursor.execute(statement)

    db.commit()
    cursor.close()
    db.close()
    print("Database setup complete!")
    
    auth = UserAuth()

    # Register a new user
    auth.register_user("test@example.com", "securepassword")
    auth.register_user("test@example.com2", "securepassword2")
    
    # Try logging in
    auth.login_user("test@example.com", "securepassword")
    print(auth.get_users())
    
    auth.create_playlist(1, "its britney bitch", 180, 1)
    print(auth.get_playlists_by_user(1))
    auth.delete_playlist(1)
    print(auth.get_playlists_by_user(1))
    
    
    # Close connection
    auth.close_connection()
