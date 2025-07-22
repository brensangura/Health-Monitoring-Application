from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import random
from datetime import datetime
from app import db
from models import HealthData

health_bp = Blueprint('health', __name__)

# Simple symptom checker database (in a real app, this would be more comprehensive)
SYMPTOM_DATABASE = {
    'headache': {
        'possible_causes': ['tension', 'migraine', 'dehydration', 'eye strain'],
        'recommendations': ['drink water', 'rest', 'take pain reliever if needed']
    },
    'fever': {
        'possible_causes': ['infection', 'flu', 'cold'],
        'recommendations': ['rest', 'stay hydrated', 'take fever reducer']
    },
    'cough': {
        'possible_causes': ['cold', 'allergies', 'respiratory infection'],
        'recommendations': ['stay hydrated', 'use cough drops', 'consider cough medicine']
    }
}

HEALTH_TIPS = [
    "Drink at least 8 glasses of water daily.",
    "Aim for 7-9 hours of sleep each night.",
    "Take a 5-minute break every hour if you sit for long periods.",
    "Wash your hands regularly to prevent infections.",
    "Include fruits and vegetables in every meal."
]

@health_bp.route('/health')
@login_required
def health_monitor():
    return render_template('health.html')

@health_bp.route('/chatbot', methods=['POST'])
@login_required
def chatbot():
    user_message = request.json.get('message', '').lower()
    response = ""
    
    # Simple chatbot logic
    if 'symptom' in user_message or 'pain' in user_message:
        response = "I can help check symptoms. Please tell me your main symptom (e.g., headache, fever)."
    elif any(symptom in user_message for symptom in SYMPTOM_DATABASE.keys()):
        for symptom, info in SYMPTOM_DATABASE.items():
            if symptom in user_message:
                causes = ', '.join(info['possible_causes'])
                recommendations = ', '.join(info['recommendations'])
                response = f"Possible causes: {causes}. Recommendations: {recommendations}. If symptoms persist, consult a doctor."
                break
    elif 'tip' in user_message or 'advice' in user_message:
        response = random.choice(HEALTH_TIPS)
    else:
        response = "I'm here to help with health questions. You can ask about symptoms or request a health tip."
    
    return jsonify({'response': response})

@health_bp.route('/get_health_tip')
@login_required
def get_health_tip():
    return jsonify({'tip': random.choice(HEALTH_TIPS)})

@health_bp.route('/log_symptoms', methods=['POST'])
@login_required
def log_symptoms():
    symptoms = request.json.get('symptoms', '')
    
    # Find or create today's health data entry
    today = datetime.utcnow().date()
    health_data = HealthData.query.filter(
        HealthData.user_id == current_user.id,
        db.func.date(HealthData.date) == today
    ).first()
    
    if not health_data:
        health_data = HealthData(user_id=current_user.id)
        db.session.add(health_data)
    
    health_data.symptoms = symptoms
    db.session.commit()
    
    return jsonify({'success': True})
