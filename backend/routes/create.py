from flask import Blueprint, request, jsonify, abort
from models import db, Record, Patient_Record

create_record = Blueprint("create_record", __name__)

@create_record.route("/<nurse_id>/create/record", methods=["POST"])
def create_record_for_patient(nurse_id):
    data = request.get_json()
    patient_id = data.get("patient_id")
    body_temp = data.get("body_temp", "Not Checked")
    blood_pressure = data.get("blood_pressure", "Not Checked")
    spo = data.get("spo", "Not Checked")

    if not patient_id:
        abort(400, description="Patient ID is required.")
 
    new_record = Record(
        id=new_record_id,
        body_temp=body_temp,
        blood_pressure=blood_pressure,
        spo=spo
    )
    
    db.session.add(new_record)
    
    patient_record = Patient_Record(
        patient_id=patient_id,
        record_id=new_record_id,
        nurse_id=nurse_id
    )
    db.session.add(patient_record)
    
    db.session.commit()
    
    return jsonify(new_record.to_json()), 201

def generate_custom_id(model_class, prefix):
    last_entry = model_class.query.filter(model_class.id.like(f"{prefix}%")).order_by(model_class.id.desc()).first()
    
    if last_entry:
        last_id_number = int(last_entry.id[len(prefix):])
        new_id_number = last_id_number + 1
    else:
        new_id_number = 101
    
    return f"{prefix}{new_id_number:03d}"
