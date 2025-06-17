import secrets
import datetime
from functools import wraps
from flask import session, jsonify
from config import SECURITY_CONFIG

def generate_verification_code():
    """Generate a 6-character verification code"""
    return secrets.token_hex(3).upper()

def generate_reset_token():
    """Generate a secure reset token"""
    return secrets.token_urlsafe(32)

def get_verification_expiry():
    """Get verification code expiry time"""
    return datetime.datetime.now() + datetime.timedelta(
        minutes=SECURITY_CONFIG['verification_code_expiry_minutes']
    )

def get_reset_expiry():
    """Get password reset token expiry time"""
    return datetime.datetime.now() + datetime.timedelta(
        hours=SECURITY_CONFIG['password_reset_expiry_hours']
    )

def is_expired(expiry_str):
    """Check if a timestamp string has expired"""
    if not expiry_str:
        return True
    try:
        expiry_time = datetime.datetime.fromisoformat(expiry_str)
        return datetime.datetime.now() > expiry_time
    except:
        return True

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        if not session.get('is_admin', False):
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function
