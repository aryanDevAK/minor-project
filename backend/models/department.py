from models.dbConfig import db
from sqlalchemy.orm import relationship

def generate_custom_id(model_class, prefix):
    last_entry = model_class.query.filter(model_class.id.like(f"{prefix}%")).order_by(model_class.id.desc()).first()
    
    if last_entry:
        last_id_number = int(last_entry.id[4:])
        new_id_number = last_id_number + 1
    else:
        new_id_number = 101
    
    return f"{prefix}{new_id_number}"

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = generate_custom_id(Department, 'DEPT')
    
    def to_json(self):
        return {
            'dept_id': self.id,
            'name': self.name
        }