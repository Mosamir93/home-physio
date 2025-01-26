from flask import Blueprint, request, jsonify, session, render_template
from ..models.patient import Patient
from ..models.physiotherapists import Physiotherapists
from .utils import generate_jwt, decode_jwt
from .oauth import validate_google_token
from .. import db


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    google_token = request.json.get("google_token")
    google_data = validate_google_token(google_token)

    if not google_data:
        return jsonify({"message": "Invalid Google token"}), 400
    
    user = Patient.query.filter_by(
        email=google_data["email"]).first() or Physiotherapists.query.filter_by(
        email=google_data["email"]).first()
    
    if user:
        return jsonify({"message": "User already exists. Log in instead."}), 400
    
    role = request.json.get("role")
    if role == "patient":
        user = Patient.from_google(google_data)
    elif role == "physiotherapist":
        user = Physiotherapists.from_google(google_data)

    user.phone = request.json.get("phone")
    db.session.add(user)
    db.session.commit()

    token = generate_jwt(user.id, role)
    return jsonify({"token": token})


@auth_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    google_token = request.json.get("google_token")
    google_data = validate_google_token(google_token)

    if not google_data:
        return jsonify({"message": "Invalid Google token"}), 400
    
    user = Patient.query.filter_by(
        email=google_data["email"]).first() or Physiotherapists.query.filter_by(
        email=google_data["email"]).first()
    
    if not user:
        return jsonify({"message": "User does not exist. Please sign up."}), 400
    
    token = generate_jwt(user.id, user.role)
    return jsonify({"token": token})


@auth_bp.route('/logout', methods=['POST'], strict_slashes=False)  # ### ADDITION ###
def logout():
    # Add server-side session or token blacklisting if needed.
    return jsonify({"message": "Logged out successfully"}), 200
