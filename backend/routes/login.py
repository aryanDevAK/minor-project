# routes/login.py
from flask import Blueprint, request, jsonify, abort
from models.user import User
from werkzeug.security import check_password_hash
# from flask_jwt_extended import create_access_token

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login_user():
    id = request.json.get("id")
    password = request.json.get("password")
    
    user = User.query.filter_by(user_id=id).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid ID or password"}), 401

    # access_token = create_access_token(identity=user.id)
    
    if user.role == "doctor":
        return jsonify({"message": "Login successful"}), 200
    elif user.role == "patient":
        return jsonify({"message": "Login successful"}), 200
    elif user.role == "nurse":
        return jsonify({"message": "Login successful"}), 200
    elif user.role == "staff":
        return jsonify({"message": "Login successful"}), 200
    elif user.role == "admin":
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "User role not recognized"}), 403