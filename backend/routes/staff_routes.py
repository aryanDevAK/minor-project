from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from models.dbConfig import db
from models.staff import Staff
from models.user import User
from models.department import Department
from models.staffDept import Staff_Dept
from datetime import datetime
import sqlalchemy
from routes.helper_function import str_to_date, has_required_role


staff_routes_bp = Blueprint("register_staff", __name__)
@staff_routes_bp.route("/register/staff", methods=["POST"])
@jwt_required()
def register_staff():
    if not has_required_role(["admin"]):
        return jsonify({"message" : "You do not have permission to do that"}), 404

    try:
        name = request.json.get("name")
        birth_date_str = request.json.get("birth_date")
        gender = request.json.get("gender")
        mobile_num = request.json.get("mobile_num")
        email = request.json.get("email")
        password = request.json.get("password")
        department_id = request.json.get("department_id")
        role = request.json.get("role")

        if not name or not email or not password or not role or not birth_date_str or not gender or not mobile_num:
            return jsonify({"error": "All fields are required"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User already exists"}), 409

        if not Department.query.filter_by(id=department_id).first():
            return jsonify({"error": "Department not exists"}), 404

        birth_date = str_to_date(birth_date_str)
        hashed_password = generate_password_hash(password)

        new_staff = Staff(name=name, birth_date=birth_date, gender=gender, mobile_num=mobile_num)
        new_user = User(user_id=new_staff.id, email=email, password=hashed_password, role=role)
        new_assignment = Staff_Dept(staff_id=new_staff.id,dept_id=department_id)

        db.session.add(new_staff)
        db.session.add(new_user)
        db.session.add(new_assignment)
        db.session.commit()

        return jsonify({"message":"User registered successfully"}), 201

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@staff_routes_bp.route("/get/staff", methods=["GET"])
@jwt_required()
def get_staff():
    try:
        staff_members = db.session.query(
            Staff.id, 
            Staff.name, 
            Staff.birth_date, 
            Staff.gender, 
            Staff.mobile_num, 
            User.email, 
            User.role,
            Department.name.label("department_name")
        ).join(User, Staff.id == User.user_id) \
         .join(Staff_Dept, Staff.id == Staff_Dept.staff_id) \
         .join(Department, Staff_Dept.dept_id == Department.id) \
         .all()

        staff_list = [{
            "id": staff_member.id,
            "name": staff_member.name,
            "birth_date": staff_member.birth_date,
            "gender": staff_member.gender,
            "mobile_num": staff_member.mobile_num,
            "email": staff_member.email,
            "role": staff_member.role,
            "department":staff_member.department_name
        } for staff_member in staff_members]

        return jsonify(staff_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@staff_routes_bp.route("/get/staff/<string:staff_id>", methods=["GET"])
@jwt_required()
def get_staff_member(staff_id):
    try:
        staff_member = db.session.query(
            Staff.id, 
            Staff.name, 
            Staff.birth_date, 
            Staff.gender, 
            Staff.mobile_num, 
            User.email, 
            User.role,
            Department.name.label("department_name")
        ).join(User, Staff.id == User.user_id) \
         .join(Staff_Dept, Staff.id == Staff_Dept.staff_id) \
         .join(Department, Staff_Dept.dept_id == Department.id) \
         .filter(Staff.id == staff_id).first()

        if not staff_member:
            return jsonify({"error": "Staff member not found"}), 404

        staff_info = {
            "id": staff_member.id,
            "name": staff_member.name,
            "birth_date": staff_member.birth_date.strftime('%d-%m-%Y'),
            "gender": staff_member.gender,
            "mobile_num": staff_member.mobile_num,
            "email": staff_member.email,
            "role": staff_member.role,
            "department":staff_member.department_name
        }

        return jsonify(staff_info), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@staff_routes_bp.route("/update/staff/<string:staff_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_staff(staff_id):
    if not has_required_role(["admin"]):
        return jsonify({"message" : "You do not have permission to do that"}), 404

    try:
        staff = Staff.query.filter_by(id=staff_id).first()
        if not staff:
            return jsonify({"error": "User not found"}), 404

        name = request.json.get("name")
        birth_date_str = request.json.get("birth-date")
        gender = request.json.get("gender")
        mobile_num = request.json.get("mobile_num")
        email = request.json.get("email")
        department_id = request.json.get("department_id")
        role = request.json.get("role")

        if name:
            staff.name = name
        if birth_date_str:
            staff.birth_date = str_to_date(birth_date_str)
        if gender:
            staff.gender = gender
        if mobile_num:
            staff.mobile_num = mobile_num
        if department_id:
            assignment = Staff_Dept.query.filter_by(staff_id=staff.id).first()
            if assignment:
                assignment.dept_id = department_id
            else:
                return jsonify({"message":"User not assigned to any department"}),403
        if email:
            user = User.query.filter_by(user_id=staff.id).first()
            if user:
                user.email = email
            else:
                return jsonify({"error": "User not found"}), 404
        if role:
            user = User.query.filter_by(user_id=staff.id).first()
            user.role = role

        db.session.commit()

        return jsonify({"message": "User updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@staff_routes_bp.route("/delete/staff/<string:staff_id>", methods=["DELETE"])
@jwt_required()
def delete_staff(staff_id):
    if not has_required_role(["admin"]):
        return jsonify({"message" : "You do not have permission to do that"}), 404

    try:
        staff = Staff.query.filter_by(id=staff_id).first()
        if not staff:
            return jsonify({"error": "Staff member not found"}), 404

        User.query.filter_by(user_id=staff.id).delete()
        # Staff_Dept.filter_by(staff_id=staff.id).delete()
        db.session.delete(staff)
        db.session.commit()

        return jsonify({"message": "Staff member deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
