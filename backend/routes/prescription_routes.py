from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.dbConfig import db
from models.prescription import Prescription
from models.prescription_patient_doc import Prescription_Patient_Doctor
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
import sqlalchemy.exc
from routes.helper_function import str_to_date, has_required_role


prescription_bp = Blueprint('prescription', __name__)
@prescription_bp.route('/prescription', methods=['POST'])
@jwt_required()
def create_prescription():
    if not has_required_role(["admin", "doctor", "nurse"]):
        return jsonify({"message": "You do not have permission to do that"}), 401
    try:
        patient_id = request.json.get('patient_id')
        doc_id = request.json.get('doc_id')
        medications = request.json.get('medications')
        dosage = request.json.get('dosage')
        appointment_id = request.json.get('appointment_id')

        if not patient_id or not doc_id:
            return jsonify({"error": "All fields are required"}), 400
        
        patient = Patient.query.filter_by(id=patient_id).first()
        doctor = Doctor.query.filter_by(id=doc_id).first()
        appointment = Appointment.query.filter_by(id=appointment_id).first()

        if not patient:
            return jsonify({"error": "Patient not found"}), 404
        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404
        
        new_prescription = Prescription(medications=medications, dosage=dosage)
        db.session.add(new_prescription)
        db.session.flush()

        prescription_patient_doctor = Prescription_Patient_Doctor(
            patient_id=patient_id,
            doc_id=doc_id,
            prescription_id=new_prescription.id,
            appointment_id=appointment_id
        )
        db.session.add(prescription_patient_doctor)
        db.session.commit()

        return jsonify({"message": "Prescription successfully created"}), 201

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@prescription_bp.route('/prescription/id/<string:prescription_id>', methods=['GET'])
@jwt_required()
def get_prescription_by_id(prescription_id):
    try:
        prescription = db.session.query(
            Prescription.id,
            Prescription.medications,
            Prescription.dosage,
            Prescription_Patient_Doctor.appointment_id,
            Doctor.name.label("doc_name"),
            Patient.name.label("patient_name")
        ).join(Prescription_Patient_Doctor, Prescription.id == Prescription_Patient_Doctor.prescription_id) \
         .join(Doctor, Doctor.id == Prescription_Patient_Doctor.doc_id) \
         .join(Patient, Patient.id == Prescription_Patient_Doctor.patient_id) \
         .filter(Prescription.id == prescription_id) \
         .first()

        if not prescription:
            return jsonify({"message": "Prescription not found"}), 404

        prescription_data = {
            "id": prescription.id,
            "medications": prescription.medications,
            "dosage": prescription.dosage,
            "appointment_id": prescription.appointment_id,
            "doc_name": prescription.doc_name,
            "patient_name": prescription.patient_name
        }

        return jsonify(prescription_data), 200

    except Exception as e:
        # In case of any error, return the error message
        return jsonify({"error": str(e)}), 500

@prescription_bp.route('/prescription/<string:patient_id>', methods=['GET'])
@jwt_required()
def get_prescriptions_by_patient(patient_id):
    try:
        patient = Patient.query.filter_by(id=patient_id).first()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        prescriptions = db.session.query(
            Prescription.id,
            Prescription.medications,
            Prescription.dosage,
            Prescription_Patient_Doctor.appointment_id,
            Doctor.name.label("doc_name")
        ).join(Prescription_Patient_Doctor, Prescription.id == Prescription_Patient_Doctor.prescription_id) \
         .join(Doctor, Doctor.id==Prescription_Patient_Doctor.doc_id) \
         .filter(Prescription_Patient_Doctor.patient_id == patient_id) \
         .all()

        if not prescriptions:
            return jsonify({"message": "No prescriptions found for this patient"}), 404

        prescription_list = [{
            "id":prescription.id,
            "medications":prescription.medications,
            "dosage":prescription.dosage,
            "appointment_id":prescription.appointment_id,
            "doc_name":prescription.doc_name
        } for prescription in prescriptions]

        return jsonify(prescription_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@prescription_bp.route('/prescription/appointment/<string:appointment_id>', methods=['GET'])
@jwt_required()
def get_prescription_by_appointment(appointment_id):
    try:
        prescriptions = db.session.query(
            Prescription.id,
            Prescription.medications,
            Prescription.dosage,
            Prescription_Patient_Doctor.appointment_id,
            Doctor.name.label("doc_name")
        ).join(Prescription_Patient_Doctor, Prescription.id == Prescription_Patient_Doctor.prescription_id) \
         .join(Doctor, Doctor.id==Prescription_Patient_Doctor.doc_id) \
         .filter(Prescription_Patient_Doctor.appointment_id == appointment_id) \
         .all()

        if not prescriptions:
            return jsonify({"message": "No prescription found for this appointment"}), 404

        prescription_list = [{
            "id":prescription.id,
            "medications":prescription.medications,
            "dosage":prescription.dosage,
            "doc_name":prescription.doc_name
        }for prescription in prescriptions]
        return jsonify(prescription_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@prescription_bp.route('/prescription/doctor/<string:doc_id>', methods=['GET'])
@jwt_required()
def get_prescriptions_by_doctor(doc_id):
    try:
        doctor = Doctor.query.filter_by(id=doc_id).first()
        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

        prescriptions = db.session.query(
            Prescription.id,
            Prescription.medications,
            Prescription.dosage,
            Prescription_Patient_Doctor.appointment_id,
            Patient.name.label("patient_name")
        ).join(Prescription_Patient_Doctor, Prescription.id == Prescription_Patient_Doctor.prescription_id) \
         .join(Patient, Patient.id == Prescription_Patient_Doctor.patient_id) \
         .filter(Prescription_Patient_Doctor.doc_id == doc_id) \
         .all()

        # If no prescriptions are found
        if not prescriptions:
            return jsonify({"message": "No prescriptions found for this doctor"}), 404

        prescription_list = [{
            "id": prescription.id,
            "medications": prescription.medications,
            "dosage": prescription.dosage,
            "appointment_id": prescription.appointment_id,
            "patient_name": prescription.patient_name
        } for prescription in prescriptions]

        return jsonify(prescription_list), 200

    except Exception as e:
        # In case of any error, return the error message
        return jsonify({"error": str(e)}), 500

@prescription_bp.route('/prescription/<string:prescription_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_prescription(prescription_id):
    if not has_required_role(["admin", "doctor"]):
        return jsonify({"message": "You do not have permission to do that"}), 401
    try:
        prescription = Prescription.query.filter_by(id=prescription_id).first()
        if not prescription:
            return jsonify({"error": "Prescription not found"}), 404

        medications = request.json.get('medications')
        dosage = request.json.get('dosage')

        if medications:
            prescription.medications = medications
        if dosage:
            prescription.dosage = dosage

        db.session.commit()

        return jsonify({"message": "Prescription updated successfully"}), 200

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@prescription_bp.route('/prescription/<string:prescription_id>', methods=['DELETE'])
@jwt_required()
def delete_prescription(prescription_id):
    if not has_required_role(["admin", "doctor", "nurse"]):
        return jsonify({"message": "You do not have permission to do that"}), 401
        
    try:
        prescription = Prescription.query.filter_by(id=prescription_id).first()
        if not prescription:
            return jsonify({"error": "Prescription not found"}), 404

        Prescription_Patient_Doctor.query.filter_by(prescription_id=prescription_id).delete()
        db.session.delete(prescription)
        db.session.commit()

        return jsonify({"message": "Prescription deleted successfully"}), 200

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
