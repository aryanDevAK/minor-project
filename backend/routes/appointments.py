from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.dbConfig import db
from models.Appointment import Appointment, generate_custom_id
from models.Patient_Doc_Room_Appointment import Patient_Doc_Room_Appointment
from models.patient import Patient
from models.doctor import Doctor
from models.room import Room
import sqlalchemy.exc
from datetime import datetime

# Blueprint for appointment routes
appointment_bp = Blueprint('appointment_bp', __name__)

# CREATE Appointment (and associate with Patient, Doctor, Room)
@appointment_bp.route('/appointment', methods=['POST'])
@jwt_required()
def create_appointment():
    try:
        # Retrieve form data
        patient_id = request.json.get('patient_id')
        doc_id = request.json.get('doc_id')
        room_id = request.json.get('room_id')
        appointment_date = request.json.get('date')
        appointment_time = request.json.get('time')

        if not patient_id or not doc_id or not room_id or not appointment_date or not appointment_time:
            return jsonify({"error": "All fields (patient_id, doc_id, room_id, date, time) are required"}), 400

        # Parse the date and time strings
        try:
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(appointment_time, '%H:%M:%S').time()
        except ValueError:
            return jsonify({"error": "Invalid date or time format"}), 400

        # Check if patient, doctor, and room exist
        patient = Patient.query.filter_by(id=patient_id).first()
        doctor = Doctor.query.filter_by(id=doc_id).first()
        room = Room.query.filter_by(id=room_id).first()

        if not patient:
            return jsonify({"error": "Patient not found"}), 404
        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404
        if not room:
            return jsonify({"error": "Room not found"}), 404

        # Create new appointment
        new_appointment = Appointment(date=appointment_date, time=appointment_time)
        db.session.add(new_appointment)
        db.session.flush()  # Get new_appointment.id

        # Associate appointment with patient, doctor, and room
        patient_doc_room_appointment = Patient_Doc_Room_Appointment(
            patient_id=patient_id,
            doc_id=doc_id,
            room_id=room_id,
            appointment_id=new_appointment.id
        )
        db.session.add(patient_doc_room_appointment)
        db.session.commit()

        return jsonify({"message": "Appointment created successfully", "appointment_id": new_appointment.id}), 201

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# READ Appointment by patient ID (GET all appointments for a specific patient)
@appointment_bp.route('/appointments/<string:patient_id>', methods=['GET'])
@jwt_required()
def get_appointments_by_patient(patient_id):
    try:
        # Validate patient existence
        patient = Patient.query.filter_by(id=patient_id).first()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Fetch all appointments for the patient
        appointments = db.session.query(Appointment).join(
            Patient_Doc_Room_Appointment, Appointment.id == Patient_Doc_Room_Appointment.appointment_id
        ).filter(Patient_Doc_Room_Appointment.patient_id == patient_id).all()

        if not appointments:
            return jsonify({"message": "No appointments found for this patient"}), 404

        # Serialize appointments
        appointment_list = [{
            "appointment_id": appointment.id,
            "date": appointment.date.strftime('%Y-%m-%d'),
            "time": appointment.time.strftime('%H:%M:%S')
        } for appointment in appointments]

        return jsonify(appointment_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE Appointment (Update date and/or time)
@appointment_bp.route('/appointment/<string:appointment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_appointment(appointment_id):
    try:
        # Fetch the appointment by ID
        appointment = Appointment.query.filter_by(id=appointment_id).first()
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        # Update date and time if provided
        appointment_date = request.json.get('date')
        appointment_time = request.json.get('time')

        if appointment_date:
            try:
                appointment.date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid date format"}), 400

        if appointment_time:
            try:
                appointment.time = datetime.strptime(appointment_time, '%H:%M:%S').time()
            except ValueError:
                return jsonify({"error": "Invalid time format"}), 400

        db.session.commit()

        return jsonify({"message": "Appointment updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# DELETE Appointment (Delete by appointment ID)
@appointment_bp.route('/appointment/<string:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    try:
        # Fetch the appointment by ID
        appointment = Appointment.query.filter_by(id=appointment_id).first()
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        # Delete the appointment from the database
        db.session.delete(appointment)
        db.session.commit()

        return jsonify({"message": "Appointment deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# READ Appointment by doctor ID (GET all appointments for a specific doctor)
@appointment_bp.route('/appointments/doctor/<string:doctor_id>', methods=['GET'])
@jwt_required()
def get_appointments_by_doctor(doctor_id):
    try:
        # Validate doctor existence
        doctor = Doctor.query.filter_by(id=doctor_id).first()
        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

        # Fetch all appointments for the doctor
        appointments = db.session.query(Appointment).join(
            Patient_Doc_Room_Appointment, Appointment.id == Patient_Doc_Room_Appointment.appointment_id
        ).filter(Patient_Doc_Room_Appointment.doc_id == doctor_id).all()

        if not appointments:
            return jsonify({"message": "No appointments found for this doctor"}), 404

        # Serialize appointments
        appointment_list = [{
            "appointment_id": appointment.id,
            "patient_id": patient_doc_room.patient_id,
            "date": appointment.date.strftime('%Y-%m-%d'),
            "time": appointment.time.strftime('%H:%M:%S')
        } for appointment in appointments for patient_doc_room in Patient_Doc_Room_Appointment.query.filter_by(appointment_id=appointment.id).all()]

        return jsonify(appointment_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
