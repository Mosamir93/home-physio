import requests
from flask import current_app


def validate_google_token(token):
    """validates the google token"""
    response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}", timeout=5)
    if response.status_code == 200:
        return response.json()
    
    print(f"Google token validation failed with status code: {response.status_code}")
    return None

def get_google_user_info(auth_code):
    """Exchange auth code for tokens and retrieve user info."""
    token_url = "https://oauth2.googleapis.com/token"
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"

    data = {
        "code": auth_code,
        "client_id": current_app.config["GOOGLE_CLIENT_ID"],
        "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
        "redirect_uri": "postmessage",
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data, timeout=5)
    if response.status_code != 200:
        print("Error fetching token:", response.json())
        return None

    tokens = response.json()
    access_token = tokens.get("access_token")

    userinfo_response = requests.get(userinfo_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=5)
    if userinfo_response.status_code != 200:
        print("Error fetching user info:", userinfo_response.json())
        return None

    return userinfo_response.json()
