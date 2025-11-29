# ChatBot
Flask + OpenAI powered chat app with a WhatsApp-style interface, in-browser chat widget, and simple session management.

This project is a simple WhatsApp-style / chat-widget style web app built with **Flask** on the backend and a vanilla HTML/CSS/JS frontend.  
The backend talks to the **OpenAI API** and returns AI responses to user messages.

- Backend: Python + Flask
- Frontend: Static HTML/CSS/JS (served from `/static`)
- AI: OpenAI Chat Completions API

---

## Features

- style / chat-widget UI in the browser
- `/api/chat` endpoint that:
  - Accepts a user message + optional history
  - Sends the conversation to OpenAI
  - Returns the assistant reply as JSON
- Simple in-memory chat session storage
- Clean separation of frontend (static files) and backend (Flask)

---

## Project Structure

```text
.
├── app.py               # Flask backend (API + static file serving)
├── static/
│   └── index.html       # Frontend chat UI (WhatsApp-style / AOC Assistant widget)
├── .env                 # Optional (for non-secret config like model name)
└── README.md
