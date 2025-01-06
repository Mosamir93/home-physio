from flask import Blueprint, request, jsonify, session
from ..models.patient import Patient
from ..models.physiotherapists import Physiotherapists
from utils import generate_jwt, decode_jwt
from oauth import validate_google_token
from .. import db


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/signup', methods=['POST'], strictslashes=False)
def signup():
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

    token = generate_jwt(user.id)
    return jsonify({"token": token})


def login():
    google_token = request.json.get("google_token")
    google_data = validate_google_token(google_token)

    if not google_data:
        return jsonify({"message": "Invalid Google token"}), 400
    
    user = Patient.query.filter_by(
        email=google_data["email"]).first() or Physiotherapists.query.filter_by(
        email=google_data["email"]).first()
    
    if not user:
        return jsonify({"message": "User does not exist. Please sign up."}), 400
    
    token = generate_jwt(user.id)
    return jsonify({"token": token})
