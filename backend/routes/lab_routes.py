from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from models.user import User
from models.labs import Lab
from models.department import Department
from models.labDept import Lab_Dept
from models.dbConfig import db
import sqlalchemy
from routes.helper_function import str_to_date, has_required_role

lab_bp = Blueprint("lab_bp", __name__)
@lab_bp.route("/register/lab", methods=["POST"])
@jwt_required()
def register_lab():
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 403

    try:
        name = request.json.get("name")
        license_num = request.json.get("license_num")
        dept_id = request.json.get("dept_id")
        email = request.json.get("email")
        password = request.json.get("password")
        role = request.json.get("role")

        if not all([name, license_num, dept_id, email, password, role]):
            return jsonify({"error": "All fields are required"}), 400

        lab_exists = Lab.query.filter_by(license_num=license_num).first() is not None
        if lab_exists:
            return jsonify({"error": "Lab already exists"}), 409

        dept = Department.query.filter_by(id=dept_id).first()
        if not dept:
            return jsonify({"error": "Department not found"}), 404
        hashed_password = generate_password_hash(password)

        new_lab = Lab(name=name, license_num=license_num)
        db.session.add(new_lab)
        db.session.flush()

        new_lab_dept = Lab_Dept(lab_id=new_lab.id, dept_id=dept_id)
        new_user = User(user_id=new_lab.id, email=email, password=hashed_password, role=role)

        db.session.add(new_lab_dept)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registered Successfully"}), 201

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@lab_bp.route("/labs", methods=["GET"])
@jwt_required()
def get_all_labs():
    try:
        labs = Lab.query.all()
        all_labs = []
        for lab in labs:
            lab_dept = Lab_Dept.query.filter_by(lab_id=lab.id).first()
            user = User.query.filter_by(user_id=lab.id).first()

            lab_data = {
                "id": lab.id,
                "name": lab.name,
                "license_num": lab.license_num,
                "dept_id": lab_dept.dept_id if lab_dept else None,
                "email": user.email if user else None,
                "role": user.role if user else None
            }
            all_labs.append(lab_data)

        return jsonify(all_labs), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@lab_bp.route("/lab/<string:lab_id>", methods=["GET"])
@jwt_required()
def get_lab(lab_id):
    try:
        lab = Lab.query.filter_by(id=lab_id).first()
        if not lab:
            return jsonify({"error": "Lab not found"}), 404

        lab_dept = Lab_Dept.query.filter_by(lab_id=lab.id).first()
        user = User.query.filter_by(user_id=lab.id).first()

        return jsonify({
            "id": lab.id,
            "name": lab.name,
            "license_num": lab.license_num,
            "dept_id": lab_dept.dept_id if lab_dept else None,
            "email": user.email if user else None,
            "role": user.role if user else None
        }), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@lab_bp.route("/lab/<string:lab_id>", methods=["PUT","PATCH"])
@jwt_required()
def update_lab(lab_id):
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 403

    try:
        lab = Lab.query.filter_by(id=lab_id).first()
        if not lab:
            return jsonify({"error": "Lab not found"}), 404

        name = request.json.get("name")
        dept_id = request.json.get("dept_id")
        email = request.json.get("email")
        role = request.json.get("role")

        if name:
            lab.name = name
        
        if dept_id:
            dept = Department.query.filter_by(id=dept_id).first()
            if dept:
                lab_dept = Lab_Dept.query.filter_by(lab_id=lab.id).first()
                if lab_dept:
                    lab_dept.dept_id = dept_id
                else:
                    new_lab_dept = Lab_Dept(lab_id=lab.id, dept_id=dept_id)
                    db.session.add(new_lab_dept)
            else:
                return jsonify({"error": "Department not found"}), 404

        if email or role:
            user = User.query.filter_by(user_id=lab.id).first()
            if email:
                user.email = email
            if role:
                user.role = role

        db.session.commit()

        return jsonify({"message": "Lab updated successfully"}), 200

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@lab_bp.route("/lab/<string:lab_id>", methods=["DELETE"])
@jwt_required()
def delete_lab(lab_id):
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 403

    try:
        lab = Lab.query.filter_by(id=lab_id).first()
        if not lab:
            return jsonify({"error": "Lab not found"}), 404

        Lab_Dept.query.filter_by(lab_id=lab.id).delete()
        User.query.filter_by(user_id=lab.id).delete()

        db.session.delete(lab)
        db.session.commit()

        return jsonify({"message": "Lab deleted successfully"}), 200

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
