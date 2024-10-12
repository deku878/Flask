import sqlite3
import os

# Path to the database file
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database.db'))

# Connect to the SQLite database
connection = sqlite3.connect(db_path)

# Read and execute the schema SQL script to create the 'posts' table
with open('schema.sql') as f:
    connection.executescript(f.read())

# Insert some initial data into the 'posts' table
cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", 
            ('First Post', 'Content for the first post'))
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", 
            ('Second Post', 'Content for the second post'))

# Commit the changes and close the connection
connection.commit()
connection.close()

print(f"Database initialized at {db_path}")
