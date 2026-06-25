from flask import Blueprint, request, jsonify, session, current_app
from models.db import query
from groq import Groq
import uuid

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

        user_message = data.get(
            'message',
            ''
        ).strip()

        if not user_message:

            return jsonify({
                'reply': 'Please type something.'
            })

        if 'chat_session_id' not in session:

            session['chat_session_id'] = uuid.uuid4().hex

        session_id = session['chat_session_id']

        # SAVE USER MESSAGE

        try:

            query(
                """
                INSERT INTO chatbot_history
                (
                    session_id,
                    role,
                    message
                )
                VALUES (%s,%s,%s)
                """,
                (
                    session_id,
                    'user',
                    user_message
                ),
                commit=True
            )

        except Exception as db_error:

            print(
                "CHAT SAVE ERROR:",
                str(db_error)
            )

        # GROQ CLIENT

        client = Groq(
            api_key=current_app.config['GROQ_API_KEY']
        )

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

        # SAVE BOT MESSAGE

        try:

            query(
                """
                INSERT INTO chatbot_history
                (
                    session_id,
                    role,
                    message
                )
                VALUES (%s,%s,%s)
                """,
                (
                    session_id,
                    'assistant',
                    reply
                ),
                commit=True
            )

        except Exception as db_error:

            print(
                "BOT SAVE ERROR:",
                str(db_error)
            )

        return jsonify({
            'reply': reply
        })

    except Exception as e:

        print(
            "CHATBOT ERROR:",
            str(e)
        )

        return jsonify({
            'reply': 'Sorry, chatbot is temporarily unavailable.'
        })