from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.nurse import Nurse
from models.user import User
from models.nurseDept import Nurse_Dept
from models.department import Department
from models.dbConfig import db
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime

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

nurse_routes_bp = Blueprint("register_nurse", __name__)
@nurse_routes_bp.route("/register/nurse", methods=["POST"])
@jwt_required()
def register_nurse():
    if not has_required_role(["admin"]):
        return jsonify({"message" : "You do not have permission to do that"}), 403

    try:
        name = request.json.get("name")
        birth_date_str = request.json.get("birth_date")
        email = request.json.get("email")
        password = request.json.get("password")
        department_id = request.json.get("department_id")
        role = "nurse"

        if not (name and email and password and role and birth_date_str and department_id):
            return jsonify({"error": "All fields are required"}), 400

        if User.query.filter_by(email=email).first() is not None:
            return jsonify({"error": "User email already exists"}), 409

        department = Department.query.filter_by(id=department_id).first()
        if not department:
            return jsonify({"error": "Department not exists"}), 404

        birth_date = str_to_date(birth_date_str)
        hashed_password = generate_password_hash(password)

        new_nurse = Nurse(name=name, birth_date=birth_date)
        db.session.add(new_nurse)

        new_assignment = Nurse_Dept(nurse_id=new_nurse.id, dept_id=department_id)
        db.session.add(new_assignment)

        new_user = User(user_id=new_nurse.id, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        # return jsonify({
        #     "id": new_nurse.id,
        #     "name": new_nurse.name,
        #     "birth_date": new_nurse.birth_date.strftime('%Y-%m-%d'),
        #     "email": new_user.email,
        #     "role": new_user.role
        # }), 201

        return jsonify({"message" : "Registered Successfully"}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@nurse_routes_bp.route("/get/nurses", methods=["GET"])
@jwt_required()
def get_nurses():
    try:
        nurses = db.session.query(
            Nurse.id,
            Nurse.name,
            Nurse.birth_date,
            User.email,
            Department.name.label('department_name')
        ).join(User, Nurse.id == User.user_id) \
         .join(Nurse_Dept, Nurse.id == Nurse_Dept.nurse_id) \
         .join(Department, Nurse_Dept.dept_id == Department.id) \
         .all()

        nurses_list = [{
            "id": nurse.id,
            "name": nurse.name,
            "birth_date": nurse.birth_date,
            "email": nurse.email,
            "department": nurse.department_name
        } for nurse in nurses]

        return jsonify(nurses_list), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@nurse_routes_bp.route("/get/nurse/<string:nurse_id>", methods=["GET"])
@jwt_required()
def get_nurse(nurse_id):
    try:
        nurse = db.session.query(
            Nurse.id,
            Nurse.name,
            Nurse.birth_date,
            User.email,
            Department.name.label('department_name')
        ).join(User, Nurse.id == User.user_id) \
         .join(Nurse_Dept, Nurse.id == Nurse_Dept.nurse_id) \
         .join(Department, Nurse_Dept.dept_id == Department.id) \
         .filter(Nurse.id == nurse_id) \
         .first()

        if not nurse:
            return jsonify({"error": "Nurse not found"}), 404

        nurse_info = {
            "id": nurse.id,
            "name": nurse.name,
            "birth_date": nurse.birth_date,
            "email": nurse.email,
            "department": nurse.department_name
        }

        return jsonify(nurse_info), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@nurse_routes_bp.route("/get/nurse/<string:nurse_id>", methods=["PUT","PATCH"])
@jwt_required()
def update_nurse(nurse_id):
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 403

    try:
        nurse = Nurse.query.filter_by(id=nurse_id).first()
        if not nurse:
            return jsonify({"error": "User not found"}), 404

        data = request.json
        name = data.get("name")
        birth_date_str = data.get("birth_date")
        department_id = data.get("department_id")
        email = data.get("email")

        if name:
            nurse.name = name

        if birth_date_str:
            nurse.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

        if department_id:
            department = Department.query.filter_by(id=department_id).first()
            if department:
                department.dept_id = department_id
            else:
                return jsonify({"error": "Department not exists"}), 404

        if email:
            user = User.query.filter_by(user_id=nurse.id).first()
            if user:
                user.email = email
            else:
                return jsonify({"error": "User not found"}), 404
        db.session.commit()
        return jsonify({"message":"Information updated successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500


@nurse_routes_bp.route("/nurse/<string:nurse_id>", methods=["DELETE"])
@jwt_required()
def delete_nurse(nurse_id):
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 403

    try:
        nurse = Nurse.query.filter_by(id=nurse_id).first()
        if not nurse:
            return jsonify({"error": "User not found"}), 404

        Nurse_Dept.query.filter_by(nurse_id=nurse.id).delete()
        User.query.filter_by(user_id=nurse.id).delete()

        db.session.delete(nurse)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
