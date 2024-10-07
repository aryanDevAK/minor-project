from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.dbConfig import db
from models.Prescription import Prescription, generate_custom_id
from models.Prescription_Patient_Doctor import Prescription_Patient_Doctor
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
import sqlalchemy.exc

# Define Blueprint
prescription_bp = Blueprint('prescription', __name__)

# CREATE Operation for Prescription (Assign Prescription to a Patient and Doctor)
@prescription_bp.route('/prescription', methods=['POST'])
@jwt_required()
def create_prescription():
    try:
        # Retrieve request data
        patient_id = request.json.get('patient_id')
        doc_id = request.json.get('doc_id')
        medications = request.json.get('medications')
        dosage = request.json.get('dosage')
        appointment_id = request.json.get('appointment_id')

        if not patient_id or not doc_id or not medications:
            return jsonify({"error": "patient_id, doc_id, and medications are required"}), 400
        
        # Validate patient and doctor existence
        patient = Patient.query.filter_by(id=patient_id).first()
        doctor = Doctor.query.filter_by(id=doc_id).first()
        appointment = Appointment.query.filter_by(id=appointment_id).first()

        if not patient:
            return jsonify({"error": "Patient not found"}), 404
        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404
        
        # Create new prescription entry
        new_prescription = Prescription(medications=medications, dosage=dosage)
        db.session.add(new_prescription)
        db.session.flush()  # To get new_prescription.id

        # Create the Prescription_Patient_Doctor entry
        prescription_patient_doctor = Prescription_Patient_Doctor(
            patient_id=patient_id,
            doc_id=doc_id,
            prescription_id=new_prescription.id,
            appointment_id=appointment_id
        )
        db.session.add(prescription_patient_doctor)
        db.session.commit()

        return jsonify({"message": "Prescription successfully created", "prescription_id": new_prescription.id}), 201

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# READ Operation (Get Prescription for a Patient)
@prescription_bp.route('/prescription/<string:patient_id>', methods=['GET'])
@jwt_required()
def get_prescriptions_by_patient(patient_id):
    try:
        # Validate patient existence
        patient = Patient.query.filter_by(id=patient_id).first()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Fetch all prescriptions for the given patient
        prescriptions = db.session.query(Prescription).join(
            Prescription_Patient_Doctor, Prescription.id == Prescription_Patient_Doctor.prescription_id
        ).filter(Prescription_Patient_Doctor.patient_id == patient_id).all()

        if not prescriptions:
            return jsonify({"message": "No prescriptions found for this patient"}), 404

        # Serialize the prescriptions to JSON
        prescription_list = [prescription.to_json() for prescription in prescriptions]

        return jsonify(prescription_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# READ Operation (Get Prescription for a Specific Appointment)
@prescription_bp.route('/prescription/appointment/<string:appointment_id>', methods=['GET'])
@jwt_required()
def get_prescription_by_appointment(appointment_id):
    try:
        # Fetch the prescription based on the appointment ID
        prescription = db.session.query(Prescription).join(
            Prescription_Patient_Doctor, Prescription.id == Prescription_Patient_Doctor.prescription_id
        ).filter(Prescription_Patient_Doctor.appointment_id == appointment_id).first()

        if not prescription:
            return jsonify({"message": "No prescription found for this appointment"}), 404

        return jsonify(prescription.to_json()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE Operation (Update a Prescription)
@prescription_bp.route('/prescription/<string:prescription_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_prescription(prescription_id):
    try:
        # Retrieve the prescription by ID
        prescription = Prescription.query.filter_by(id=prescription_id).first()
        if not prescription:
            return jsonify({"error": "Prescription not found"}), 404

        # Update fields if provided
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

# DELETE Operation (Delete a Prescription)
@prescription_bp.route('/prescription/<string:prescription_id>', methods=['DELETE'])
@jwt_required()
def delete_prescription(prescription_id):
    try:
        # Find the prescription and its association in Prescription_Patient_Doctor
        prescription = Prescription.query.filter_by(id=prescription_id).first()
        if not prescription:
            return jsonify({"error": "Prescription not found"}), 404

        # Remove the related Prescription_Patient_Doctor record
        Prescription_Patient_Doctor.query.filter_by(prescription_id=prescription_id).delete()
        db.session.delete(prescription)
        db.session.commit()

        return jsonify({"message": "Prescription deleted successfully"}), 200

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
