# routes/register.py
from flask import Blueprint, request, jsonify, abort
from models.dbConfig import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
# from bcrypt import generate_password_hash
import sqlalchemy.exc

register_bp = Blueprint("register", __name__)  # Create a blueprint for the register route

@register_bp.route("/register", methods=["POST"])
def register_user():
    try:
        email = request.json.get("email")
        password = request.json.get("password")
        role = request.json.get("role")

        if not email or not password or not role:
            return jsonify({"error": "All fields (email, password, role) are required"}), 400

        user_exists = User.query.filter_by(email=email).first() is not None
        if user_exists:
            return jsonify({"error": "User already exists"}), 409

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
