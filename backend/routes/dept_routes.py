from models.department import Department
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.dbConfig import db
import sqlalchemy.exc
from routes.helper_function import str_to_date, has_required_role

dept_routes_bp = Blueprint("department_routes", __name__)

@dept_routes_bp.route("/register/department", methods=["POST"])
@jwt_required()
def register_department():
    if not has_required_role(["admin"]):
        return jsonify({"message" : "You do not have permission to do that"})
    try:
        dept_name = request.json.get("name")

        if not dept_name:
            return jsonify({"error": "Name is required"}), 400

        department_exists = Department.query.filter_by(name=dept_name).first() is not None
        if department_exists:
            return jsonify({"error": "Department already exists"}), 409

        new_department = Department(name=dept_name)
        db.session.add(new_department)
        db.session.commit()

        return jsonify({"message":"Registered Successfully"}), 201

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@dept_routes_bp.route("/get/departments", methods=["GET"])
@jwt_required()
def get_departments():
    try:
        departments = Department.query.all()

        department_list = [{"id": dept.id, "name": dept.name} for dept in departments]
        
        return jsonify(department_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dept_routes_bp.route("/get/department/<string:id>", methods=["GET"])
@jwt_required()
def get_department(id):
    try:
        department = Department.query.get(id)
        
        if not department:
            return jsonify({"error": "Department not found"}), 404
        
        return jsonify({
            "id": department.id,
            "name": department.name
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dept_routes_bp.route("/department/<string:dept_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_department(dept_id):
    if not has_required_role(["admin"]):
        return jsonify({"message" : "You do not have permission to do that"}), 403

    try:
        department = Department.query.filter_by(id=dept_id).first()

        if not department:
            return jsonify({"error": "Department not found"}), 404

        dept_name = request.json.get("name")

        if not dept_name:
            return jsonify({"error": "Department name is required"}), 400

        department_exists = Department.query.filter_by(id=department.id).first()
        if department_exists:
            department_exists.name = dept_name

        db.session.commit()

        return jsonify({"message": "Updated Successfully"
        }), 200

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@dept_routes_bp.route("/department/<string:id>", methods=["DELETE"])
@jwt_required()
def delete_department(id):
    if not has_required_role(["admin"]):
        return jsonify({"message" : "You do not have permission to do that"}), 403

    try:
        department = Department.query.get(id)

        if not department:
            return jsonify({"error": "Department not found"}), 404

        db.session.delete(department)
        db.session.commit()

        return jsonify({"message": "Department deleted successfully"}), 200

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
