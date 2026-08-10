from flask import Blueprint, request, jsonify
from controllers.auth_controller import register

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
    