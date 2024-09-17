# models/Room.py
from models.dbConfig import db
from sqlalchemy.orm import relationship

def generate_custom_id(model_class, prefix):
    last_entry = model_class.query.filter(model_class.id.like(f"{prefix}%")).order_by(model_class.id.desc()).first()
    
    if last_entry:
        last_id_number = int(last_entry.id[1:])
        new_id_number = last_id_number + 1
    else:
        new_id_number = 101
    
    return f"{prefix}{new_id_number}"

class Room(db.Model):
    __tablename__ = 'room'
    
    id = db.Column(db.String(10), primary_key=True)
    room_type = db.Column(db.String(100), nullable=False)
    total_capacity = db.Column(db.Integer, nullable=False)
    occupied_capacity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.String(10), nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = generate_custom_id(Room, 'R')

    @property
    def available_capacity(self):
        return self.total_capacity - self.occupied_capacity
    
    def assign_room(self, number_of_occupants=1):
        if self.occupied_capacity + number_of_occupants > self.total_capacity:
            raise ValueError(f"Cannot assign room. Only {self.available_capacity} spaces are available.")
        self.occupied_capacity += number_of_occupants
        db.session.commit()

    def release_room(self, number_of_occupants=1):
        if self.occupied_capacity - number_of_occupants < 0:
            raise ValueError("Occupied capacity cannot be less than zero.")
        self.occupied_capacity -= number_of_occupants
        db.session.commit()

    def to_json():
        return {
            "id": self.id,
            "room_type": self.room_type,
            "total_capacity": self.total_capacity,
            "occupied_capacity": self.occupied_capacity,
            "available_capacity": self.available_capacity,
            "price": self.price
        }