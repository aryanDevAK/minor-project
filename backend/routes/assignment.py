from flask import Blueprint, request, jsonify
from models.dbConfig import db
from models.docDept import Doc_Dept
from models.nurseDept import Nurse_Dept
from models.doctor import Doctor
from models.nurse import Nurse
from models.department import Department
import sqlalchemy.exc

register_assign_doc_dept_bp = Blueprint('assign_doc_dept', __name__)
@register_assign_doc_dept_bp.route("/assign/doctor-department", methods=["POST"])
def assign_doctor_to_department():
    try:
        doctor_id = request.json.get("doctor_id")
        department_id = request.json.get("department_id")

        if not doctor_id or not department_id:
            return jsonify({"error": "Doctor ID and Department ID are required"}), 400

        doctor = Doctor.query.filter_by(id=doctor_id).first()
        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

        department = Department.query.filter_by(id=department_id).first()
        if not department:
            return jsonify({"error": "Department not found"}), 404

        existing_assignment = Doc_Dept.query.filter_by(doc_id=doctor_id, dept_id=department_id).first()
        if existing_assignment:
            return jsonify({"error": "Assignment already exists"}), 409

        new_assignment = Doc_Dept(doc_id=doctor_id, dept_id=department_id)
        db.session.add(new_assignment)
        db.session.commit()

        return jsonify({
            "doctor_id": doctor_id,
            "department_id": department_id,
            "department_name": department.name
        }), 201

        # return ({"message":"Successfully Assigned"}), 201

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred: " + str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

register_assign_nurse_dept_bp = Blueprint('assign_nurse_dept', __name__)
@register_assign_doc_dept_bp.route("/assign/nurse-department", methods=["POST"])
def assign_nurse_to_department():
    try:
        nurse_id = request.json.get("nurse_id")
        department_id = request.json.get("department_id")

        if not nurse_id or not department_id:
            return jsonify({"error": "Doctor ID and Department ID are required"}), 400

        nurse = Nurse.query.filter_by(id=nurse_id).first()
        if not nurse:
            return jsonify({"error": "Nurse not found"}), 404

        department = Department.query.filter_by(id=department_id).first()
        if not department:
            return jsonify({"error": "Department not found"}), 404

        existing_assignment = Nurse_Dept.query.filter_by(nurse_id=nurse_id, dept_id=department_id).first()
        if existing_assignment:
            return jsonify({"error": "Assignment already exists"}), 409

        new_assignment = Nurse_Dept(nurse_id=nurse_id, dept_id=department_id)
        db.session.add(new_assignment)
        db.session.commit()

        return jsonify({
            "nurse_id": nurse_id,
            "department_id": department_id,
            "department_name": department.name
        }), 201

        # return ({"message":"Successfully Assigned"}), 201

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred: " + str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
