import sqlite3
import os

DB_FILE = "user.db"

# remove old db so you always start fresh
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
''')

# Insert a test user with plaintext password
test_username = 'admin'
test_password = 'password'  # stored in plaintext (intentionally insecure!)
cursor.execute(
    'INSERT INTO users (username, password) VALUES (?, ?)',
    (test_username, test_password)
)

conn.commit()
conn.close()
print(f"[+] Database initialized with user: {test_username}/{test_password}")
