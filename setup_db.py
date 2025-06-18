import sqlite3

# Connect to (or create) chatbot.db
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Create the messages table
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT NOT NULL,
    bot_response TEXT NOT NULL
)
""")

conn.commit()
conn.close()
print("Database and table created successfully.")
