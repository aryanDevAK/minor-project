from models.dbConfig import db

class Patient_Doc_Room_Appointment(db.Model):
    __tablename__ = 'appointment_doc_room_patient'

    patient_id = db.Column(db.String(10),db.ForeignKey('patients.id'),nullable=False,unique=False)
    doc_id = db.Column(db.String(10), db.ForeignKey('doctors.id'), nullable=False,unique=False)
    room_id = db.Column(db.String(10), db.ForeignKey('room.id'), nullable=False,unique=False)
    appointment_id = db.Column(db.String(10), db.ForeignKey("appointments.id"),primary_key=True)

    def to_json(self):
        return {"message":"Successfully created Appointment"}