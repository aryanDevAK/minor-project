from flask import Blueprint, request, jsonify, abort
from models.patient_mobile_num import Patient_User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

login_patient_bp = Blueprint("login_patient", __name__)

@login_patient_bp.route("/login/patient", methods=["POST"])
def login_patient():
    mobile_num = request.json.get("mobile_num")

    if not mobile_num:
        return jsonify({"message": "Required mobile number"}), 401

    patient = Patient_User.query.filter_by(mobile_num=mobile_num).first()
    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    if patient.role == "patient":
        access_token = create_access_token(identity=patient.mobile_num)
        refresh_token = create_refresh_token(identity=patient.mobile_num)
        return jsonify({"access_token": access_token, "refresh_token": refresh_token, "message":"Successfully logged in"}), 200
    else:
        return jsonify({"message": "Patient not registered"}), 403