import pymysql
import pymysql.cursors
from flask import g, current_app

pymysql.install_as_MySQLdb()


def get_db():

    if 'db' not in g:

        g.db = pymysql.connect(

            host=current_app.config['MYSQL_HOST'],

            user=current_app.config['MYSQL_USER'],

            password=current_app.config['MYSQL_PASSWORD'],

            database=current_app.config['MYSQL_DB'],

            port=int(
                current_app.config.get('MYSQL_PORT', 3306)
            ),

            connect_timeout=60,

            cursorclass=pymysql.cursors.DictCursor,

            ssl={
                "ssl": {}
            }

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

            return cursor.rowcount

        rv = cursor.fetchall()

        cursor.close()

        return (rv[0] if rv else None) if one else rv

    except Exception as e:

        if commit:

            db.rollback()

        cursor.close()

        raise e