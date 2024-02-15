from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify
from models.userrole import UserRole

# TODO: implement the payment verification
def payment_required():
    def decorator(func):
        @wraps(func)
        def original_function(*args, **kwargs):
            return func(*args, **kwargs)
        return original_function
    return decorator