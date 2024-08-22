from models.dbConfig import db


class Doc_Dept(db.Model):
    __tablename__ = "doc_dept"

    doc_id = db.Column(db.String(20), db.ForeignKey('doctors.id'), primary_key=True)
    dept_id = db.Column(db.String(20), db.ForeignKey('departments.id'))

    def to_json():
        return {
            "doc_id": self.doc_id,
            "dept_id": self.dept_id
        }