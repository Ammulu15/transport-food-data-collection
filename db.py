import sqlite3

DB_PATH = "data/emissions.db"

def create_table():
    """Create database table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transport_emissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            transport_mode TEXT,
            input_type TEXT,
            value REAL,
            frequency INTEGER,
            travel_date TEXT,
            emissions REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_data(name, transport_mode, input_type, value, frequency, travel_date, emissions):
    """Insert transport data into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transport_emissions (name, transport_mode, input_type, value, frequency, travel_date, emissions)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, transport_mode, input_type, value, frequency, travel_date, emissions))
    conn.commit()
    conn.close()
