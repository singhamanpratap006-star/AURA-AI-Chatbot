AURA AI – Personal AI Chatbot

AURA AI is a simple personal AI chatbot built using Python, Flask, Ollama and the SmolLM2 language model.

It provides a local chat interface where users can communicate with an AI assistant, create multiple conversations and revisit previous chats.

Features

- AI-powered conversations
- Multiple chat sessions
- Previous conversation history
- Automatic chat titles
- Delete conversations
- Custom AI personality
- Responsive interface for desktop and mobile
- Local AI model through Ollama

Technologies Used

- Python
- Flask
- Ollama
- SmolLM2 (360M)
- HTML
- CSS
- JavaScript
- JSON

Project Structure

AURA-AI-Chatbot/
│
├── app.py
├── chatbot.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js

Requirements

- Python 3
- Ollama
- SmolLM2 model

Installation

1. Clone the repository

git clone https://github.com/singhamanpratap006-star/AURA-AI-Chatbot.git

2. Open the project folder

cd AURA-AI-Chatbot

3. Install Python dependencies

pip install -r requirements.txt

4. Download the AI model

ollama pull smollm2:360m

5. Run AURA AI

python app.py

6. Open in your browser

http://127.0.0.1:5000

Important Note

AURA AI runs locally using Ollama. The laptop must remain on while using the chatbot.

This project is currently a learning project and is under development.

Developer

Created as a personal learning project to explore Python, AI integration and web development.
