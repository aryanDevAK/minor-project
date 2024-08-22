# models/base_model.py
from sqlalchemy import Column, Integer, String
from models.dbConfig import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.String(20), primary_key=True, unique=True)
    
    @staticmethod
    def generate_custom_id(model_class, prefix):
        # Query the specific model class for the last entry with this prefix
        last_entry = model_class.query.filter(model_class.id.like(f"{prefix}%")).order_by(model_class.id.desc()).first()

        if last_entry:
            # Extract the numeric part of the ID, increment it
            last_id_number = int(last_entry.id[1:])  # Remove the prefix ('D' or 'P') and get the number
            new_id_number = last_id_number + 1
        else:
            # Start with 10001 if no entry exists
            new_id_number = 10001

        # Return the new ID with the prefix
        return f"{prefix}{new_id_number}"

