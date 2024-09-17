from models.dbConfig import db
from datetime import date

def generate_custom_id(model_class, prefix):
    last_entry = model_class.query.filter(model_class.id.like(f"{prefix}%")).order_by(model_class.id.desc()).first()
    
    if last_entry:
        last_id_number = int(last_entry.id[2:])
        new_id_number = last_id_number + 1
    else:
        new_id_number = 101
    
    return f"{prefix}{new_id_number}"

class Lab_Report(db.Model):
    __tablename__ = 'lab_report'
    
    id = db.Column(db.String(10), primary_key=True)
    test_report = db.Column(db.LargeBinary, nullable=False)  #LargeBinary for storing the PDF data
    test_name = db.Column(db.String(50), nullable=False)
    test_date = db.Column(db.Date, nullable=False, default=date.today)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = generate_custom_id(Lab_Report, 'RP')

    def to_json(self):
        return {
            "id": self.id,
            "test_name": self.test_name,
            "test_date": self.test_date.strftime('%Y-%m-%d'),
        }