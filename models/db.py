import os
import pymysql
import pymysql.cursors
from flask import g, current_app

pymysql.install_as_MySQLdb()


def get_db():
    if 'db' not in g:
        # SYSTEM FIX: Dynamic keys mapped directly with fallbacks for Render environment variables
        host = os.environ.get('MYSQL_HOST') or current_app.config.get('MYSQL_HOST', 'mysql-98e4b7a-jangirrahul0026-386c.i.aivencloud.com')
        user = os.environ.get('MYSQL_USER') or current_app.config.get('MYSQL_USER', 'avnadmin')
        password = os.environ.get('MYSQL_PASSWORD') or current_app.config.get('MYSQL_PASSWORD', '')
        database_name = os.environ.get('MYSQL_DB') or current_app.config.get('MYSQL_DB', 'genxcafe')
        
        try:
            port_val = int(os.environ.get('MYSQL_PORT') or current_app.config.get('MYSQL_PORT', 24240))
        except (ValueError, TypeError):
            port_val = 24240

        # String stripping to avoid hidden white space issues on Render
        host = host.strip() if host else host
        user = user.strip() if user else user
        password = password.strip() if password else password
        database_name = database_name.strip() if database_name else database_name

        g.db = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database_name, # Mapped correctly
            port=port_val,
            connect_timeout=60,
            cursorclass=pymysql.cursors.DictCursor,
            ssl={"ssl": {}} # Enforces SSL encryption for Aiven
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def query(sql, args=(), one=False, commit=False):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(sql, args)
        if commit:
            db.commit()
            row_count = cursor.rowcount
            cursor.close()
            return row_count
            
        rv = cursor.fetchall()
        cursor.close()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        if commit:
            db.rollback()
        cursor.close()
        raise e