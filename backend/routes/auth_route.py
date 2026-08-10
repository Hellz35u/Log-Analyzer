from flask import Blueprint, request, jsonify
from werkzeug.datastructures import Authorization
from controllers.auth_controller import register, login, logout

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register_route():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "success": False,
            "message": "Request body must contain JSON"
        }), 400
    
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "username and password are required"
        }), 400
    
    result = register(username, password)

    status_code = result["status_code"]

    return jsonify({
        "success": result["success"],
        "message": result["message"]
    }), status_code

@auth_bp.post("/login")
def login_route():
    data = request.get_json(silent = True)

    if data is None:
        return jsonify({
            "success": False,
            "message": "Request body must contain JSON",
        }), 400
    
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "username and password are required"
        }), 400
    
    result = login(username, password)
    status_code = result["status_code"]

    response = {
        "success": result["success"],
        "message": result["message"]
    }

    if "token" in result:
        response["token"] = result["token"]
    
    return jsonify(response), status_code

@auth_bp("/logout")
def logout_route():
    authorization = request.headers.get("Authorization")

    if not authorization:
        return jsonify({
            "success": False,
            "message": "Authorization header is required"
        }), 401

    parts = authorization.split(" ")

    if len(parts) != 2 or parts[0] != "Bearer":
        return jsonify({
            "success": False,
            "message": "Invalid authorization format"
        }), 401

    token = parts[1]

    result = logout(token)
    status_code = result["status_code"]

    return jsonify({
        "success": result["success"],
        "message": result["message"]
    }), status_code