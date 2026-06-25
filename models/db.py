import MySQLdb
import MySQLdb.cursors
from flask import g, current_app


def get_db():

    if 'db' not in g:

        g.db = MySQLdb.connect(

            host=current_app.config['MYSQL_HOST'],

            user=current_app.config['MYSQL_USER'],

            passwd=current_app.config['MYSQL_PASSWORD'],

            db=current_app.config['MYSQL_DB'],

            port=int(
                current_app.config.get('MYSQL_PORT', 3306)
            ),

            cursorclass=MySQLdb.cursors.DictCursor,

            connect_timeout=10,

            ssl_mode='REQUIRED'
        )

    return g.db


def close_db(e=None):

    db = g.pop('db', None)

    if db is not None:

        db.close()


def query(sql, args=(), one=False, commit=False):

    try:

        db = get_db()

        cursor = db.cursor()

        cursor.execute(sql, args)

        if commit:

            db.commit()

            return cursor.rowcount

        rv = cursor.fetchall()

        cursor.close()

        return (rv[0] if rv else None) if one else rv

    except Exception as e:

        print("DATABASE ERROR:", str(e))

        return [] if not one else None