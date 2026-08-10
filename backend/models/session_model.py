from sqlite3 import connect
from database import get_connection

def create_session(user_id, token_hash, expires_at):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO sessions (user_id, token_hash, expires_at)
            VALUES (?, ?, ?)
            """,
            (user_id, token_hash, expires_at)
        )

        connection.commit()

        return connection.lastrowid
    
    finally:
        if connection:
            connection.close()

def get_session_by_token_hash(token_hash):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM sessions WHERE token_hash = ?
            """,
            (token_hash,)
        )

        return cursor.fetchone()

    finally:
        if connection:
            connection.close()

def delete_session(token_hash):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM sessions WHERE token_hash = ?
            """,
            (token_hash,)
        )
    
        connection.commit()

    finally:
        if connection:
            connection.close()
    
def delete_expired_session():
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM sessions 
            WHERE expires_at <= CURRENT_TIMESTAMP
            """
        )

        connection.commit()

    finally:
        if connection:
            connection.close()