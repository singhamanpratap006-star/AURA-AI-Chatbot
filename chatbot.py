import ollama
import json
import os

FILE_NAME = "chat_sessions.json"

# Maximum conversation history sent to AI
MAX_HISTORY = 10

# Custom personality
system_prompt = """
Your name is AURA.
You are a friendly and intelligent AI assistant.
Use simple English.
Give clear and helpful answers.
Keep responses reasonably short.
"""

# Load saved chat sessions
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as file:
        sessions = json.load(file)
else:
    sessions = {}

# Create first chat
if not sessions:
    sessions["Chat 1"] = []

current_chat = list(sessions.keys())[0]


# Save function
def save_sessions():
    with open(FILE_NAME, "w") as file:
        json.dump(sessions, file, indent=4)


print("==============================")
print("          AURA AI")
print("==============================")

print("Commands:")
print("new    - Create new chat")
print("list   - Show all chats")
print("switch - Switch chat")
print("clear  - Clear current chat")
print("exit   - Exit chatbot")

print("\nCurrent chat:", current_chat)


while True:

    user_input = input("\nYou: ").strip()

    # Exit
    if user_input.lower() == "exit":
        print("AURA: Goodbye!")
        break

    # Create new chat
    elif user_input.lower() == "new":

        number = 1

        while f"Chat {number}" in sessions:
            number += 1

        new_chat = f"Chat {number}"

        sessions[new_chat] = []

        current_chat = new_chat

        save_sessions()

        print("AURA: New chat created:", current_chat)

    # List chats
    elif user_input.lower() == "list":

        print("\nSaved conversations:")

        for chat in sessions:
            print("-", chat)

    # Switch chat
    elif user_input.lower() == "switch":

        chat_name = input("Enter chat name: ").strip()

        if chat_name in sessions:
            current_chat = chat_name
            print("AURA: Switched to", current_chat)

        else:
            print("AURA: Chat not found.")

    # Clear current chat
    elif user_input.lower() == "clear":

        sessions[current_chat] = []

        save_sessions()

        print("AURA: Chat history cleared!")

    # Normal conversation
    else:

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # Load only the latest 10 messages
        messages.extend(
            sessions[current_chat][-MAX_HISTORY:]
        )

        # Add new user message
        messages.append({
            "role": "user",
            "content": user_input
        })

        # Generate response
        response = ollama.chat(
            model="smollm2:360m",
            messages=messages
        )

        bot_reply = response["message"]["content"]

        print("AURA:", bot_reply)

        # Save complete conversation
        sessions[current_chat].append({
            "role": "user",
            "content": user_input
        })

        sessions[current_chat].append({
            "role": "assistant",
            "content": bot_reply
        })

        save_sessions()