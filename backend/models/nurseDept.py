from models.dbConfig import db

class Nurse_Dept(db.Model):
    __tablename__ = "nurse_dept"

    nurse_id = db.Column(db.String(20), db.ForeignKey('nurses.id'), primary_key=True)
    dept_id = db.Column(db.String(20), db.ForeignKey('departments.id'))

    def to_json():
        return {
            "nurse_id": self.nurse_id,
            "dept_id": self.dept_id
        }