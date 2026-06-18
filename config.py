import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'genxcafe-secret-key')
    
    # 1. Database Configuration (Render environment variables se read karega)
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'mysql-98e4b7a-jangirrahul0026-386c.i.aivencloud.com')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 24240))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'avnadmin')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'genxcafe')
    
    # SYSTEM CORRECTED: Yeh line ab Render dashboard wale password ko fetch karegi
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    
    # 2. Chatbot & Extra Configurations
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    GROQ_MODEL = 'llama3-70b-8192'
    
    # 3. File Uploads Config
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    WTF_CSRF_ENABLED = True
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}