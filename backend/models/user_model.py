import sqlite3
from database import get_connection

def add_new_user(username, password):
   
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        connection.commit()

    finally:
        if connection:    
            connection.close()


def get_user_by_id(user_id):
    connection = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        
        user = cursor.fetchone()
        return user

    finally:
        if connection:
            connection.close()

def get_user_by_username(username):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()
        return user
    
    finally:
        if connection:
            connection.close()

