from models.dbConfig import db

class Patient_Record(db.Model):
    __tablename__ = 'patientrecord'
    
    patient_id = db.Column(db.String(10), db.ForeignKey("patients.id"), primary_key=True ,nullable=False)
    record_id = db.Column(db.String(10), db.ForeignKey("record.id"), nullable=False)
    nurse_id = db.Column(db.String(10), db.ForeignKey("nurse.id"), nullable=False)