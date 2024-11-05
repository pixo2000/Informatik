import sqlite3

def setup_database():
    # Establish a connection to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create a table for storing user information
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
    print("Database setup complete.")

# Run the setup when this script is executed
if __name__ == "__main__":
    setup_database()
