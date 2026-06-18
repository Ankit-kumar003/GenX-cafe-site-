from flask import Blueprint, request, jsonify, session
from models.db import query
from groq import Groq
from flask import current_app
import uuid

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
        client = Groq(api_key=current_app.config['GROQ_API_KEY'])
        response = client.chat.completions.create(
            model=current_app.config['GROQ_MODEL'],
            messages=[{'role': 'system', 'content': SYSTEM_PROMPT}] + messages,
            max_tokens=200,
            temperature=0.7
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "Sorry, I'm having a moment! ☕ Please try again or contact us directly."

    # Store bot reply
    query("INSERT INTO chatbot_history (session_id, role, message) VALUES (%s,%s,%s)",
          (session_id, 'assistant', reply), commit=True)

    return jsonify({'reply': reply})
