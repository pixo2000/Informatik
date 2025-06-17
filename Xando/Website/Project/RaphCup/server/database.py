import sqlite3
import datetime
from config import DATABASE_CONFIG

class Database:
    def __init__(self):
        self.db_name = DATABASE_CONFIG['name']
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        conn = self.get_connection()
        c = conn.cursor()
        
        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            password TEXT,
            verified BOOLEAN DEFAULT FALSE,
            verification_code TEXT,
            verification_expires TEXT,
            reset_token TEXT,
            reset_expires TEXT,
            is_admin BOOLEAN DEFAULT FALSE,
            discord_tag TEXT,
            valorant_rank TEXT,
            valorant_peak TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Tournaments table
        c.execute('''CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            date1 TEXT,
            date2 TEXT,
            final_date TEXT,
            registration_deadline TEXT,
            max_players INTEGER,
            created_by INTEGER,
            status TEXT DEFAULT 'upcoming',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )''')
        
        # Tournament registrations
        c.execute('''CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY,
            tournament_id INTEGER,
            user_id INTEGER,
            date_vote TEXT,
            registered_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(tournament_id, user_id)
        )''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, email, password_hash, verification_code, verification_expires):
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO users (email, password, verification_code, verification_expires) 
                         VALUES (?, ?, ?, ?)''',
                      (email, password_hash, verification_code, verification_expires))
            conn.commit()
            return c.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_user_by_email(self, email):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        return user
    
    def verify_user(self, email):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('UPDATE users SET verified = TRUE, verification_code = NULL, verification_expires = NULL WHERE email = ?', (email,))
        conn.commit()
        conn.close()
    
    def set_reset_token(self, email, reset_token, reset_expires):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('UPDATE users SET reset_token = ?, reset_expires = ? WHERE email = ?',
                  (reset_token, reset_expires, email))
        conn.commit()
        conn.close()
    
    def get_user_by_reset_token(self, reset_token):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE reset_token = ?', (reset_token,))
        user = c.fetchone()
        conn.close()
        return user
    
    def update_password(self, user_id, new_password_hash):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('UPDATE users SET password = ?, reset_token = NULL, reset_expires = NULL WHERE id = ?',
                  (new_password_hash, user_id))
        conn.commit()
        conn.close()
    
    def get_tournaments(self, status='upcoming'):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM tournaments WHERE status = ? ORDER BY date1', (status,))
        tournaments = c.fetchall()
        conn.close()
        return tournaments
    
    def create_tournament(self, name, description, date1, date2, registration_deadline, max_players, created_by):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO tournaments 
                     (name, description, date1, date2, registration_deadline, max_players, created_by)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (name, description, date1, date2, registration_deadline, max_players, created_by))
        conn.commit()
        tournament_id = c.lastrowid
        conn.close()
        return tournament_id
    
    def register_for_tournament(self, tournament_id, user_id, date_vote):
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO registrations (tournament_id, user_id, date_vote) VALUES (?, ?, ?)',
                      (tournament_id, user_id, date_vote))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def update_user_profile(self, user_id, discord_tag, valorant_rank, valorant_peak):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('UPDATE users SET discord_tag = ?, valorant_rank = ?, valorant_peak = ? WHERE id = ?',
                  (discord_tag, valorant_rank, valorant_peak, user_id))
        conn.commit()
        conn.close()

# Global database instance
db = Database()
