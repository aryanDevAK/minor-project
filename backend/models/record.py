# models/Records.py
from models.dbConfig import db
from datetime import date

def generate_custom_id(model_class, prefix):
    last_entry = model_class.query.filter(model_class.id.like(f"{prefix}%")).order_by(model_class.id.desc()).first()
    
    if last_entry:
        last_id_number = int(last_entry.id[3:])
        new_id_number = last_id_number + 1
    else:
        new_id_number = 101
    
    return f"{prefix}{new_id_number}"

class Record(db.Model):
    __tablename__ = 'records'
    
    id = db.Column(db.String(10), primary_key=True)
    body_temp = db.Column(db.String(10), nullable=True, default="Not Checked")
    blood_pressure = db.Column(db.String(10), nullable = True, default="Not Checked")
    spo = db.Column(db.String(10), nullable=True, default="Not Checked")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = generate_custom_id(Record, 'REC')

    def to_json():
        return {
            'id': self.id,
            "body_temp" : self.body_temp,
            "blood_pressure": self.blood_pressure,
            "spo": self.spo
        }