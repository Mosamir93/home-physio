from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.availability import Availability
from ..models.physiotherapists import Physiotherapists
from .. import db


physio_bp = Blueprint('physio', __name__)

@physio_bp.route('/availability', methods=['POST'], strict_slashes=False)
@jwt_required()
def set_availabilty():
    try:
        user_info = get_jwt_identity()  # Fetch the JWT identity
        print(f"User Info: {user_info}")  # Debug print to check identity

        user_id = user_info['id']  # Adjust this based on the structure of your JWT token

        physiotherapist = Physiotherapists.query.get(user_id)
        if not physiotherapist:
            return jsonify({"message": "Only physiotherapists can set availability"}), 403

        date = request.form.get("date")
        time_slots = request.form.get("time_slots").split(",")
        
        for slot in time_slots:
            availability = Availability(
                physiotherapist_id=user_id,
                date=date,
                time_slot=slot.strip(),
                is_booked=False
            )
            db.session.add(availability)
        
        db.session.commit()

        return redirect(url_for('physio.dashboard'))
    except Exception as e:
        return jsonify({"message": str(e)}), 500  # Error handling

@physio_bp.route('/dashboard', methods=['GET'], strict_slashes=False)
@jwt_required()
def dashboard():
    user_info = get_jwt_identity()
    user_id = user_info['id']
    physiotherapist = Physiotherapists.query.get(user_id)
    availabilities = Availability.query.filter_by(physiotherapist_id=user_id).all()
    return render_template('physiotherapist/dashboard.html', physiotherapist=physiotherapist, availabilities=availabilities)
