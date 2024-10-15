from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.dbConfig import db
from models.patient import Patient
from models.patient_mobile_num import Patient_Mobile_Num, Patient_User
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy.exc
from datetime import datetime, date
from routes.helper_function import  has_required_role

patient_routes_bp = Blueprint("register_patient", __name__)
@patient_routes_bp.route("/register/patient", methods=["POST"])
@jwt_required()
def register_patient():
    if not has_required_role(["doctor", "nurse", "admin"]):
        return jsonify({"message" : "You do not have permission to do that"}), 403

    try:
        name = request.json.get("name")
        birth_date = request.json.get("birth-date")
        mobile_num = request.json.get("mobile-num")

        if not name or not birth_date or not mobile_num:
            return jsonify({"error": "All fields are required"}), 400
        
        patient_exists = Patient_User.query.filter_by(mobile_num=mobile_num).first() is not None
        if patient_exists:
            return jsonify({"error": "Mobile Number exists. You can directly login"}), 409

        try:
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

        new_patient = Patient(name=name, birth_date=birth_date)
        db.session.add(new_patient)

        new_patient_num = Patient_Mobile_Num(id=new_patient.id, mobile_num=mobile_num)
        db.session.add(new_patient_num)
        
        new_patient_user = Patient_User(mobile_num=mobile_num)
        db.session.add(new_patient_user)
        db.session.commit()

        return jsonify({"message": "Successfully Registered"}), 201
    
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@patient_routes_bp.route("/get/patients", methods=["GET"])
@jwt_required()
def get_patients():
    try:
        patients = db.session.query(
            Patient.id,
            Patient.name,
            Patient.birth_date,
            Patient_Mobile_Num.mobile_num
        ).join(Patient_Mobile_Num, Patient.id == Patient_Mobile_Num.id).all()

        patient_list = [{
            "id": patient.id,
            "name": patient.name,
            "birth_date":patient.birth_date.strftime('%Y-%m-%d'),
            "mobile_num": patient.mobile_num
        } for patient in patients]

        return jsonify(patient_list), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@patient_routes_bp.route("/get/patient/<string:identifier>", methods=["GET"])
@jwt_required()
def get_patient(identifier):
    try:
        # Try to fetch patient by ID first, if not found, fetch by mobile number
        patient = db.session.query(
            Patient.id,
            Patient.name,
            Patient.birth_date,
            Patient_Mobile_Num.mobile_num
        ).join(Patient_Mobile_Num, Patient.id == Patient_Mobile_Num.id) \
         .filter((Patient.id == identifier) | (Patient_Mobile_Num.mobile_num == identifier)).first()

        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        patient_info = {
            "id": patient.id,
            "name": patient.name,
            "birth_date":patient.birth_date.strftime('%Y-%m-%d'),
            "mobile_num": patient.mobile_num
        }

        return jsonify(patient_info), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@patient_routes_bp.route("/update/patient/<string:identifier>", methods=["PUT", "PATCH"])
@jwt_required()
def update_patient(identifier):
    if not has_required_role(["doctor", "nurse", "admin"]):
        return jsonify({"message" : "You do not have permission to do that"}), 403

    try:
        patient = Patient.query.join(Patient_Mobile_Num, Patient.id == Patient_Mobile_Num.id) \
            .filter((Patient.id == identifier) | (Patient_Mobile_Num.mobile_num == identifier)).first()

        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        name = request.json.get("name")
        mobile_num = request.json.get("mobile-num")

        if name:
            patient.name = name
        if mobile_num:
            patient_num = Patient_Mobile_Num.query.filter_by(id=patient.id).first()
            if patient_num:
                patient_num.mobile_num = mobile_num
            else:
                return jsonify({"error": "Mobile number not found"}), 404

        db.session.commit()

        return jsonify({"message": "Patient details updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@patient_routes_bp.route("/delete/patient/<string:identifier>", methods=["DELETE"])
@jwt_required()
def delete_patient(identifier):
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 403

    try:
        patient = Patient.query.filter_by(id=identifier).first()
        
        if patient:
            patient_num = Patient_Mobile_Num.query.filter_by(id=patient.id).first()

            if patient_num:
                Patient_Mobile_Num.query.filter_by(id=patient.id).delete() 
                Patient_User.query.filter_by(mobile_num=patient_num.mobile_num).delete()
            
            db.session.delete(patient)  
            db.session.commit()

            return jsonify({"message": "Patient deleted successfully"}), 200

        else:
            patient_num = Patient_Mobile_Num.query.filter_by(mobile_num=identifier).first()
            if not patient_num:
                return jsonify({"error": "Patient with the provided identifier not found"}), 404
            
            patient = Patient.query.filter_by(id=patient_num.id).first()

            if patient:
                Patient_Mobile_Num.query.filter_by(id=patient.id).delete()  # Delete from Patient_Mobile_Num
                Patient_User.query.filter_by(mobile_num=patient_num.mobile_num).delete()  # Delete from Patient_User
            
                db.session.delete(patient)  
                db.session.commit()

                return jsonify({"message": "Patient deleted successfully"}), 200

            return jsonify({"error": "Patient not found"}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

