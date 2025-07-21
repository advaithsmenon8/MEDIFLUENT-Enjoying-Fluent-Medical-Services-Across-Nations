import sqlite3
from werkzeug.security import generate_password_hash

# Connect to SQLite database (this will create the database file if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Sample user details
email = 'user@example.com'
password = 'password123'  # Use a sample password (will be hashed)

# Hash the password using werkzeug's generate_password_hash
hashed_password = generate_password_hash(password)

# Insert the sample user into the users table
cursor.execute('''
    INSERT OR IGNORE INTO users (email, password) VALUES (?, ?)
''', (email, hashed_password))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Sample user added successfully.")
