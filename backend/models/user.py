from uuid import uuid4
from models.dbConfig import db

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(128), primary_key=True, unique=True, default=get_uuid)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "role": self.role
        }