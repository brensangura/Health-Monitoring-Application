from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from models import Doctor, Message

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/doctor')
@login_required
def doctor_contact():
    doctors = Doctor.query.all()
    return render_template('doctor.html', doctors=doctors)

@doctor_bp.route('/get_doctor/<int:doctor_id>')
@login_required
def get_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify({
        'name': doctor.name,
        'specialty': doctor.specialty,
        'contact_info': doctor.contact_info,
        'availability': doctor.availability,
        'bio': doctor.bio
    })

@doctor_bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    doctor_id = request.json.get('doctor_id')
    content = request.json.get('content')
    
    if not doctor_id or not content:
        return jsonify({'success': False, 'error': 'Missing data'})
    
    message = Message(
        user_id=current_user.id,
        doctor_id=doctor_id,
        content=content,
        is_from_doctor=False
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'success': True})

@doctor_bp.route('/get_messages/<int:doctor_id>')
@login_required
def get_messages(doctor_id):
    messages = Message.query.filter(
        ((Message.user_id == current_user.id) & (Message.doctor_id == doctor_id))
    ).order_by(Message.timestamp.asc()).all()
    
    message_list = [{
        'id': msg.id,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M'),
        'is_from_doctor': msg.is_from_doctor
    } for msg in messages]
    
    return jsonify({'messages': message_list})
