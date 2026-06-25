from flask import Blueprint, request, jsonify, session, current_app
from models.db import query
from groq import Groq
import uuid
import traceback

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

        # SAVE USER MESSAGE

        query(
            """
            INSERT INTO chatbot_history
            (session_id, role, message)
            VALUES (%s,%s,%s)
            """,
            (session_id, 'user', user_message),
            commit=True
        )

        # CREATE GROQ CLIENT

        client = Groq(
            api_key=current_app.config['GROQ_API_KEY']
        )

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

        query(
            """
            INSERT INTO chatbot_history
            (session_id, role, message)
            VALUES (%s,%s,%s)
            """,
            (session_id, 'assistant', reply),
            commit=True
        )

        return jsonify({
            'reply': reply
        })

    except Exception as e:

        traceback.print_exc()

        print("CHATBOT ERROR:", str(e))

        return jsonify({
            'reply': f'Error: {str(e)}'
        })