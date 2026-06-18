import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'genxcafe-secret-key')
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    
    # Cloud Aiven Database ke credentials yahan daalein
    MYSQL_HOST = 'mysql-98e4b7a-jangirrahul0026-386c.i.aivencloud.com'
    MYSQL_PORT = 24240
    MYSQL_USER = 'avnadmin'
    MYSQL_DB = 'genxcafe'
    # 'Click to reveal password' wale text par click karke jo password mila wo yahan copy karein
    MYSQL_PASSWORD = ''
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    GROQ_MODEL = 'llama3-70b-8192'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    WTF_CSRF_ENABLED = True
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
