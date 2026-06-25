<<<<<<< HEAD
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
=======
from flask import Blueprint, request, jsonify, session
from models.db import query
from groq import Groq
from flask import current_app
import uuid
import os # SYSTEM FIX: Imported os to read render environment variables directly

chatbot = Blueprint('chatbot', __name__)

SYSTEM_PROMPT = """You are Barista Bot, the friendly AI assistant for Gen X Cafe.
You help customers with:
- Menu recommendations (Coffee, Tea, Cold Beverages, Pizza, Burgers, Sandwiches, Desserts)
- Cafe information: Open 7AM-11PM daily, located at MG Road, Jaipur
- Reservation assistance
- Special offers and featured items
- General cafe FAQs

Be warm, concise, and helpful. Use emojis sparingly. Keep responses under 100 words.
If asked about prices, mention our menu page. Always end with a helpful suggestion."""

@chatbot.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    if 'chat_session_id' not in session:
        session['chat_session_id'] = uuid.uuid4().hex

    session_id = session['chat_session_id']

    # Store user message
    query("INSERT INTO chatbot_history (session_id, role, message) VALUES (%s,%s,%s)",
          (session_id, 'user', user_message), commit=True)

    # Get recent history
    history = query(
        "SELECT role, message FROM chatbot_history WHERE session_id=%s ORDER BY created_at DESC LIMIT 10",
        (session_id,)
    )
    history = list(reversed(history)) if history else []

    messages = [{'role': h['role'], 'content': h['message']} for h in history]

    try:
        # SYSTEM FIX: Directly checking os.environ so Render keys are read instantly
        # Also added a solid model fallback 'llama3-8b-8192' if config model is missing
        api_key = os.environ.get('GROQ_API_KEY') or current_app.config.get('GROQ_API_KEY')
        model_name = os.environ.get('GROQ_MODEL') or current_app.config.get('GROQ_MODEL') or 'llama3-8b-8192'
        
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[{'role': 'system', 'content': SYSTEM_PROMPT}] + messages,
            max_tokens=200,
            temperature=0.7
        )
        reply = response.choices[0].message.content
    except Exception as e:
        # Debugging ke liye aap local/render logs me error dekh sakein
        print("Chatbot Error:", str(e))
        reply = "Sorry, I'm having a moment! ☕ Please try again or contact us directly."

    # Store bot reply
    query("INSERT INTO chatbot_history (session_id, role, message) VALUES (%s,%s,%s)",
          (session_id, 'assistant', reply), commit=True)

    return jsonify({'reply': reply})
>>>>>>> ee502b266f23d8c41c8780c8fc03b1f415f79d0f
