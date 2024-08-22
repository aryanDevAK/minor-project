# models/Doctor.py
from models.base_model import BaseModel
from models.dbConfig import db

class Doctor(BaseModel):
    __tablename__ = 'doctors'
    
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = self.generate_custom_id(Doctor,'D')

    def to_json():
        return {
            "name" : self.name,
            "email" : self.email,
            "password" : self.password
        }