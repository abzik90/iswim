from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from models.subscription import Subscription, db
from datetime import datetime, timedelta

from functions.privilege import privilege_required
from functions.payment import payment_required
from models.userrole import UserRole

subscriptions_bp = Blueprint('subscriptions', __name__)

# Instructor or admin subscribes user for a program
@subscriptions_bp.route('/subscriptions', methods=['POST'])
@jwt_required()
@privilege_required()
def create_subscription():
    user_id = request.json.get('user_id', "")
    program_id = request.json.get('program_id', "")
    payment_date = request.json.get('payment_date', datetime.utcnow())
    valid_thru = request.json.get('valid_thru', datetime.utcnow() + timedelta(days=30))

    new_sub = Subscription(user_id = user_id, program_id = program_id, payment_date = payment_date, valid_thru = valid_thru)
    db.session.add(new_sub)
    db.session.commit()
    return jsonify({'message': 'New subscription added successfully'})
   
# User himself does the subscription
@subscriptions_bp.route('/subscriptions/user', methods=['POST'])
@jwt_required()
@payment_required()
def create_subscription_via_payment():
    user_id = (get_jwt())["id"]
    program_id = request.json.get('program_id', "")
    payment_date = request.json.get('payment_date', datetime.utcnow())
    valid_thru = request.json.get('valid_thru', datetime.utcnow() + timedelta(days=30))

    new_sub = Subscription(user_id = user_id, program_id = program_id, payment_date = payment_date, valid_thru = valid_thru)
    db.session.add(new_sub)
    db.session.commit()
    return jsonify({'message': 'New subscription added successfully'})

@subscriptions_bp.route('/subscriptions', methods=['GET'])
@jwt_required()
@privilege_required()
def get_programs():
    subs = Subscription.query.all()
    return jsonify([sub.to_dict() for sub in subs])
    
@subscriptions_bp.route('/subscriptions/<int:sub_id>', methods=['GET'])
@jwt_required()
def get_program(sub_id):
    sub = Subscription.query.get_or_404(sub_id)
    if sub.user_id == (get_jwt())["id"] or sub.role != UserRole.USER:
        return jsonify(sub.to_dict())
    return jsonify(message='Access denied! You don\'t have permissions'), 403 


@subscriptions_bp.route('/subscriptions/<int:sub_id>', methods=['PUT'])
@jwt_required()
@privilege_required()
def update_program(sub_id):
    sub = Subscription.query.get_or_404(sub_id)
    for key, value in request.json.items():
        # Check if the parameter is changed
        if hasattr(sub, key) and getattr(sub, key) != value:
            setattr(sub, key, value)
    db.session.commit()
    return jsonify({'message': 'A subscription updated successfully'})

@subscriptions_bp.route('/subscriptions/<int:sub_id>', methods=['DELETE'])
@jwt_required()
@privilege_required()
def delete_program(sub_id):
    sub = Subscription.query.get_or_404(sub_id)
    db.session.delete(sub)
    db.session.commit()
    return jsonify({'message': 'A subscription is deleted successfully'})