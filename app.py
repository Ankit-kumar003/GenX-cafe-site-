from flask import Flask, send_from_directory
from config import Config
from models.db import close_db

from routes.public import public
from routes.auth import auth
# 1. Yahan admin ko admin_bp se badlein
from routes.admin import admin_bp 
from routes.chatbot import chatbot

import os

app = Flask(__name__)
app.config.from_object(Config)

# BLUEPRINTS REGISTER
app.register_blueprint(public)
app.register_blueprint(auth)
# 2. Yahan bhi admin_bp register karein, lekin url_for('admin.dashboard') ko chalane ke liye name='admin' specify karein
app.register_blueprint(admin_bp, name='admin') 
app.register_blueprint(chatbot)

# CLOSE DB
app.teardown_appcontext(close_db)

# UPLOADS ROUTE
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename
    )

# RUN
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)