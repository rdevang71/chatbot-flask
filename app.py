from flask import Flask
from routes import chatbot_routes

app = Flask(__name__)

# Register chatbot routes
app.register_blueprint(chatbot_routes)

if __name__ == "__main__":
    app.run(debug=True)