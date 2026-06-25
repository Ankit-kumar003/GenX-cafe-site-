from flask import Blueprint, request, jsonify, session, current_app
from models.db import query
from groq import Groq
import uuid
import traceback
import os # SYSTEM FIX: Imported os to read direct Render environment variables

chatbot = Blueprint('chatbot', __name__)

SYSTEM_PROMPT = """
You are Barista Bot for Gen X Cafe.

You help users with:
- Coffee recommendations
- Food suggestions
- Reservation help
- Cafe timings
- Menu guidance

Keep replies short, friendly and helpful.
"""

@chatbot.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({
                'reply': 'Please type something.'
            })

        # CREATE SESSION
        if 'chat_session_id' not in session:
            session['chat_session_id'] = uuid.uuid4().hex

        session_id = session['chat_session_id']

        # SAVE USER MESSAGE (Wrapped inside a safe try-except block so DB sleep doesn't crash the bot)
        try:
            query(
                """
                INSERT INTO chatbot_history
                (session_id, role, message)
                VALUES (%s,%s,%s)
                """,
                (session_id, 'user', user_message),
                commit=True
            )
        except Exception as db_err:
            print("Chatbot DB Log Error (User):", str(db_err))

        # CREATE GROQ CLIENT
        # SYSTEM FIX: Fallback applied to read directly from OS Environment if Flask Config feels empty on Render
        api_key = os.environ.get('GROQ_API_KEY') or current_app.config.get('GROQ_API_KEY', '')

        if not api_key:
            return jsonify({
                'reply': "Sorry, my API Key is missing on Render configuration! ☕"
            })

        client = Groq(api_key=api_key)

        # AI RESPONSE
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7,
            max_tokens=200
        )

        reply = response.choices[0].message.content

        # SAVE BOT RESPONSE
        try:
            query(
                """
                INSERT INTO chatbot_history
                (session_id, role, message)
                VALUES (%s,%s,%s)
                """,
                (session_id, 'assistant', reply),
                commit=True
            )
        except Exception as db_err:
            print("Chatbot DB Log Error (Bot):", str(db_err))

        return jsonify({
            'reply': reply
        })

    except Exception as e:
        traceback.print_exc()
        print("CHATBOT ERROR:", str(e))
        return jsonify({
            'reply': f"Sorry, I'm having a moment! ☕ (Error: {str(e)})"
        })