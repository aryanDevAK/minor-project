# routes/register.py
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.dbConfig import db
from models.user import User
from models.doctor import Doctor
from models.docDept import Doc_Dept
from models.department import Department
from models.nurse import Nurse
from models.staff import Staff
from models.room import Room
from models.labs import Lab
from models.labDept import Lab_Dept
from models.patient import Patient
from models.patient_mobile_num import Patient_Mobile_Num, Patient_User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import sqlalchemy.exc

def str_to_date(birth_date):
    try:
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        return birth_date
    except ValueError:
        return jsonify({"error": "Invalid birth_date format. Use YYYY-MM-DD."}), 400

def has_required_role(required_roles):
    identity = get_jwt_identity()
    user_id = identity.get("id")
    user_role = identity.get("role")

    if not user_id or not user_role:
        return False

    return user_role in required_roles

# register_doc_bp = Blueprint("register_doctor", __name__)
# @register_doc_bp.route("/register/doctor", methods=["POST"])
# @jwt_required()
# def register_doctor():
    if not has_required_role(["admin"]):
        return jsonify({"message" : "You do not have permission to do that"}), 401

    try:
        name = request.json.get("name")
        birth_date_str = request.json.get("birth-date")
        speciality = request.json.get("speciality")
        email = request.json.get("email")
        password = request.json.get("password")
        department_id = request.json.get("department_id")
        role = "doctor"

        if not all([name, email, password, role, birth_date_str, speciality, department_id]):
            return jsonify({"message": "All fields (name, email, password, role, birth_date, speciality, department_id) are required"}), 400

        user_exists = User.query.filter_by(email=email).first() is not None
        if user_exists:
            return jsonify({"message": "Doctor already exists"}), 409

        department = Department.query.filter_by(id=department_id).first()
        if not department:
            return jsonify({"error": "Department not found"}), 404


        birth_date = str_to_date(birth_date_str)
        hashed_password = generate_password_hash(password)

        new_doctor = Doctor(name=name, birth_date=birth_date, speciality=speciality)
        db.session.add(new_doctor)

        new_user = User(user_id=new_doctor.id, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        
        new_assignment = Doc_Dept(doc_id=new_doctor.id, dept_id=department_id)
        db.session.add(new_assignment)
        
        db.session.commit()

        # return jsonify({"message":"Doctor registered"})
        return jsonify({"id":new_doctor.id,"name":new_doctor.name,"speciality":new_doctor.speciality, "email":new_user.email,"password":new_user.password,"role":new_user.role }), 201

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

# register_dept_bp = Blueprint("register_department",__name__)
# @register_dept_bp.route("/register/department", methods=["POST"])
# @jwt_required()
# def register_department():
#     if not has_required_role(["admin"]):
#         return jsonify({"message" : "You do not have permission to do that"})
#     try:
#         dept_name = request.json.get("name")

#         if not dept_name:
#             return jsonify({"error": "Department Name required"}), 400

#         department_exists = Department.query.filter_by(name=dept_name).first() is not None
#         if department_exists:
#             return jsonify({"error": "Department already exists"}), 409

#         new_department = Department(name=dept_name)
#         db.session.add(new_department)
#         db.session.commit()

#         return jsonify({
#             "id": new_department.id,
#             "name": new_department.name,
#         }), 201
#         # return jsonify({"message":"Department created Successfully"}), 201

#     except sqlalchemy.exc.IntegrityError:
#         db.session.rollback()
#         return jsonify({"error": "Database integrity error occurred"}), 500

#     except sqlalchemy.exc.SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

# register_nurse_bp = Blueprint("register_nurse", __name__)
# @register_nurse_bp.route("/register/nurse", methods=["POST"])
# @jwt_required()
# def register_nurse():
#     if not has_required_role(["admin"]):
#         return jsonify({"message" : "You do not have permission to do that"})

#     try:
#         name = request.json.get("name")
#         birth_date_str = request.json.get("birth_date")
#         email = request.json.get("email")
#         password = request.json.get("password")
#         department_id = request.json.get("department_id")
#         role = request.json.get("role")

#         if not name and not email and not password and not role and not birth_date_str and not department_id:
#             return jsonify({"error": "All fields (name, email, password, role, birth_date) are required"}), 400

#         user_exists = User.query.filter_by(email=email).first() is not None
#         if user_exists:
#             return jsonify({"error": "Nurse already exists"}), 409

#         department = Department.query.filter_by(id=department_id).first()
#         if not department:
#             return jsonify({"error": "Department not found"}), 404

#         birth_date = str_to_date(birth_date_str)
#         hashed_password = generate_password_hash(password)

#         new_nurse = Nurse(name=name, birth_date=birth_date)
#         db.session.add(new_nurse)

#         new_assignment = Nurse_Dept(nurse_id=nurse_id, dept_id=department_id)
#         db.session.add(new_assignment)

#         new_user = User(user_id=new_nurse.id, email=email, password=hashed_password, role=role)
#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify({
#             "id": new_nurse.id,
#             "name": new_nurse.name,
#             "birth_date": new_nurse.birth_date.strftime('%Y-%m-%d'),
#             "email": new_user.email,
#             "role": new_user.role
#         }), 201

#     except sqlalchemy.exc.IntegrityError:
#         db.session.rollback()
#         return jsonify({"error": "Database integrity error occurred"}), 500

#     except sqlalchemy.exc.SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

# register_staff_bp = Blueprint("register_staff", __name__)
# @register_staff_bp.route("/register/staff", methods=["POST"])
# @jwt_required()
# def register_staff():
#     if not has_required_role(["admin"]):
#         return jsonify({"message" : "You do not have permission to do that"}), 404

#     try:
#         name = request.json.get("name")
#         birth_date_str = request.json.get("birth-date")
#         gender = request.json.get("gender")
#         mobile_num = request.json.get("mobile_num")
#         email = request.json.get("email")
#         password = request.json.get("password")
#         role = request.json.get("role")

#         if not name or not email or not password or not role or not birth_date_str or not gender or not mobile_num:
#             return jsonify({"error": "All fields (name, email, password, role, birth_date) are required"}), 400

#         user_exists = User.query.filter_by(email=email).first() is not None
#         if user_exists:
#             return jsonify({"error": "Employee already exists"}), 409

#         birth_date = str_to_date(birth_date_str)
#         hashed_password = generate_password_hash(password)

#         new_staff = Staff(name=name, birth_date=birth_date, gender=gender, mobile_num=mobile_num)
#         new_user = User(user_id=new_staff.id, email=email, password=hashed_password, role=role)

#         db.session.add(new_staff)
#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify({
#             "id": new_staff.id,
#             "name": new_staff.name,
#             "birth_date": new_staff.birth_date.strftime('%Y-%m-%d'),
#             "gender": new_staff.gender,
#             "mobile_num": new_staff.mobile_num,
#             "email": new_user.email,
#             "password": new_user.password,
#             "role": new_user.role
#         }), 201

#     except sqlalchemy.exc.IntegrityError:
#         db.session.rollback()
#         return jsonify({"error": "Database integrity error occurred"}), 500

#     except sqlalchemy.exc.SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

register_room_bp = Blueprint("register_room", __name__)
@register_room_bp.route("/register/room", methods=["POST"])
@jwt_required()
def register_room():
    if not has_required_role(["admin"]):
        return jsonify({"message" : "You do not have permission to do that"})

    try:
        room_type = request.json.get("room_type")
        total_capacity = request.json.get("total_capacity")
        price = request.json.get("price")

        if not room_type or not total_capacity or not price:
            return jsonify({"error": "All fields are required"}), 400

        new_room = Room(room_type=room_type, total_capacity=total_capacity, price=price)

        db.session.add(new_room)
        db.session.commit()

        return jsonify({
            "id": new_room.id,
            "room_type": new_room.room_type,
            "total_capacity": new_room.total_capacity,
            "occupied_capacity": new_room.occupied_capacity,
            "price": new_room.price
        }), 201

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

register_lab_bp = Blueprint("register_lab", __name__)
@register_lab_bp.route("/register/lab", methods=["POST"])
@jwt_required()
def register_lab():
    if not has_required_role(["admin"]):
        return jsonify({"message" : "You do not have permission to do that"})

    try:
        name = request.json.get("name")
        license_num = request.json.get("license_num")
        dept_id = request.json.get("dept_id")
        email = request.json.get("email")
        password = request.json.get("password")
        role = request.json.get("role")

        if not name and not license_num and not dept_id and not email and not password and not role:
            return jsonify({"error": "All fields are required"}), 400

        lab_exists = Lab.query.filter_by(license_num=license_num).first() is not None
        if lab_exists:
            return jsonify({"error": "Lab already exists"}), 409

        hashed_password = generate_password_hash(password)

        new_lab = Lab(name=name, license_num=license_num)
        new_lab_dept = Lab_Dept(lab_id=new_lab.id, dept_id=dept_id)
        new_user = User(user_id=new_lab.id, email=email, password=hashed_password, role=role)

        db.session.add(new_lab)
        db.session.add(new_lab_dept)
        db.session.add(new_user)
        db.session.commit()

        return({"message" : "Registered Successfully"})
        
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

register_patient_bp = Blueprint("register_patient", __name__)
@register_patient_bp.route("/register/patient", methods=["POST"])
@jwt_required()
def register_patient():
    if not has_required_role(["doctor", "nurse", "admin"]):
        return jsonify({"message" : "You do not have permission to do that"})

    try:
        name = request.json.get("name")
        birth_date_str = request.json.get("birth-date")
        mobile_num = request.json.get("mobile-num")

        if not name and not birth_date_str and not mobile_num:
            return jsonify({"error": "All fields are required"}), 400
        
        patient_exists = Patient_Mobile_Num.query.filter_by(mobile_num=mobile_num).first() is not None
        if patient_exists:
            return jsonify({"error": "Patient exists. You can directly book an appointment"}), 409

        birth_date = str_to_date(birth_date_str)

        new_patient = Patient(name=name, birth_date=birth_date)
        new_patient_num = Patient_Mobile_Num(id=new_patient.id, mobile_num=mobile_num)
        new_patient_user = Patient_User(mobile_num=mobile_num)

        db.session.add(new_patient)
        db.session.add(new_patient_num)
        db.session.add(new_patient_user)
        db.session.commit()

        return({"message":"Succefully Registered"})
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500


