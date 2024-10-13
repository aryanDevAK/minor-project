from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.dbConfig import db
from models.room import Room
import sqlalchemy.exc
from routes.helper_function import str_to_date, has_required_role

room_bp = Blueprint("register_room", __name__)

@room_bp.route("/register/room", methods=["POST"])
@jwt_required()
def register_room():
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 403

    try:
        room_type = request.json.get("room_type")
        total_capacity = request.json.get("total_capacity")
        price = request.json.get("price")

        if not room_type or not total_capacity or not price:
            return jsonify({"error": "All fields are required"}), 400

        new_room = Room(room_type=room_type, total_capacity=total_capacity, price=price)
        db.session.add(new_room)
        db.session.commit()

        return jsonify({"message":"Registered Succefully"}), 201

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error occurred"}), 500

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@room_bp.route("/rooms", methods=["GET"])
@jwt_required()
def get_rooms():
    try:
        rooms = Room.query.all()
        appointment_list = [{
            "room_id": room.id,
            "room_type": room.room_type,
            "total_capacity": room.total_capacity,
            "occupied_capacity": room.occupied_capacity,
            "price": room.price
        } for room in rooms]
        return jsonify(appointment_list), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@room_bp.route("/room/<string:room_id>", methods=["PUT","PATCH"])
@jwt_required()
def update_room(room_id):
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 403

    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    try:
        room_type = request.json.get("room_type")
        total_capacity = request.json.get("total_capacity")
        occupied_capacity = request.json.get("occupied_capacity")
        price = request.json.get("price")

        if room_type:
            room.room_type = room_type
        if total_capacity:
            room.total_capacity = total_capacity
        if occupied_capacity:
            room.occupied_capacity = occupied_capacity
        if price:
            room.price = price

        db.session.commit()

        return jsonify({"message":"Updated Succefully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

@room_bp.route("/room/<string:room_id>", methods=["DELETE"])
@jwt_required()
def delete_room(room_id):
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 403

    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    try:
        db.session.delete(room)
        db.session.commit()
        return jsonify({"message": "Room deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
