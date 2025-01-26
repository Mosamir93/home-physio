from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.availability import Availability
from ..models.physiotherapists import Physiotherapists
from .. import db


physio_bp = Blueprint('physio', __name__)

@physio_bp.route('/availability', methods=['POST'], strict_slashes=False)
@jwt_required()
def set_availabilty():
    user_id = get_jwt_identity()
    physiotherapist = Physiotherapists.query.get(user_id)

    if not physiotherapist:
        return jsonify({"message": "Only physiotherapists can set availability"}), 403
    
    slots = request.json.get("time_slots")
    date = request.json.get("date")
    
    for slot in slots:
        availability = Availability(
            physiotherapist_id=user_id,
            date=date,
            time_slot=slot,
            is_booked=False
        )
        db.session.add(availability)
    db.session.commit()

    return jsonify({"message": "Availability set successfully"})
