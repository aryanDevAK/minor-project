from flask import Blueprint, request, jsonify, abort
from models.dbConfig import db
from models.record import Record
from models.patientRecord import Patient_Record
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

def has_required_role(required_roles):
    identity = get_jwt_identity()
    user_id = identity.get("id")
    user_role = identity.get("role")

    if not user_id or not user_role:
        return False

    return user_role in required_roles

create_patient_record = Blueprint("create_patient_record", __name__)
@create_patient_record.route("/create/record", methods=["POST"])
@jwt_required()
def create_record_for_patient():
    if not has_required_role(["admin", "nurse", "doctor"]):
        return jsonify({"message": "You do not have permission to do that"}), 403
    
    data = request.get_json()
    patient_id = data.get("patient_id")
    body_temp = data.get("body_temp")
    blood_pressure = data.get("blood_pressure")
    spo = data.get("spo")

    if not patient_id:
        return jsonify({"message": "Patient ID is required"}), 400

    new_record_id = generate_custom_id(Record, 'REC')
    record = Record(id=new_record_id, body_temp=body_temp, blood_pressure=blood_pressure, spo=spo)
    db.session.add(record)

    patient_record = Patient_Record(patient_id=patient_id, record_id=new_record_id, nurse_id=user_id)
    db.session.add(patient_record)

    db.session.commit()

    return jsonify({"message": "Record created successfully."}), 201

# @create_patient_record.route("/update/record", methods=["PATCH"])
# @jwt_required()
# def update_record_for_patient():
#     if not has_required_role(["admin", "nurse", "doctor"]):
#         return jsonify({"message": "You do not have permission to do that"}), 403
    
#     data = request.get_json()
#     patient_id = data.get("patient_id")
#     body_temp = data.get("body_temp")
#     blood_pressure = data.get("blood_pressure")
#     spo = data.get("spo")

#     if not patient_id:
#         return jsonify({"message": "Patient ID is required"}), 400

#     # Find existing record by patient_id
#     patient_record = Patient_Record.query.filter_by(patient_id=patient_id).first()

#     if not patient_record:
#         return jsonify({"message": "Patient record not found"}), 404

#     record = Record.query.filter_by(id=patient_record.record_id).first()
#     if not record:
#         return jsonify({"message": "Record not found"}), 404

#     record.body_temp = body_temp or record.body_temp
#     record.blood_pressure = blood_pressure or record.blood_pressure
#     record.spo = spo or record.spo

#     db.session.commit()

#     return jsonify({"message": "Record updated successfully."}), 200
