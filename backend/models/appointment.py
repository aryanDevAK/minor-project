# models/Prescription.py
from models.dbConfig import db

def generate_custom_id(model_class, prefix):
    last_entry = model_class.query.filter(model_class.id.like(f"{prefix}%")).order_by(model_class.id.desc()).first()
    
    if last_entry:
        last_id_number = int(last_entry.id[2:])
        new_id_number = last_id_number + 1
    else:
        new_id_number = 101
    
    return f"{prefix}{new_id_number}"

class Appointment(db.Model):
    __tablename__ = 'appointments'  
    
    id = db.Column(db.String(10), primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        if not self.id:
            self.id = generate_custom_id(Appointment, 'AP')

    def to_json():
        return {
            "id" : self.id,
            "date": self.date,
            "time": self.time
        }