import requests
from flask import current_app


def validate_google_token(token):
    """validates the google token"""
    response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
    if response.status_code == 200:
        return response.json()
    return None
