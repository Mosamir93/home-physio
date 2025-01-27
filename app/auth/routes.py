from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from ..models.patient import Patient
from .utils import get_dashboard_redirect, set_jwt_cookies
from ..models.physiotherapists import Physiotherapists
from .. import db

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()


@auth_bp.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')

    data = request.form
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')
    city = data.get('city')
    password = data.get('password')
    role = request.form.get("role")

    if not (email and password and phone):
        return render_template('auth/signup.html', error="All fields are required.")

    user = Patient.query.filter_by(email=email).first() or Physiotherapists.query.filter_by(email=email).first()

    if user:
        return render_template('auth/signup.html', error="User already exists. Log in instead.")

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    if role == "patient":
        user = Patient(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            city=city,
            role="patient",
            password_hash=hashed_password
        )
    elif role == "physiotherapist":
        user = Physiotherapists(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            city=city,
            role="physiotherapist",
            password_hash=hashed_password
        )

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity={"id": user.id, "role": user.role})
    response = redirect(get_dashboard_redirect(user.role))

    set_jwt_cookies(response, token)

    return response


@auth_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    email = request.form.get("email")
    password = request.form.get("password")

    if not (email and password):
        return render_template('auth/login.html', error="Email and password are required.")

    user = Patient.query.filter_by(email=email).first() or Physiotherapists.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return render_template('auth/login.html', error="Invalid email or password.")

    token = create_access_token(identity={"id": user.id, "role": user.role})
    response = redirect(get_dashboard_redirect(user.role))
    set_jwt_cookies(response, token)

    return response


@auth_bp.route('/logout', methods=['POST'], strict_slashes=False)
def logout():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response
