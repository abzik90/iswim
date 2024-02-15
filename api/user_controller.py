from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from functions.privilege import privilege_required
from sqlalchemy import desc

from app import db
from models.user import User
from models.subscription import Subscription
from models.attendance import Attendance
from models.userrole import UserRole
from datetime import datetime

users_bp = Blueprint('users', __name__)
   
@users_bp.route('/register', methods=['POST'])
def create_user():
    firstname = request.json.get('firstname', "")
    surname = request.json.get('surname', "")
    email = request.json.get('email', "")    
    password = request.json.get('password', "")
    role = request.json.get('role', UserRole.ADMIN)
    age = request.json.get('age', "")
    new_user = User(firstname=firstname, surname=surname, email=email,password=password, role = role, age =age)
    if new_user.is_valid():
        db.session.add(new_user)
        db.session.commit()
        user_identity = {"id": new_user.id, "email": new_user.email}
        access_token = create_access_token(identity=user_identity)
        return jsonify({'access_token': access_token,'message': 'User created successfully'}), 200
    return jsonify({'message': 'Invalid user information'}), 401

@users_bp.route('/login', methods=['POST'])
def authenticate_user():
    email = request.json.get('email', "")
    password = request.json.get('password', "")
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        user_identity = {"id": user.id, "email": user.email, "role": user.role} #hopefully this isn't a security threat :)
        access_token = create_access_token(identity=user_identity)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])
    
@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@privilege_required()
def update_user(user_id):
    subject_user = User.query.get_or_404(user_id)
    for key, value in request.json.items():
        # Check if the parameter is changed
        if hasattr(subject_user, key) and getattr(subject_user, key) != value:
            setattr(subject_user, key, value)
    db.session.commit()

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@privilege_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# TODO: after creating controllers for attendance and subscription fill in the sample values in the table
#       and finish this function
@users_bp.route('/user/validate', methods=['GET'])
@jwt_required()
def validate_user():
    current_user_id = get_jwt()["id"]
    current_date = datetime.utcnow().date()
    subscription = Subscription.query.filter_by(user_id=current_user_id).filter(Subscription.payment_date <= current_date, Subscription.valid_thru >= current_date).order_by(desc(Subscription.payment_date)).first()

    if subscription:
        new_attendance = Attendance(user_id=current_user_id)
        db.session.add(new_attendance)
        db.session.commit()
        return jsonify(message='Success: Attendance recorded'), 200
    else:
        return jsonify(message='Access prohibited: No valid subscription'), 403