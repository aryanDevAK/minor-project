from models.dbConfig import db

class Patient_Mobile_Num(db.Model):
    __tablename__ = 'patientMobileNum'
    
    id = db.Column(db.String(10), db.ForeignKey("patients.id"), primary_key=True, nullable=False)
    mobile_num = db.Column(db.String(10), primary_key=True ,nullable=False)

class Patient_User(db.Model):
    __tablename__ = 'patientUser'
    
    mobile_num = db.Column(db.String(10), db.ForeignKey("patientMobileNum.mobile_num"), primary_key=True ,nullable=False)
    role = db.Column(db.String(50), default="patient")
