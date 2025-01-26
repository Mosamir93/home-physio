import requests
from flask import current_app


def validate_google_token(token):
    """validates the google token"""
    response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}", timeout=5)
    if response.status_code == 200:
        return response.json()
    
    print(f"Google token validation failed with status code: {response.status_code}")
    return None
