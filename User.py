from config import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(128), primary_key=True)
    password = db.Column(db.String(255), nullable=False)  # Increased length for hashed passwords
    role = db.Column(db.String(50), nullable=False)  # e.g., 'doctor', 'nurse', 'staff', 'patient'

    ROLES = ['doctor', 'nurse', 'staff', 'patient']

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role not in self.ROLES:
            raise ValueError("Invalid role")

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_json(self):
        """Serialize the User instance to JSON format."""
        return {
            "id": self.id,
            "role": self.role
        }