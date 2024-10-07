from datetime import datetime, date
from flask_jwt_extended import jwt_required, get_jwt_identity

def str_to_date(birth_date):
    try:
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        return birth_date
    except ValueError:
        return jsonify({"error": "Invalid birth_date format. Use YYYY-MM-DD."}), 400

def has_required_role(required_roles):
    identity = get_jwt_identity()  # Get the identity from the JWT

    # Check if identity is a dictionary and has the expected keys
    if isinstance(identity, dict):
        user_id = identity.get("id")
        user_role = identity.get("role")

        # Validate that user_id and user_role exist
        if user_id is None or user_role is None:
            return False

        # Check if the user's role is in the required roles
        return user_role in required_roles
    
    return False  # Return False if identity is not a dictionary
