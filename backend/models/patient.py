# models/Doctor.py
from models.base_model import BaseModel
from models.dbConfig import db
from datetime import date

class Patient(BaseModel):
    __tablename__ = 'patients'
    __table_args__ = {'extend_existing': True}

    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = self.generate_custom_id(Patient,'P')

    def age(self):
        today = date.today()
        if self.birth_date:
            age = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
            return age
        return None

    def to_json():
        return {
            "name" : self.name,
            "birth_date": self.birth_date.strftime('%Y-%m-%d') if self.birth_date else None,
            "age" : self.age,
        }