import os
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, abort
from functools import wraps

JWT_SECRET = os.environ.get('JWT_SECRET', 'dev_jwt_secret')
JWT_EXPIRE_MINUTES = 60 * 24  # 1 day default

# PUBLIC_INTERFACE
def hash_password(password: str) -> str:
    """Generate hashed password."""
    return generate_password_hash(password)

# PUBLIC_INTERFACE
def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return check_password_hash(password_hash, password)

# PUBLIC_INTERFACE
def generate_jwt(user_id: int) -> str:
    """Generate a JWT token for a given user ID."""
    exp = datetime.utcnow() + timedelta(minutes=int(os.environ.get('JWT_EXPIRE_MINUTES', JWT_EXPIRE_MINUTES)))
    payload = {
        'user_id': user_id,
        'exp': exp
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

# PUBLIC_INTERFACE
def decode_jwt(token: str) -> dict:
    """Decode a JWT token and return its payload."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        abort(401, 'Token has expired')
    except jwt.InvalidTokenError:
        abort(401, 'Invalid token')

# PUBLIC_INTERFACE
def jwt_required(fn):
    """Decorator that ensures the requester has a valid JWT token."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header or not auth_header.startswith('Bearer '):
            abort(401, 'Authorization header is expected (Bearer token)')
        token = auth_header[len('Bearer '):]
        payload = decode_jwt(token)
        request.user_id = payload['user_id']
        return fn(*args, **kwargs)
    return wrapper

