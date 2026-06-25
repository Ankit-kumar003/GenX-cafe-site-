import MySQLdb
<<<<<<< HEAD
import MySQLdb.cursors
=======
# Explicitly cursors ko import kar rahe hain taaki AttributeError na aaye
import MySQLdb.cursors 
>>>>>>> ee502b266f23d8c41c8780c8fc03b1f415f79d0f
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
<<<<<<< HEAD
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB'],
            port=int(current_app.config.get('MYSQL_PORT', 3306)),
            cursorclass=MySQLdb.cursors.DictCursor
=======
            password=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB'],
            port=int(current_app.config.get('MYSQL_PORT', 3306)),
            cursorclass=MySQLdb.cursors.DictCursor  # Ab yeh error nahi dega
>>>>>>> ee502b266f23d8c41c8780c8fc03b1f415f79d0f
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query(sql, args=(), one=False, commit=False):
    db = get_db()
    cursor = db.cursor()
<<<<<<< HEAD

    try:
        cursor.execute(sql, args)

        if commit:
            db.commit()
            return cursor.rowcount

        rv = cursor.fetchall()
        cursor.close()

        return (rv[0] if rv else None) if one else rv

    except Exception as e:
        if commit:
            db.rollback()

=======
    try:
        cursor.execute(sql, args)
        if commit:
            db.commit()
            return cursor.rowcount
        
        rv = cursor.fetchall()
        cursor.close()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        if commit:
            db.rollback()
>>>>>>> ee502b266f23d8c41c8780c8fc03b1f415f79d0f
        cursor.close()
        raise e