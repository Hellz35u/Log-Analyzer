import hashlib
from datetime import datetime, timedelta
from sqlite3 import DatabaseError
import sqlite3
from models.session_model import delete_session, get_session_by_token_hash
from models.user_model import add_new_user, get_user_by_username, get_user_by_id
from models.database import get_connection
from services.validators import validate_password, validate_username
from models.session_model import create_session
import bcrypt
import secrets


def register(username, password):
    password_bytes = password.encode()
    salt = bcrypt.gensalt()
    password_hashed = bcrypt.hashpw(password_bytes, salt)

    try:
        if not validate_username(username):
            return{
                "success": False,
                "message": "Invalid username",
                "status_code": 400
            }
        
        if not validate_password(password):
            return{
                "success": False,
                "message": "Invalid password",
                "status_code": 400
            }
        
        user = get_user_by_username(username)

        if user is not None:
            return{
                "success": False,
                "message": "Username already exists",
                "status_code": 400
            }
        
        password_bytes = password.encode()
        salt = bcrypt.gensalt()
        password_hashed = bcrypt.hashpw(password_bytes, salt)

        add_new_user(username, password_hashed)
        return {
            "success": True,
            "message": "User registered successfully",
            "status_code": 200
        }
    
    except sqlite3.DatabaseError as e:
        return{
            "success": False,
            "message": "Database Error",
            "status_code": 500
        }

def login(username, password):
    try:
        user = get_user_by_username(username)

        if user is None:
            return{
                "success": False,
                "message": "Invalid username or password",
                "status_code": 401
            }

        password_bytes = password.encode()

        if not bcrypt.checkpw(password_bytes, user["password"]):
            return{
                "success": False,
                "message": "Invalid username or password",
                "status_code": 401
            }
        
        token = secrets.token_urlsafe(32)

        token_hash = hashlib.sha256(token.encode()).hexdigest()

        expires_at = datetime.now() + timedelta(hours=24)

        create_session(user["id"], token_hash, expires_at)

        return {
            "success": True,
            "message": "Login successfully",
            "status_code": 200,
            "token": token
        }

    except DatabaseError:
        return{
            "success": False,
            "message": "Database error",
            "status_code": 500
        }

def logout(token):
    try:
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        session = get_session_by_token_hash(token_hash)

        if session is None:
            return {
                "success": False,
                "message": "Invalid session",
                "status_code": 401
            }

        delete_session(token_hash)

        return {
            "success": True,
            "message": "Logout successfully",
            "status_code": 200
        }

    except DatabaseError:
        return {
            "success": False,
            "message": "Database error",
            "status_code": 500
        }