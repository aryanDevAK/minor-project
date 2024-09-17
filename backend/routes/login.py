from flask import Blueprint, request, jsonify
from models.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login_user():
    user_id = request.json.get("id")
    password = request.json.get("password")
    
    if not user_id or not password:
        return jsonify({"message": "Missing required fields"}), 401

    user = User.query.filter_by(user_id=user_id).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid ID or password"}), 401

    access_token = create_access_token(identity={"id": user.user_id, "role": user.role})
    refresh_token = create_refresh_token(identity={"id": user.user_id, "role":user.role})

    role_message = {
        "doctor": "Welcome, Doctor",
        "nurse": "Welcome, Nurse",
        "staff": "Welcome, Staff Member",
        "admin": "Welcome, Admin",
        "receptionist": "Welcome, Receptionist",
        "lab": "Welcome, Lab Technician"
    }

    if user.role in role_message:
        return jsonify({
            "message": role_message[user.role],
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    else:
        return jsonify({"message": "User role not recognized"}), 403
