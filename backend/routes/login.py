from flask import Blueprint, request, jsonify
from models.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

login_bp = Blueprint("login", __name__)
@login_bp.route("/login", methods=["POST"])
def login_user():
    try:
        user_id = request.json.get("id")
        password = request.json.get("password")

        if not user_id or not password:
            return jsonify({"message": "Missing required fields"}), 400

        user = User.query.filter_by(user_id=user_id).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"message": "Invalid ID or password"}), 401

        access_token = create_access_token(identity={"id": user.user_id, "role": user.role})
        refresh_token = create_refresh_token(identity={"id": user.user_id, "role": user.role})

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
                "role" : user.role,
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        else:
            return jsonify({"message": "Not recognized"}), 400  

    except Exception as e:
        return jsonify({"message": "An Unexpected error occurred during login", "error": str(e)}), 500

@login_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    try:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        return jsonify({"message": "Error refreshing token", "error": str(e)}), 500
