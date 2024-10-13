from models.dbConfig import db

class Patient_Test_Report(db.Model):
    __tablename__ = 'patient_test_report'

    patient_id = db.Column(db.String(10),db.ForeignKey('patients.id'), nullable=False)
    lab_id = db.Column(db.String(10), db.ForeignKey('labs.id'), nullable=False)
    report_id = db.Column(db.String(10), db.ForeignKey('lab_report.id'),primary_key=True, nullable=False)

    def to_json(self):
        return {"message":"Successfully uploaded the test report"}