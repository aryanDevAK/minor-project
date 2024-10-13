from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.dbConfig import db
from models.appointment import Appointment, generate_custom_id
from models.patient_doctor_room_appointment import Patient_Doc_Room_Appointment
from models.patient import Patient
from models.doctor import Doctor
from models.room import Room
import sqlalchemy.exc
from datetime import datetime
from routes.helper_function import str_to_date, has_required_role

appointment_bp = Blueprint('appointment_bp', __name__)
@appointment_bp.route('/appointment', methods=['POST'])
@jwt_required()
def create_appointment():
    if not has_required_role(["admin", "receptionist", "doctor"]):
        return jsonify({"message": "You do not have permission to do that"}), 401
    
    try:
        patient_id = request.json.get('patient_id')
        doc_id = request.json.get('doc_id')
        room_id = request.json.get('room_id')
        appointment_date = request.json.get('date')
        appointment_time = request.json.get('time')

        # Validate input fields
        if not all([patient_id, doc_id, room_id, appointment_date, appointment_time]):
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
            return jsonify({"error": "Room is full"}), 404
        if room.occupied_capacity >= room.total_capacity:
            return jsonify({"error": "Room is full"}), 400
        
        existing_appointment = db.session.query(Appointment).join(
            Patient_Doc_Room_Appointment,
            Appointment.id == Patient_Doc_Room_Appointment.appointment_id
        ).filter(
            Patient_Doc_Room_Appointment.patient_id == patient_id,
            Appointment.date == appointment_date
        ).first()

        if existing_appointment:
            return jsonify({"error": "An appointment for this patient already exists for today."}), 400

        new_appointment = Appointment(date=appointment_date, time=appointment_time)
        db.session.add(new_appointment)
        db.session.flush()

        patient_doc_room_appointment = Patient_Doc_Room_Appointment(
            patient_id=patient_id,
            doc_id=doc_id,
            room_id=room_id,
            appointment_id=new_appointment.id
        )
        db.session.add(patient_doc_room_appointment)
        room.occupied_capacity += 1
        db.session.commit()

        return jsonify({"message": "Appointment created"}), 201

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
        
@appointment_bp.route('/appointments/<string:patient_id>', methods=['GET'])
@jwt_required()
def get_appointments_by_patient(patient_id):
    try:
        patient = Patient.query.filter_by(id=patient_id).first()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        appointments = db.session.query(
            Appointment.id,
            Appointment.date,
            Appointment.time,
            Patient_Doc_Room_Appointment.room_id,
            Room.room_type,
            Doctor.name.label("doc_name"),
        ).join(Appointment, Appointment.id == Patient_Doc_Room_Appointment.appointment_id) \
         .join(Room, Patient_Doc_Room_Appointment.room_id == Room.id) \
         .join(Doctor, Patient_Doc_Room_Appointment.doc_id == Doctor.id) \
         .filter(Patient_Doc_Room_Appointment.patient_id == patient.id) \
         .all()

        if not appointments:
            return jsonify({"message": "No appointments found for this patient"}), 404

        appointment_list = [{
            "appointment_id": appointment.id,
            "date": appointment.date.strftime('%Y-%m-%d'),
            "time": appointment.time.strftime('%H:%M:%S'),
            "room_number": appointment.room_id,
            "room_type" : appointment.room_type,
            "doctor_name": appointment.doc_name
        } for appointment in appointments]

        return jsonify(appointment_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appointment_bp.route('/appointment/<string:appointment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_appointment(appointment_id):
    try:
        appointment = Appointment.query.filter_by(id=appointment_id).first()
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        appointment_data = Patient_Doc_Room_Appointment.query.filter_by(appointment_id=appointment_id).first()
        if not appointment_data:
            return jsonify({"error": "Appointment data not found"}), 404

        appointment_date = request.json.get('date')
        appointment_time = request.json.get('time')
        room_id = request.json.get('room_id')  
        doc_id = request.json.get('doc_id')

        if appointment_date:
            try:
                appointment.date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        if appointment_time:
            try:
                appointment.time = datetime.strptime(appointment_time, '%H:%M:%S').time()
            except ValueError:
                return jsonify({"error": "Invalid time format. Use HH:MM:SS."}), 400

        if room_id:
            room_info = Room.query.filter_by(id=room_id).first()
            if room_info:
                if room_info.occupied_capacity >= room_info.total_capacity:
                    return jsonify({"error": "Selected room is full."}), 400
                old_room_id = appointment_data.room_id
                old_room = Room.query.filter_by(id=old_room_id).first()
                if old_room:
                    old_room.occupied_capacity -= 1
                appointment_data.room_id = room_id
                room_info.occupied_capacity += 1

            else:
                return jsonify({"error": "Room not found."}), 404

        if doc_id:
            doctor_info = Doctor.query.filter_by(id=doc_id).first()
            if doctor_info:
                appointment_data.doc_id = doc_id
            else:
                return jsonify({"error": "Doctor not found."}), 404

        db.session.commit()

        return jsonify({"message": "Appointment updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appointment_bp.route('/appointment/<string:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 401
    
    try:
        appointment = Appointment.query.filter_by(id=appointment_id).first()
        
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        appointment_rel = Patient_Doc_Room_Appointment.query.filter_by(appointment_id=appointment_id).first()
        if appointment_rel:
            room_info = Room.query.filter_by(id=appointment_rel.room_id).first()
            room_info.occupied_capacity -= 1
            db.session.delete(appointment_rel)

        # Delete the appointment
        db.session.delete(appointment)
        db.session.commit()

        return jsonify({"message": "Appointment deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@appointment_bp.route('/appointments/doctor/<string:doctor_id>', methods=['GET'])
@jwt_required()
def get_appointments_by_doctor(doctor_id):
    try:
        doctor = Doctor.query.filter_by(id=doctor_id).first()
        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

        appointments = db.session.query(
            Appointment.id,
            Appointment.date,
            Appointment.time,
            Patient_Doc_Room_Appointment.room_id,
            Patient.name.label("patient_name"),
        ).join(Appointment, Appointment.id == Patient_Doc_Room_Appointment.appointment_id) \
         .join(Room, Patient_Doc_Room_Appointment.room_id == Room.id) \
         .join(Patient, Patient_Doc_Room_Appointment.patient_id == Patient.id) \
         .filter(Patient_Doc_Room_Appointment.doc_id == doctor.id) \
         .all()

        if not appointments:
            return jsonify({"message": "No appointments found for this doctor"}), 404

        appointment_list = [{
            "appointment_id": appointment.id,
            "date": appointment.date.strftime('%Y-%m-%d'),
            "time": appointment.time.strftime('%H:%M:%S'),
            "room_number": appointment.room_id,
            "patient_name": appointment.patient_name
        } for appointment in appointments]

        return jsonify(appointment_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
