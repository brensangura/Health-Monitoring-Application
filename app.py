from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Import models after db initialization to avoid circular imports
from models import User, HealthData, Doctor, Message

# Import blueprints
from dashboard import dashboard_bp
from health_monitor import health_bp
from doctor_contact import doctor_bp

# Register blueprints
app.register_blueprint(dashboard_bp)
app.register_blueprint(health_bp)
app.register_blueprint(doctor_bp)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login logic would go here
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Registration logic would go here
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
