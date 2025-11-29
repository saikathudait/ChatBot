import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

app = Flask(__name__, static_folder="static", static_url_path="/static")

# Init OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

# In-memory storage for chat sessions (use database in production)
chat_sessions = {}

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    history = data.get("history", [])
    session_id = data.get("session_id", "default")
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    # Build messages list for the model
    messages = [
        {
            "role": "system",
            "content": (
                "You are a highly intelligent and professional AI assistant created by AOC. "
                "You provide clear, accurate, and helpful responses. You can assist with "
                "coding, writing, analysis, and general questions. Be concise yet thorough."
            ),
        }
    ]
    
    # Add previous history
    for msg in history:
        role = msg.get("role")
        content = msg.get("content")
        if role in ["user", "assistant"] and isinstance(content, str):
            messages.append({"role": role, "content": content})
    
    # Add the new user message
    messages.append({"role": "user", "content": user_message})
    
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
        )
        reply = completion.choices[0].message.content
        
        # Store session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = {
                "id": session_id,
                "title": user_message[:50],
                "created": datetime.now().isoformat(),
                "messages": []
            }
        
        chat_sessions[session_id]["messages"].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        chat_sessions[session_id]["messages"].append({
            "role": "assistant",
            "content": reply,
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({"reply": reply})
    
    except Exception as e:
        print("OpenAI API error:", e)
        return jsonify({"error": "Something went wrong with the AI request."}), 500

@app.route("/api/sessions", methods=["GET"])
def get_sessions():
    sessions_list = [
        {
            "id": sid,
            "title": session["title"],
            "created": session["created"],
            "message_count": len(session["messages"])
        }
        for sid, session in chat_sessions.items()
    ]
    return jsonify({"sessions": sorted(sessions_list, key=lambda x: x["created"], reverse=True)})

@app.route("/api/sessions/<session_id>", methods=["GET"])
def get_session(session_id):
    if session_id in chat_sessions:
        return jsonify(chat_sessions[session_id])
    return jsonify({"error": "Session not found"}), 404

@app.route("/api/sessions/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return jsonify({"success": True})
    return jsonify({"error": "Session not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)