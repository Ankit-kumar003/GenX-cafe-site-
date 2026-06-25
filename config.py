import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'genxcafe-secret-key')
    
    # 1. Database Configuration (Render environment variables se read karega with safe .strip())
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'mysql-98e4b7a-jangirrahul0026-386c.i.aivencloud.com').strip()
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 24240))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'avnadmin').strip()
    MYSQL_DB = os.environ.get('MYSQL_DB', 'genxcafe').strip()
    
    # SYSTEM CORRECTED: Render dashboard wale password ko bina space ke fetch karega
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '').strip()
    
    # 2. Chatbot & Extra Configurations
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '').strip()
    GROQ_MODEL = 'llama3-70b-8192'
    
    # 3. File Uploads Config (SYSTEM FIXED: Path matched with static/uploads structure)
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    WTF_CSRF_ENABLED = True
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    print("MYSQL PASSWORD:", os.environ.get("MYSQL_PASSWORD"))