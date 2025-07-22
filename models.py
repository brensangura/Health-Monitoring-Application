from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    health_data = db.relationship('HealthData', backref='user', lazy='dynamic')
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    weight = db.Column(db.Float)
    blood_pressure = db.Column(db.String(20))
    heart_rate = db.Column(db.Integer)
    symptoms = db.Column(db.String(500))
    medications = db.Column(db.String(500))

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialty = db.Column(db.String(100))
    contact_info = db.Column(db.String(200))
    availability = db.Column(db.String(500))
    bio = db.Column(db.Text)
    messages = db.relationship('Message', backref='doctor', lazy='dynamic')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_from_doctor = db.Column(db.Boolean)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
