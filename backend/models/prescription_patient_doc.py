from models.dbConfig import db

class Prescription_Patient_Doctor(db.Model):
    __tablename__ = 'prescrition_patient_doctor_2'

    patient_id = db.Column(db.String(10),db.ForeignKey('patients.id'), nullable=False)
    doc_id = db.Column(db.String(10), db.ForeignKey('doctors.id'),  nullable=False)
    prescription_id = db.Column(db.String(10), db.ForeignKey('prescriptions.id'),primary_key=True, nullable=False)
    appointment_id = db.Column(db.String(10), db.ForeignKey("appointments.id"),nullable=False)