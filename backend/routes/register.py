# routes/register.py
from flask import Blueprint, request, jsonify, abort
from models.dbConfig import db
from models.user import User
from models.doctor import Doctor
from models.department import Department
from werkzeug.security import generate_password_hash, check_password_hash
# from bcrypt import generate_password_hash
import sqlalchemy.exc

register_doc_bp = Blueprint("register_doctor", __name__)
@register_doc_bp.route("/register/doctor", methods=["POST"])
def register_doctor():
    try:
        name = request.json.get("name")
        age = request.json.get("age")
        speciality = request.json.get("speciality")
        email = request.json.get("email")
        password = request.json.get("password")
        role = request.json.get("role")

        if not name or not email or not password or not role or not age or not speciality:
            return jsonify({"error": "All fields (name, email, password, role) are required"}), 400

        user_exists = User.query.filter_by(email=email).first() is not None
        if user_exists:
            return jsonify({"error": "Doctor already exists"}), 409

        hashed_password = generate_password_hash(password)
        new_doctor = Doctor(name=name, age=age, speciality=speciality)
        new_user = User(user_id=new_doctor.id, email=email, password=hashed_password, role=role)
        db.session.add(new_doctor)
        db.session.add(new_user)
        db.session.commit()

        # return jsonify({"message":"Doctor registered"})
        return jsonify({"id":new_doctor.id,"name":new_doctor.name,"age":new_doctor.age,"speciality":new_doctor.speciality, "email":new_user.email,"password":new_user.password,"role":new_user.role }), 201

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

register_dept_bp = Blueprint("register_department",__name__)
@register_dept_bp.route("/register/department", methods=["POST"])
def register_department():
    try:
        dept_name = request.json.get("name")

        if not dept_name:
            return jsonify({"error": "Department Name required"}), 400

        department_exists = Department.query.filter_by(name=dept_name).first() is not None
        if department_exists:
            return jsonify({"error": "Department already exists"}), 409

        new_department = Department(name=dept_name)
        db.session.add(new_department)
        db.session.commit()

        return jsonify({
            "id": new_department.id,
            "name": new_department.name,
        }), 201
        # return jsonify({"message":"Department created Successfully"}), 201

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500