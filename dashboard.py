from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from datetime import datetime, timedelta
from app import db
from models import HealthData

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Get health data for the current user
    health_data = HealthData.query.filter_by(user_id=current_user.id)\
        .order_by(HealthData.date.desc()).limit(10).all()
    
    # Prepare data for charts
    dates = [data.date.strftime('%Y-%m-%d') for data in health_data]
    weights = [data.weight for data in health_data]
    heart_rates = [data.heart_rate for data in health_data]
    
    # Get medication reminders
    medications = []
    if health_data:
        latest_data = health_data[0]
        if latest_data.medications:
            medications = latest_data.medications.split(',')
    
    return render_template('dashboard.html', 
                         dates=dates, 
                         weights=weights, 
                         heart_rates=heart_rates,
                         medications=medications)

@dashboard_bp.route('/add_health_data', methods=['POST'])
@login_required
def add_health_data():
    data = request.json
    new_data = HealthData(
        user_id=current_user.id,
        weight=data.get('weight'),
        blood_pressure=data.get('blood_pressure'),
        heart_rate=data.get('heart_rate'),
        symptoms=data.get('symptoms'),
        medications=data.get('medications')
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'success': True})

@dashboard_bp.route('/get_health_data')
@login_required
def get_health_data():
    time_range = request.args.get('range', 'week')
    
    if time_range == 'week':
        date_threshold = datetime.utcnow() - timedelta(days=7)
    elif time_range == 'month':
        date_threshold = datetime.utcnow() - timedelta(days=30)
    else:  # year
        date_threshold = datetime.utcnow() - timedelta(days=365)
    
    health_data = HealthData.query.filter(
        HealthData.user_id == current_user.id,
        HealthData.date >= date_threshold
    ).order_by(HealthData.date.asc()).all()
    
    data = {
        'dates': [d.date.strftime('%Y-%m-%d') for d in health_data],
        'weights': [d.weight for d in health_data],
        'heart_rates': [d.heart_rate for d in health_data],
        'blood_pressures': [d.blood_pressure for d in health_data]
    }
    
    return jsonify(data)
