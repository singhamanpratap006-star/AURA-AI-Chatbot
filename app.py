from flask import Flask, render_template, request, jsonify
import ollama
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Configuration
FILE_NAME = "chat_sessions.json"
MODEL_NAME = "smollm2:360m"
MAX_HISTORY = 10

# AURA personality
SYSTEM_PROMPT = """
Your name is AURA.

You are a friendly and helpful AI assistant.

IMPORTANT LANGUAGE RULES:
1. Always use correct English spelling.
2. Use proper grammar and punctuation.
3. Write clear and understandable sentences.
4. Check your spelling before giving an answer.
5. Avoid unnecessary complicated vocabulary.
6. If you are unsure about something, say so.
7. Never intentionally misspell words.

Keep your answers clear, natural and reasonably short.
"""


# Get current date and time
def current_time():
    return datetime.now().isoformat()


# Load previous conversations
def load_sessions():

    if os.path.exists(FILE_NAME):

        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data

        except (json.JSONDecodeError, OSError):
            print("Unable to read chat history.")

    return {}


# Save conversations
def save_sessions():

    with open(FILE_NAME, "w") as file:
        json.dump(sessions, file, indent=4)


# Create a new chat
def create_chat():

    chat_id = str(uuid.uuid4())

    sessions[chat_id] = {
        "title": "New Chat",
        "messages": [],
        "created_at": current_time(),
        "updated_at": current_time()
    }

    save_sessions()

    return chat_id


# Load saved chats
sessions = load_sessions()

if not sessions:
    create_chat()


# Home page
@app.route("/")
def home():

    return render_template("index.html")


# Get all conversations
@app.route("/api/chats", methods=["GET"])
def get_chats():

    chat_list = []

    for chat_id, chat in sessions.items():

        chat_list.append({
            "id": chat_id,
            "title": chat["title"],
            "updated_at": chat["updated_at"]
        })

    chat_list.sort(
        key=lambda chat: chat["updated_at"],
        reverse=True
    )

    return jsonify({"chats": chat_list})


# Create a new conversation
@app.route("/api/chats", methods=["POST"])
def new_chat():

    chat_id = create_chat()

    return jsonify({
        "id": chat_id,
        "title": sessions[chat_id]["title"]
    })


# Open previous conversation
@app.route("/api/chats/<chat_id>", methods=["GET"])
def get_chat(chat_id):

    if chat_id not in sessions:

        return jsonify({
            "error": "Chat not found."
        }), 404

    return jsonify({
        "id": chat_id,
        "title": sessions[chat_id]["title"],
        "messages": sessions[chat_id]["messages"]
    })


# Delete a conversation
@app.route("/api/chats/<chat_id>", methods=["DELETE"])
def delete_chat(chat_id):

    if chat_id not in sessions:

        return jsonify({
            "error": "Chat not found."
        }), 404

    del sessions[chat_id]

    if not sessions:
        create_chat()
    else:
        save_sessions()

    return jsonify({"success": True})


# Send message to AURA
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json() or {}

    user_message = data.get("message", "").strip()
    chat_id = data.get("chat_id", "")

    if not user_message:

        return jsonify({
            "error": "Please enter a message."
        }), 400

    if chat_id not in sessions:

        return jsonify({
            "error": "Chat not found."
        }), 404

    selected_chat = sessions[chat_id]

    history = selected_chat["messages"]

    # Prepare conversation history
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history[-MAX_HISTORY:])

    messages.append({
        "role": "user",
        "content": user_message
    })

    try:

        # Generate AI response using Ollama
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages
        )

        bot_reply = response["message"]["content"]

        # Save conversation
        history.append({
            "role": "user",
            "content": user_message
        })

        history.append({
            "role": "assistant",
            "content": bot_reply
        })

        # Automatically create chat title
        if selected_chat["title"] == "New Chat":

            selected_chat["title"] = user_message[:35]

        selected_chat["updated_at"] = current_time()

        save_sessions()

        return jsonify({
            "reply": bot_reply,
            "title": selected_chat["title"]
        })

    except Exception as error:

        print("Ollama error:", error)

        return jsonify({
            "error": "Unable to generate a response. Check whether Ollama is running and the model is available."
        }), 500


# Run Flask server
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )