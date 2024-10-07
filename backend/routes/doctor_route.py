from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models.dbConfig import db
from models.doctor import Doctor
from models.docDept import Doc_Dept
from models.user import User
from models.department import Department
from datetime import datetime, date
import sqlalchemy

def str_to_date(birth_date):
    try:
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        return birth_date
    except ValueError:
        return jsonify({"error": "Invalid birth_date format. Use YYYY-MM-DD."}), 400

def has_required_role(required_roles):
    identity = get_jwt_identity()  # Get the identity from the JWT

    # Check if identity is a dictionary and has the expected keys
    if isinstance(identity, dict):
        user_id = identity.get("id")
        user_role = identity.get("role")

        # Validate that user_id and user_role exist
        if user_id is None or user_role is None:
            return False

        # Check if the user's role is in the required roles
        return user_role in required_roles
    
    return False  # Return False if identity is not a dictionary

doctor_routes_bp = Blueprint("doctor_routes", __name__)
@doctor_routes_bp.route("/register/doctor", methods=["POST"])
@jwt_required()
def register_doctor():
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 401

    try:
        name = request.json.get("name")
        birth_date_str = request.json.get("birth-date")
        speciality = request.json.get("speciality")
        email = request.json.get("email")
        password = request.json.get("password")
        department_id = request.json.get("department_id")
        role = "doctor"

        if not all([name, email, password, birth_date_str, speciality, department_id]):
            return jsonify({"message": "All fields are required"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "User email already exists"}), 409

        if not Department.query.filter_by(id=department_id).first():
            return jsonify({"error": "Department not exists"}), 404

        birth_date = str_to_date(birth_date_str)
        hashed_password = generate_password_hash(password)

        new_doctor = Doctor(name=name, birth_date=birth_date, speciality=speciality)
        db.session.add(new_doctor)

        new_user = User(user_id=new_doctor.id, email=email, password=hashed_password, role=role)
        db.session.add(new_user)

        new_assignment = Doc_Dept(doc_id=new_doctor.id, dept_id=department_id)
        db.session.add(new_assignment)

        db.session.commit()

        return jsonify({"message" : "Registered Successfully"})
        # return jsonify({"id": new_doctor.id, "name": new_doctor.name, "speciality": new_doctor.speciality, "email": new_user.email, "role": new_user.role}), 201

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@doctor_routes_bp.route("/get/doctors", methods=["GET"])
@jwt_required()
def get_doctors():
    try:
        doctors = db.session.query(
            Doctor.id,
            Doctor.name,
            Doctor.birth_date,
            Doctor.speciality,
            User.email,
            Department.name.label("department_name")
        ).join(User, Doctor.id == User.user_id) \
         .join(Doc_Dept, Doctor.id == Doc_Dept.doc_id) \
         .join(Department, Doc_Dept.dept_id == Department.id) \
         .all()

        doctor_list = [{
            "id" : doctor.id,
            "name" : doctor.name,
            "birth_date" : doctor.birth_date,
            "speciality" : doctor.speciality,
            "email" : doctor.email,
            "department" : doctor.department_name
        }for doctor in doctors]

        return jsonify(doctor_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@doctor_routes_bp.route("/get/doctor/<string:doctor_id>", methods=["GET"])
@jwt_required()
def get_doctor(doctor_id):
    try:
        doctor = db.session.query(
            Doctor.id,
            Doctor.name,
            Doctor.birth_date,
            Doctor.speciality,
            User.email,
            Department.name.label("department_name")
        ).join(User, Doctor.id == User.user_id) \
         .join(Doc_Dept, Doctor.id == Doc_Dept.doc_id) \
         .join(Department, Doc_Dept.dept_id == Department.id) \
         .filter(Doctor.id == doctor_id) \
         .first()

        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

        doctor_info = {
            "id": doctor.id,
            "name": doctor.name,
            "birth_date": doctor.birth_date,
            "speciality": doctor.speciality,
            "email": doctor.email,
            "department": doctor.department_name
        }

        return jsonify(doctor_info), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update Doctor
@doctor_routes_bp.route("/doctor/<string:doctor_id>", methods=["PUT","PATCH"])
@jwt_required()
def update_doctor(doctor_id):
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 401

    try:
        doctor = Doctor.query.filter_by(id=doctor_id).first()
        if not doctor:
            return jsonify({"error": "User not found"}), 404

        name = request.json.get("name")
        birth_date_str = request.json.get("birth-date")
        speciality = request.json.get("speciality")
        department_id = request.json.get("department_id")
        email = request.json.get("email")

        if name:
            doctor.name = name
        
        if birth_date_str:
            doctor.birth_date = str_to_date(birth_date_str)
        
        if speciality:
            doctor.speciality = speciality

        if department_id:
            assignment = Doc_Dept.query.filter_by(doc_id=doctor.id).first()
            if assignment:
                assignment.dept_id = department_id
            else:
                return jsonify({"error": "Doctor not assigned to any department"}), 404

        if email:
            user = User.query.filter_by(user_id=doctor.id).first()
            if user:
                user.email = email
            else:
                return jsonify({"error": "User not found"}), 404

        db.session.commit()
        return jsonify({"message": "Information updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete Doctor
@doctor_routes_bp.route("/doctor/<string:doctor_id>", methods=["DELETE"])
@jwt_required()
def delete_doctor(doctor_id):
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 401

    try:
        doctor = Doctor.query.filter_by(id=doctor_id).first()
        if not doctor:
            return jsonify({"error": "User not found"}), 404

        User.query.filter_by(user_id=doctor.id).delete()
        Doc_Dept.query.filter_by(doc_id=doctor.id).delete()
        
        db.session.delete(doctor)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
