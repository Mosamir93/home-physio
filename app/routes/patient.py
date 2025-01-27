from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.booking import Booking
from ..models.availability import Availability
from ..models.patient import Patient
from ..models.physiotherapists import Physiotherapists
from .. import db

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/book', methods=['POST'], strict_slashes=False)
@jwt_required()
def book_appointment():
    user_id = get_jwt_identity()
    patient = Patient.query.get(user_id)

    if not patient:
        return jsonify({"message": "Only patients can book appointments"}), 403

    physiotherapist_id = request.form.get("physiotherapist_id")
    date = request.form.get("date")
    time_slot = request.form.get("time_slot")

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

    return redirect(url_for('patient.dashboard'))

@patient_bp.route('/dashboard', methods=['GET'], strict_slashes=False)
@jwt_required()
def dashboard():
    user_info = get_jwt_identity()
    user_id = user_info['id']
    bookings = Booking.query.filter_by(patient_id=user_id).all()

    location = request.args.get('location')
    date = request.args.get('date')
    
    physiotherapists = []
    if location and date:
        physiotherapists = Physiotherapists.query.filter_by(city=location).all()

        for physiotherapist in physiotherapists:
            physiotherapist.available_slots = Availability.query.filter_by(
                physiotherapist_id=physiotherapist.id, date=date, is_booked=False
            ).all()

    return render_template('patient/dashboard.html', bookings=bookings, physiotherapists=physiotherapists)
