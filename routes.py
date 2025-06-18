from flask import Blueprint, request, jsonify
import sqlite3
import chatbot_logic

chatbot_routes = Blueprint("chatbot", __name__)

def get_db_connection():
    """Creates a new SQLite database connection."""
    return sqlite3.connect("chatbot.db")

@chatbot_routes.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Invalid request, missing 'message'"}), 400  # Handle empty or missing input

    user_input = data["message"]
    bot_response = chatbot_logic.get_response(user_input) or "I'm sorry, I couldn't understand that."

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (user_input, bot_response) VALUES (?, ?)", (user_input, bot_response))
        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Improved error handling
    finally:
        conn.close()

    return jsonify({"response": bot_response})

@chatbot_routes.route('/history', methods=['GET'])
def history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_input, bot_response FROM messages")
        messages = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    return jsonify({"history": [{"user_message": msg[0], "bot_response": msg[1]} for msg in messages]})  # Improved JSON format