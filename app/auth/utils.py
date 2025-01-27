from flask import url_for
from datetime import timedelta


def get_dashboard_redirect(role):
    if role == "patient":
        return url_for('patient.dashboard')
    elif role == "physiotherapist":
        return url_for('physio.dashboard')

def set_jwt_cookies(response, token):
    expiration = timedelta(days=7)
    response.set_cookie('access_token_cookie', token, httponly=True, secure=False, max_age=expiration)
