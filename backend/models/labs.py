# models/Lab.py
from models.dbConfig import db

def generate_custom_id(model_class, prefix):
    last_entry = model_class.query.filter(model_class.id.like(f"{prefix}%")).order_by(model_class.id.desc()).first()
    
    if last_entry:
        last_id_number = int(last_entry.id[3:])
        new_id_number = last_id_number + 1
    else:
        new_id_number = 101
    
    return f"{prefix}{new_id_number}"

class Lab(db.Model):
    __tablename__ = 'labs'
    
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_num = db.Column(db.String(10), primary_key=True, nullable = False, unique=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = generate_custom_id(Lab, 'LAB')

    def to_json():
        return {
            "name" : self.name,
            "license-number": self.license_num
        }