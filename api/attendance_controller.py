from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from functions.privilege import privilege_required
from models.attendance import Attendance, db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/attendance', methods=['POST'])
@jwt_required()
def write_attendance():
    user_id = get_jwt()["id"]
    program_id = request.json.get('program_id', "") # program_id logic should be revised
    visit_date = request.json.get('visit_date', datetime.now())
    exit_date = request.json.get('exit_date', "")

    new_entry = Attendance(user_id = user_id, program_id = program_id, visit_date = visit_date, exit_date = exit_date)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Attendance has been written successfully'})

@attendance_bp.route('/attendance', methods=['GET'])
@jwt_required()
def get_attendance():
    attendances = Attendance.query.all()
    return jsonify([attendance.to_dict() for attendance in attendances])
    
@attendance_bp.route('/attendance/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_attendance(user_id):
    attendances = Attendance.query.filter_by(user_id=user_id).all()
    return jsonify([attendance.to_dict() for attendance in attendances])

@attendance_bp.route('/attendance/<int:attendance_id>', methods=['PUT'])
@jwt_required()
def update_attendance(attendance_id):
    subject_attendance = Attendance.query.get_or_404(attendance_id)
    exit_date = request.json.get('exit_date', datetime.now())
    subject_attendance.exit_date = exit_date
    db.session.commit()
    return jsonify({'message': "Updated successfully"})
    
@attendance_bp.route('/attendance/upd/<int:attendance_id>', methods=['PUT'])
@jwt_required()
@privilege_required()
def update_attendance_admin(attendance_id):
    subject_attendance = Attendance.query.get_or_404(attendance_id)
    for key, value in request.json.items():
        # Check if the parameter is changed
        if hasattr(subject_attendance, key) and getattr(subject_attendance, key) != value:
            setattr(subject_attendance, key, value)
    db.session.commit()
    return jsonify({'message': "Updated successfully"})

@attendance_bp.route('/attendance/<int:attendance_id>', methods=['DELETE'])
@jwt_required()
@privilege_required()
def delete_attendance(attendance_id):
    subject_attendance = Attendance.query.get_or_404(attendance_id)
    db.session.delete(subject_attendance)
    db.session.commit()
    return jsonify({'message': 'An attendance has been deleted successfully'})