import jwt
from datetime import datetime, timedelta
from flask import current_app


def generate_jwt(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload,
                      current_app.config['SECRET_KEY'],
                      algorithm='HS256')


def decode_jwt(token):
    try:
        payload = jwt.decode(token,
                             current_app.config['SECRET_KEY'],
                             algorithms=['HS256'])
        return payload['user_id'], payload['role']
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
