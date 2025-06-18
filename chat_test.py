import requests

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Chatbot: Goodbye!")
        break

    response = requests.post(
        "http://127.0.0.1:5000/chat",
        json={"message": user_input}
    )

    if response.status_code == 200:
        print("Chatbot:", response.json().get("response"))
    else:
        print("Error:", response.json().get("error"))
