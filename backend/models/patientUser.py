from models.dbConfig import db

class Patient_User(db.Model):
    __tablename__ = 'patientUser'
    
    mobile_num = db.Column(db.String(10), db.ForeignKey("patientMobileNum.mobile_num"), primary_key=True ,nullable=False)
    role = db.Column(db.String(50), default="patient")