from flask import Flask, send_from_directory
from config import Config
from models.db import close_db

from routes.public import public
from routes.auth import auth
from routes.admin import admin_bp
from routes.chatbot import chatbot

import os

app = Flask(__name__)

app.config.from_object(Config)

# REGISTER BLUEPRINTS

app.register_blueprint(public)

app.register_blueprint(auth)

app.register_blueprint(
    admin_bp,
    name='admin'
)

app.register_blueprint(chatbot)

# CLOSE DATABASE

app.teardown_appcontext(close_db)

# UPLOAD ROUTE

@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename
    )

# GLOBAL ERROR HANDLER

@app.errorhandler(Exception)
def handle_error(e):

    print("GLOBAL ERROR:", str(e))

    return f"""
    <h1>Server Error</h1>
    <pre>{str(e)}</pre>
    """, 500


# RUN APP

if __name__ == '__main__':

    os.makedirs(
        app.config['UPLOAD_FOLDER'],
        exist_ok=True
    )

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )