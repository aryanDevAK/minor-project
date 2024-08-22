# models/Doctor.py
from models.base_model import BaseModel
from models.dbConfig import db
from sqlalchemy.orm import relationship

class Doctor(BaseModel):
    __tablename__ = 'doctors'
    
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    speciality = db.Column(db.String(100), nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = self.generate_custom_id(Doctor,'D')

    def to_json():
        return {
            "name" : self.name,
            "age" : self.age,
            "speciality" : self.speciality
        }