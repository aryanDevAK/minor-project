from models.dbConfig import db

class Lab_Dept(db.Model):
    __tablename__ = "lab_dept"

    lab_id = db.Column(db.String(20), db.ForeignKey('labs.id'), primary_key=True)
    dept_id = db.Column(db.String(20), db.ForeignKey('departments.id'))

    def to_json():
        return {
            "lab_id": self.lab_id,
            "dept_id": self.dept_id
        }