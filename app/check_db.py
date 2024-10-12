import sqlite3
import os

# Path to the database file
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database.db'))

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if the 'posts' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts';")
table_exists = cursor.fetchone()
if table_exists:
    print("Table 'posts' exists.")
else:
    print("Table 'posts' does NOT exist. Please check your schema and initialization script.")

# Check if there is data in the 'posts' table
cursor.execute("SELECT * FROM posts;")
rows = cursor.fetchall()
if rows:
    print(f"Data found in 'posts': {rows}")
else:
    print("No data found in the 'posts' table.")

conn.close()
