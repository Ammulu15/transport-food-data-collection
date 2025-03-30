import sqlite3

# Initialize the SQLite database and tables
def init_db():
    conn = sqlite3.connect('data/emissions.db')  # Path to the database file
    c = conn.cursor()
    
    # Create Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Create Transport Data table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transport_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            transport_mode TEXT NOT NULL,
            distance REAL NOT NULL,
            emissions REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# Register a new user
def register_user(name, email, password):
    conn = sqlite3.connect('data/emissions.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
    ''', (name, email, password))
    conn.commit()
    conn.close()

# Store transport data in the database
def store_transport_data(user_id, transport_mode, distance, emissions):
    conn = sqlite3.connect('data/emissions.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO transport_data (user_id, transport_mode, distance, emissions)
        VALUES (?, ?, ?, ?)
    ''', (user_id, transport_mode, distance, emissions))
    conn.commit()
    conn.close()

# Calculate emissions based on transport mode and distance
def calculate_emissions(transport_mode, distance):
    emission_factors = {
        "Car": 0.12,  # example emission factor for car in kg CO2 per km
        "Bike": 0.02,
        "Bus": 0.05,
        "Walking": 0
    }
    
    return emission_factors.get(transport_mode, 0) * distance

# Get logged-in user ID (this assumes user email is stored in session)
def get_logged_in_user_id():
    # Simulate getting the user ID from session (replace with actual session management)
    email = "user@example.com"  # This should be dynamically set in a real app
    conn = sqlite3.connect('data/emissions.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ?", (email,))
    user_id = c.fetchone()
    conn.close()
    return user_id[0] if user_id else None
