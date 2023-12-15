import jwt
import datetime

from .config import SECRET_JWT


def generate_token(user_id, expires_delta):
    payload = {
        'id': user_id,
        'exp': datetime.datetime.utcnow() + expires_delta,
        'iat': datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_JWT, algorithm="HS256")


def update_last_request(user):
    user.last_request = datetime.datetime.utcnow()
    user.save()