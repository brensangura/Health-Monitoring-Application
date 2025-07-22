import sqlite3
import streamlit as st
from datetime import datetime

def init_db():
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    
    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  email TEXT UNIQUE,
                  password TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS health_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  date TEXT,
                  weight REAL,
                  blood_pressure TEXT,
                  heart_rate INTEGER,
                  symptoms TEXT,
                  medications TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS doctors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  specialty TEXT,
                  contact_info TEXT,
                  availability TEXT,
                  bio TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  doctor_id INTEGER,
                  content TEXT,
                  timestamp TEXT,
                  is_from_doctor INTEGER,
                  FOREIGN KEY(user_id) REFERENCES users(id),
                  FOREIGN KEY(doctor_id) REFERENCES doctors(id))''')
    
    # Insert sample doctors if none exist
    c.execute("SELECT COUNT(*) FROM doctors")
    if c.fetchone()[0] == 0:
        sample_doctors = [
            ("Dr. Smith", "Cardiology", "smith@hospital.com", "Mon-Fri 9am-5pm", "Cardiologist with 10 years experience"),
            ("Dr. Johnson", "Pediatrics", "johnson@hospital.com", "Tue-Sat 10am-6pm", "Pediatric specialist"),
            ("Dr. Lee", "Neurology", "lee@hospital.com", "Mon-Thu 8am-4pm", "Neurology department head")
        ]
        c.executemany("INSERT INTO doctors (name, specialty, contact_info, availability, bio) VALUES (?, ?, ?, ?, ?)", 
                     sample_doctors)
    
    conn.commit()
    conn.close()

def get_user_data(username):
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return {'id': user[0], 'username': user[1], 'email': user[2], 'password': user[3]}
    return None

# Add other database operations as needed...
