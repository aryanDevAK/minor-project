from models.dbConfig import db

class Patient_Doc_Room_Appointment(db.Model):
    __tablename__ = 'prescription_patient_doctor'

    patient_id = db.Column(db.String(10),db.ForeignKey('patients.id'), primary_key=True, nullable=False)
    doc_id = db.Column(db.String(10), db.ForeignKey('doctors.id'), primary_key=True, nullable=False)
    room_id = db.Column(db.String(10), db.ForeignKey('room.id'), nullable=False)
    appointment_id = db.Column(db.String(10), db.ForeignKey("appointments.id"))

    def to_json(self):
        return {"message":"Successfully created Appointment"}