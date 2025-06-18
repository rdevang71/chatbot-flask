import sqlite3

def init_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            bot_response TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def load_data_into_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    with open("data.txt", "r", encoding="utf-8") as file:
        for line in file:
            cursor.execute("INSERT INTO messages (user_input, bot_response) VALUES (?, ?)", (line.strip(), "Default Response"))

    conn.commit()
    conn.close()

# Initialize database and load sample data
init_db()
load_data_into_db()
print("Database initialized with predefined responses.")