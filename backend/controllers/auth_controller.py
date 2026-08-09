from sqlite3 import DatabaseError
import sqlite3
from models.user_model import add_new_user, get_user_by_username, get_user_by_id
from models.database import get_connection
from services.validators import validate_password, validate_username
import bcrypt

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
    