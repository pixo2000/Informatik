"""
Script to create the first admin user for RaphCup
Run this after setting up the database to create an admin account
"""

import sqlite3
from werkzeug.security import generate_password_hash
import getpass

def create_admin():
    print("=== RaphCup Admin Setup ===")
    
    email = input("Admin E-Mail: ")
    password = getpass.getpass("Admin Passwort: ")
    confirm_password = getpass.getpass("Passwort bestätigen: ")
    
    if password != confirm_password:
        print("Passwörter stimmen nicht überein!")
        return
    
    if len(password) < 6:
        print("Passwort muss mindestens 6 Zeichen lang sein!")
        return
    
    try:
        conn = sqlite3.connect('raphcup.db')
        c = conn.cursor()
        
        # Check if user already exists
        c.execute('SELECT id FROM users WHERE email = ?', (email,))
        if c.fetchone():
            print("Benutzer existiert bereits!")
            return
        
        # Create admin user
        hashed_password = generate_password_hash(password)
        c.execute('''INSERT INTO users 
                     (email, password, verified, is_admin) 
                     VALUES (?, ?, TRUE, TRUE)''',
                  (email, hashed_password))
        
        conn.commit()
        conn.close()
        
        print(f"Admin-Benutzer '{email}' erfolgreich erstellt!")
        print("Sie können sich jetzt als Administrator einloggen.")
        
    except Exception as e:
        print(f"Fehler beim Erstellen des Admin-Benutzers: {e}")

if __name__ == '__main__':
    create_admin()
