from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.booking import Booking
from ..models.availability import Availability
from ..models.patient import Patient
from .. import db

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/book', methods=['POST'], strict_slashes=False)
@jwt_required()
def book_appointment():
    user_id = get_jwt_identity()
    patient = Patient.query.get(user_id)

    if not patient:
        return jsonify({"message": "Only patients can book appointments"}), 403

    physiotherapist_id = request.json.get("physiotherapist_id")
    date = request.json.get("date")
    time_slot = request.json.get("time_slot")

    availability = Availability.query.filter_by(
        physiotherapist_id=physiotherapist_id,
        date=date,
        time_slot=time_slot,
        is_booked=False
    ).first()

    if not availability:
        return jsonify({"message": "Time slot not available"}), 400

    booking = Booking(
        patient_id=user_id,
        physiotherapist_id=physiotherapist_id,
        date=date,
        time_slot=time_slot
    )
    db.session.add(booking)

    availability.is_booked = True
    db.session.commit()

    return jsonify({"message": "Appointment booked successfully"})

@patient_bp.route('/dashboard', methods=['GET'], strict_slashes=False)
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    bookings = Booking.query.filter_by(patient_id=user_id).all()
    return jsonify({"bookings": [b.to_dict() for b in bookings]})
