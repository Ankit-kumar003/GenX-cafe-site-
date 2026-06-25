import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.environ.get(
        'SECRET_KEY',
        'genxcafe-secret-key'
    )

    MYSQL_HOST = os.environ.get(
        'MYSQL_HOST',
        ''
    ).strip()

    MYSQL_PORT = int(
        os.environ.get('MYSQL_PORT', 3306)
    )

    MYSQL_USER = os.environ.get(
        'MYSQL_USER',
        ''
    ).strip()

    MYSQL_PASSWORD = os.environ.get(
        'MYSQL_PASSWORD',
        ''
    ).strip()

    MYSQL_DB = os.environ.get(
        'MYSQL_DB',
        ''
    ).strip()

    GROQ_API_KEY = os.environ.get(
        'GROQ_API_KEY',
        ''
    ).strip()

    GROQ_MODEL = "llama-3.3-70b-versatile"

    UPLOAD_FOLDER = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'static/uploads'
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    WTF_CSRF_ENABLED = True

    ALLOWED_EXTENSIONS = {
        'png',
        'jpg',
        'jpeg',
        'gif',
        'webp'
    }