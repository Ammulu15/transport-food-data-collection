import sqlite3

# Initialize Database
def init_db():
    conn = sqlite3.connect("data/emissions.db")
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    
    # Transport data table (emissions column allows NULL values)
    c.execute('''
        CREATE TABLE IF NOT EXISTS transport_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            transport_mode TEXT,
            distance REAL,
            emissions REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Food choices table
    c.execute('''
        CREATE TABLE IF NOT EXISTS food_choices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            choice TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Register User
def register_user(name, email, password):
    conn = sqlite3.connect("data/emissions.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email already exists
    finally:
        conn.close()

# Authenticate User (Login)
def authenticate_user(email, password):
    conn = sqlite3.connect("data/emissions.db")
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None  # Return user ID if exists

# Get Logged-in User ID
def get_logged_in_user_id(email):
    conn = sqlite3.connect("data/emissions.db")
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

# Update Password (Forgot Password)
def update_password(email, new_password):
    conn = sqlite3.connect("data/emissions.db")
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
    conn.commit()
    updated = c.rowcount > 0  # True if update was successful
    conn.close()
    return updated

# Store Transport Data (emissions is optional and allowed to be NULL)
def store_transport_data(user_id, transport_mode, distance, emissions=None):
    conn = sqlite3.connect("data/emissions.db")
    c = conn.cursor()
    c.execute("INSERT INTO transport_data (user_id, transport_mode, distance, emissions) VALUES (?, ?, ?, ?)",
              (user_id, transport_mode, distance, emissions))
    conn.commit()
    conn.close()

# Store Food Choices
def store_food_choice(user_id, choice):
    conn = sqlite3.connect("data/emissions.db")
    c = conn.cursor()
    c.execute("INSERT INTO food_choices (user_id, choice) VALUES (?, ?)", (user_id, choice))
    conn.commit()
    conn.close()