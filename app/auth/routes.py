from flask import Blueprint, request, jsonify, session, render_template
from ..models.patient import Patient
from ..models.physiotherapists import Physiotherapists
from flask_bcrypt import Bcrypt
from .utils import generate_jwt, decode_jwt
from .oauth import validate_google_token
from .. import db


auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()


@auth_bp.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')

    use_oauth = request.json.get("use_oauth", False)
    role = request.json.get("role")
    email = request.json.get("email")
    phone = request.json.get("phone")
    password = request.json.get("password")

    if use_oauth:
        google_token = request.json.get("google_token")
        google_data = validate_google_token(google_token)

        if not google_data:
            return jsonify({"message": "Invalid Google token"}), 400

        email = google_data.get("email")
        user = Patient.query.filter_by(email=email).first() or Physiotherapists.query.filter_by(email=email).first()

        if user:
            return jsonify({"message": "User already exists. Log in instead."}), 400

        if role == "patient":
            user = Patient.from_google(google_data)
        elif role == "physiotherapist":
            user = Physiotherapists.from_google(google_data)

        user.phone = phone

    else:
        if not (email and password and phone):
            return jsonify({"message": "Email, password, and phone are required."}), 400

        user = Patient.query.filter_by(email=email).first() or Physiotherapists.query.filter_by(email=email).first()
        if user:
            return jsonify({"message": "User already exists. Log in instead."}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        if role == "patient":
            user = Patient(
                first_name=request.json.get("first_name"),
                last_name=request.json.get("last_name"),
                email=email,
                phone=phone,
                role="patient",
                google_id=None,
                password=hashed_password
            )
        elif role == "physiotherapist":
            user = Physiotherapists(
                first_name=request.json.get("first_name"),
                last_name=request.json.get("last_name"),
                email=email,
                phone=phone,
                role="physiotherapist",
                google_id=None,
                password=hashed_password
            )

    db.session.add(user)
    db.session.commit()

    token = generate_jwt(user.id, user.role)
    return jsonify({"token": token})


@auth_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    use_oauth = request.json.get("use_oauth", False)

    if use_oauth:
        google_token = request.json.get("google_token")
        google_data = validate_google_token(google_token)

        if not google_data:
            return jsonify({"message": "Invalid Google token"}), 400

        email = google_data.get("email")
        user = Patient.query.filter_by(email=email).first() or Physiotherapists.query.filter_by(email=email).first()

    else:
        email = request.json.get("email")
        password = request.json.get("password")

        if not (email and password):
            return jsonify({"message": "Email and password are required."}), 400

        user = Patient.query.filter_by(email=email).first() or Physiotherapists.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({"message": "Invalid email or password."}), 400

    if not user:
        return jsonify({"message": "User does not exist. Please sign up."}), 400

    token = generate_jwt(user.id, user.role)
    return jsonify({"token": token, "role": user.role})

@auth_bp.route('/logout', methods=['POST'], strict_slashes=False)
def logout():
    return jsonify({"message": "Logged out successfully"}), 200
