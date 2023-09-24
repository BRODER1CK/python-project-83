import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_db():
    return psycopg2.connect(DATABASE_URL)


def get_urls_with_checks():
    with get_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('SELECT DISTINCT ON (urls.id)\
                        urls.id AS id,\
                        urls.name AS name,\
                        url_checks.created_at AS last_check,\
                        url_checks.status_code AS status_code\
                    FROM urls\
                    LEFT JOIN url_checks ON urls.id = url_checks.url_id\
                    AND url_checks.id = (SELECT MAX(id)\
                                        FROM url_checks\
                                        WHERE url_id = urls.id)\
                    ORDER BY urls.id DESC;')
            urls = curs.fetchall()
    return urls


def get_url_by_id(id):
    with get_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('SELECT * FROM urls WHERE id = %s;', (id,))
            url = curs.fetchone()
    return url


def get_url_by_name(name):
    with get_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('SELECT * FROM urls WHERE name = %s;', (name,))
            url = curs.fetchone()
    return url


def add_url(url):
    with get_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                'INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;',
                (url, datetime.now())
            )
            id = curs.fetchone().id
            conn.commit()
    return id


def get_checks_for_url(id):
    with get_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('SELECT * FROM url_checks WHERE url_id = %s', (id, ))
            checks = curs.fetchall()
    return checks


def add_check(data):
    with get_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                'INSERT INTO url_checks\
                (url_id, status_code, h1, title, description, created_at)\
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;',
                (
                    data['url_id'],
                    data['status_code'],
                    data['h1'], data['title'],
                    data['description'],
                    datetime.now()
                )
            )
            id = curs.fetchone().id
            conn.commit()
    return id
