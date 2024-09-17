# models/base_model.py
from sqlalchemy import Column, Integer, String
from models.dbConfig import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.String(20), primary_key=True, unique=True)
    
    @staticmethod
    def generate_custom_id(model_class, prefix):
        last_entry = model_class.query.filter(model_class.id.like(f"{prefix}%")).order_by(model_class.id.desc()).first()

        if last_entry:
            last_id_number = int(last_entry.id[1:])
            new_id_number = last_id_number + 1
        else:
            new_id_number = 10001

        return f"{prefix}{new_id_number}"