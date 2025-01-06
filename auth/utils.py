import jwt
import datetime
from flask import current_app


def generate_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload,
                      current_app.config['SECRET_KEY'],
                      algorithm='HS256')


def decode_jwt(token):
    try:
        payload = jwt.decode(token,
                             current_app.config['SECRET_KEY'],
                             algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
