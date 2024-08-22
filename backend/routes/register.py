# routes/register.py
from flask import Blueprint, request, jsonify, abort
from models.dbConfig import db
from models.user import User
from models.doctor import Doctor
from werkzeug.security import generate_password_hash, check_password_hash
# from bcrypt import generate_password_hash
import sqlalchemy.exc

register_bp = Blueprint("register", __name__)  # A blueprint for the register route

@register_bp.route("/register/doctor", methods=["POST"])
def register_user():
    try:
        name = request.json.get("name")
        email = request.json.get("email")
        password = request.json.get("password")
        role = request.json.get("role")

        if not name or not email or not password or not role:
            return jsonify({"error": "All fields (name, email, password, role) are required"}), 400

        doctor_exists = Doctor.query.filter_by(email=email).first() is not None
        if doctor_exists:
            return jsonify({"error": "Doctor already exists"}), 409

        hashed_password = generate_password_hash(password)
        new_doctor = Doctor(name=name, email=email, password=hashed_password)
        new_user = User(id=new_doctor.id, password=hashed_password, role=role)
        db.session.add(new_doctor)
        db.session.add(new_user)
        db.session.commit()

        # return jsonify({"message":"Doctor registered"})
        return jsonify({"id":new_doctor.id,"name":new_doctor.name,"email":new_doctor.email,"password":new_doctor.password,"role":new_user.role }), 201

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
