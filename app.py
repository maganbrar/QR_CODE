from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random
import string
from utils.qr_generator import generate_qr
import os

app = Flask(__name__)

DB_PATH = 'database/students.db'  # Your SQLite DB file
QR_PATH = 'static/qr_code.png'

# ❌ Removed this section that deletes DB on every run
# db_file = 'database/students.db'
# if os.path.exists(db_file):
#     os.remove(db_file)

# Helper: Generate coupon code
def generate_coupon(name, contact):
    name_part = (name[:3].upper() if len(name) >= 3 else (name.upper() + 'XXX')[:3])
    contact_part = (contact[-3:] if len(contact) >= 3 else ''.join(random.choices(string.digits, k=3)))
    coupon = f'B{name_part}{contact_part}E'
    return coupon

# Initialize DB (make sure table exists)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            name TEXT,
            contact TEXT,
            email TEXT,
            university TEXT,
            branch TEXT,
            coupon TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route 1: Show QR code linking to /register
@app.route('/')
def show_qr():
    base_url = request.host_url.strip('/')
    register_url = f"{base_url}/register"
    generate_qr(register_url, QR_PATH)
    return render_template('qr_code.html')

# Route 2: Register form & submission
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        name = request.form.get('name', '').strip()
        contact = request.form.get('contact', '').strip()
        email = request.form.get('email', '').strip()
        university = request.form.get('university', '').strip()
        branch = request.form.get('branch', '').strip()

        coupon = generate_coupon(name, contact)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (student_id, name, contact, email, university, branch, coupon)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, name, contact, email, university, branch, coupon))
        conn.commit()
        conn.close()

        message = f"Thank you, {name}! Your course offer coupon code: {coupon}"
        return render_template('register.html', message=message)

    return render_template('register.html')

# Route 3: Admin panel - list all students
@app.route('/admin')
def admin_panel():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('admin.html', students=students)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and a stream handler
file_handler = logging.FileHandler('app.log')
stream_handler = logging.StreamHandler()

# Create a formatter and set it for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# ...

# Route 1: Show QR code linking to /register
@app.route('/')
def show_qr():
    logger.info('Showing QR code')
    base_url = request.host_url.strip('/')
    register_url = f"{base_url}/register"
    generate_qr(register_url, QR_PATH)
    return render_template('qr_code.html')

# Route 2: Register form & submission
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        logger.info('Register form submitted')
        student_id = request.form.get('student_id', '').strip()
        name = request.form.get('name', '').strip()
        contact = request.form.get('contact', '').strip()
        email = request.form.get('email', '').strip()
        university = request.form.get('university', '').strip()
        branch = request.form.get('branch', '').strip()

        coupon = generate_coupon(name, contact)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (student_id, name, contact, email, university, branch, coupon)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, name, contact, email, university, branch, coupon))
        conn.commit()
        conn.close()

        logger.info(f'Student registered: {name}')
        message = f"Thank you, {name}! Your course offer coupon code: {coupon}"
        return render_template('register.html', message=message)

    logger.info('Showing register form')
    return render_template('register.html')

# Route 3: Admin panel - list all students
@app.route('/admin')
def admin_panel():
    logger.info('Showing admin panel')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    logger.info('Admin panel shown')
    return render_template('admin.html', students=students)

# ...

if __name__ == '__main__':
    logger.info('Initializing database')
    init_db()
    logger.info('Starting app')
    app.run(host='0.0.0.0', port=5000, debug=True)



