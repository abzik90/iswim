from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from functions.privilege import privilege_required
from models.programs import Programs, db

programs_bp = Blueprint('programs', __name__)

@programs_bp.route('/programs', methods=['POST'])
@jwt_required()
@privilege_required()
def create_program():
    title = request.json.get('title', "")
    description = request.json.get('description', "")
    start_time = request.json.get('start_time', "00:00:00")
    end_time = request.json.get('end_time', "00:00:00")

    new_program = Programs(title = title, description = description, start_time = start_time, end_time = end_time)
    db.session.add(new_program)
    db.session.commit()
    return jsonify({'message': 'New program created successfully'})
   

@programs_bp.route('/programs', methods=['GET'])
@jwt_required()
def get_programs():
    programs = Programs.query.all()
    return jsonify([program.to_dict() for program in programs])
    
@programs_bp.route('/programs/<int:program_id>', methods=['GET'])
@jwt_required()
def get_program(program_id):
    program = Programs.query.get_or_404(program_id)
    return jsonify(program.to_dict())


@programs_bp.route('/programs/<int:program_id>', methods=['PUT'])
@jwt_required()
@privilege_required()
def update_program(program_id):
    subject_program = Programs.query.get_or_404(program_id)
    for key, value in request.json.items():
        # Check if the parameter is changed
        if hasattr(subject_program, key) and getattr(subject_program, key) != value:
            setattr(subject_program, key, value)
    db.session.commit()

@programs_bp.route('/programs/<int:program_id>', methods=['DELETE'])
@jwt_required()
@privilege_required()
def delete_program(program_id):
    subject_program = Programs.query.get_or_404(program_id)
    db.session.delete(subject_program)
    db.session.commit()
    return jsonify({'message': 'A program is deleted successfully'})