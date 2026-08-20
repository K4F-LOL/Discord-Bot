import sqlite3
from datetime import datetime

class TicketDatabase:
    def __init__(self, db_path="tickets.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_channel_id INTEGER,
                user_id INTEGER,
                username TEXT,
                problem TEXT,
                status TEXT,
                created_at TEXT,
                closed_at TEXT,
                closed_by INTEGER,
                assigned_to INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_ticket(self, channel_id, user_id, username, problem):
        # Open connection to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert the ticket data into the table
        cursor.execute('''
            INSERT INTO tickets (ticket_channel_id, user_id, username, problem, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (channel_id, user_id, username, problem, "open", datetime.utcnow().isoformat()))
        
        conn.commit()
        conn.close()
    
    def close_ticket(self, channel_id, closed_by):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tickets 
            SET status = ?, closed_at = ?, closed_by = ?
            WHERE ticket_channel_id = ?
        ''', ("closed", datetime.utcnow().isoformat(), closed_by, channel_id))
        
        conn.commit()
        conn.close()
    
    def assign_ticket(self, channel_id, assigned_to):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE tickets 
            SET assigned_to = ?
            WHERE ticket_channel_id = ?
        ''', (assigned_to, channel_id))
        
        conn.commit()
        conn.close()