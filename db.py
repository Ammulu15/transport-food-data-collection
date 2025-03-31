import sqlite3
import os

# Ensure the database directory exists
os.makedirs("data", exist_ok=True)

def init_db():
    """Initialize the database and create necessary tables if they don't exist."""
    with sqlite3.connect("data/emissions.db") as conn:
        c = conn.cursor()

        

        # Create the transport_data table with session_id
        c.execute('''CREATE TABLE IF NOT EXISTS transport_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        transport_mode TEXT NOT NULL,
                        distance REAL NOT NULL)''')

        # Create the food_choices table with session_id
        c.execute('''CREATE TABLE IF NOT EXISTS food_choices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        dietary_pattern TEXT NOT NULL,
                        food_item TEXT NOT NULL)''')

        conn.commit()
        # Create contact messages table
        c.execute('''CREATE TABLE IF NOT EXISTS contact_messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        message TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

        conn.commit()
def store_transport_data(session_id, transport_mode, distance):
    """Store transport data for the user session."""
    with sqlite3.connect('data/emissions.db') as conn:
        c = conn.cursor()
        # Insert transport data with session_id
        c.execute('''INSERT INTO transport_data (session_id, transport_mode, distance) 
                     VALUES (?, ?, ?)''', (session_id, transport_mode, distance))
        conn.commit()  # Ensure data is committed
        print(f"Inserted transport data: {session_id}, {transport_mode}, {distance}")  # Debug line

def store_food_data(session_id, dietary_pattern, food_choices):
    """Store food choices for the user session."""
    with sqlite3.connect('data/emissions.db') as conn:
        c = conn.cursor()
        for food_item in food_choices:  # Insert each food item separately
            c.execute('''INSERT INTO food_choices (session_id, dietary_pattern, food_item) 
                         VALUES (?, ?, ?)''', (session_id, dietary_pattern, food_item))
        conn.commit()

        print(f"Inserted food choices: {food_choices} for session: {session_id}")  # Debug line
def store_message(name, message):
    """Save a user's contact message to the database."""
    with sqlite3.connect("data/emissions.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO contact_messages (name, message) VALUES (?, ?)", (name, message))
        conn.commit()