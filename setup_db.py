import sqlite3

# Connect to a new database file called tutor.db
conn = sqlite3.connect('tutor.db')
cursor = conn.cursor()

# Make a table for chats (questions and answers)
cursor.execute('''CREATE TABLE IF NOT EXISTS chats
(id INTEGER PRIMARY KEY AUTOINCREMENT,
message TEXT,
response TEXT)''')

# Make a table for progress (points for students)
cursor.execute('''CREATE TABLE IF NOT EXISTS progress
(id INTEGER PRIMARY KEY AUTOINCREMENT,
points INTEGER)''')

# Save everything and close
conn.commit()
conn.close()

print("Database created!")