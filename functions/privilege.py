from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify
from models.userrole import UserRole

def privilege_required():
    def decorator(func):
        @wraps(func)
        def original_function(*args, **kwargs):
            current_user_claims = get_jwt()
            if current_user_claims['role'] in [UserRole.INSTRUCTOR.value, UserRole.ADMIN.value]:
                return func(*args, **kwargs)
            else:
                return jsonify(message='Access denied! You don\'t have permissions'), 403
        return original_function
    return decorator

# def is_self_required(user_id):
#     def is_self(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             current_user_claims = get_jwt_claims()
#             if user_id == current_user_claims["id"] or current_user_claims['role'] in [UserRole.INSTRUCTOR.value, UserRole.ADMIN.value]:
#                 return func(*args, **kwargs)
#             return jsonify(message='Access denied! You don\'t have permissions'), 403 
#         return wrapper
#     return is_self
