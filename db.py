import sqlite3
import os

# Set the database path: use /tmp if running on Streamlit Cloud, else use local data folder.
if os.environ.get("STREAMLIT_CLOUD"):
    DB_PATH = "/tmp/emissions.db"
else:
    DB_PATH = "data/emissions.db"
    os.makedirs("data", exist_ok=True)  # Ensure local folder exists

def init_db():
    """Initialize the database and create necessary tables if they don't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        # Create the transport_data table
        c.execute('''CREATE TABLE IF NOT EXISTS transport_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        transport_mode TEXT NOT NULL,
                        distance REAL NOT NULL)''')

        # Create the food_choices table
        c.execute('''CREATE TABLE IF NOT EXISTS food_choices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        dietary_pattern TEXT NOT NULL,
                        food_item TEXT NOT NULL)''')

        # Create contact_messages table
        c.execute('''CREATE TABLE IF NOT EXISTS contact_messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        message TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

        conn.commit()
        print("[DEBUG] Database initialized successfully at:", DB_PATH)

def store_transport_data(session_id, transport_mode, distance):
    """Store transport data for the user session."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO transport_data (session_id, transport_mode, distance) 
                     VALUES (?, ?, ?)''', (session_id, transport_mode, distance))
        conn.commit()  
        print(f"[DEBUG] Inserted transport data: {session_id}, {transport_mode}, {distance}")

def store_food_data(session_id, dietary_pattern, food_choices):
    """Store food choices for the user session."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        for food_item in food_choices:  
            c.execute('''INSERT INTO food_choices (session_id, dietary_pattern, food_item) 
                         VALUES (?, ?, ?)''', (session_id, dietary_pattern, food_item))
        conn.commit()
        print(f"[DEBUG] Inserted food choices: {food_choices} for session: {session_id}")

def store_message(name, message):
    """Save a user's contact message to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO contact_messages (name, message) VALUES (?, ?)", (name, message))
        conn.commit()
        print(f"[DEBUG] Stored message from {name}")
