import sqlite3
import os

def init_db():
    """Initialize the SQLite database with required tables"""
    # Get the database path - moviemagic.db is in the root folder
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'moviemagic.db')
    
    print(f"Initializing database at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Create Bookings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id TEXT PRIMARY KEY,
            movie_name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            theater TEXT NOT NULL,
            address TEXT NOT NULL,
            booked_by TEXT NOT NULL,
            user_name TEXT NOT NULL,
            seats TEXT NOT NULL,
            amount_paid TEXT NOT NULL,
            booking_time TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()

