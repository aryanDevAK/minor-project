from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.dbConfig import db
from models.doctor import Doctor
from models.nurse import Nurse
from models.patient import Patient
from models.staff import Staff
from models.department import Department
from models.labs import Lab
from models.appointment import Appointment
from datetime import datetime, date
import sqlalchemy

count_routes_bp = Blueprint("counter", __name__)

@count_routes_bp.route("/get/count", methods=["GET"])
@jwt_required()
def counter():
    try:
        doctor_count = Doctor.query.count()
        patient_count = Patient.query.count()
        nurse_count = Nurse.query.count()
        staff_count = Staff.query.count()
        department_count = Department.query.count()
        lab_count = Lab.query.count()
        appointment_count = Appointment.query.count()

        count_list = {
            "total_doctor": {"name": "Total Doctors", "count": doctor_count},
            "total_nurse": {"name": "Total Nurses", "count": nurse_count},
            "total_staff": {"name": "Total Staff", "count": staff_count},
            "total_patient": {"name": "Total Patients", "count": patient_count},  # Fixed patient_count
            "total_department": {"name": "Total Departments", "count": department_count},
            "total_lab": {"name": "Total Labs", "count": lab_count},
            "total_appointment": {"name": "Total Appointments", "count": appointment_count}
        }

        return jsonify(count_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred while counting records: {str(e)}"}), 500