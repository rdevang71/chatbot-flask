import json
import nlp_processing

# Load chatbot data
with open("data.json", "r", encoding="utf-8") as file:
    chatbot_data = json.load(file)

def get_response(user_input):
    """Matches user query with chatbot data using NLP."""
    return nlp_processing.find_best_match(user_input)