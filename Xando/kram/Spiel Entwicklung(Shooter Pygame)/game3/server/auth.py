import sqlite3
import bcrypt


# Hash the password using bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


# Check if the provided password matches the hashed password
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)


# Register a new user
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists.")

    conn.close()


# Authenticate a user
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result and check_password(password, result[0]):
        print("Login successful!")
        return True
    else:
        print("Incorrect username or password.")
        return False

    conn.close()


# Change a user's password
def change_user_password(username, current_password, new_password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result and check_password(current_password, result[0]):
        hashed_password = hash_password(new_password)
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
        conn.commit()
        print(f"Password for user '{username}' updated successfully.")
        return True
    else:
        print("Current password is incorrect.")
        return False

    conn.close()


# Delete a user by username
def delete_user_by_username(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"User '{username}' deleted successfully.")
        return True
    else:
        print(f"User '{username}' not found.")
        return False


# Admin function to reset a user's password
def reset_user_password(username, new_password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    hashed_password = hash_password(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"Password for user '{username}' reset successfully.")
        return True
    else:
        print(f"User '{username}' not found.")
        return False
