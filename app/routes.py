from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from app import app
import pandas as pd
from .models import predict_engagement
from app import dbInfo
from .models import User

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.authenticate(username, password)
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    prediction = None
    if request.method == 'POST':
        data = {
            'attendance': request.form.get('attendance'),
            'average_score': request.form.get('average_score')
            # add other fields as necessary
        }
        prediction = predict_engagement(data)
    return render_template("dashboard.html", prediction=prediction)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        attendance = request.form.get('attendance')
        average_score = request.form.get('average_score')
        # other fields...

        student_data = {
            "name": name,
            "attendnace": attendance,
            "average_score": average_score
        }

        student_id = dbInfo.students_collection.insert_one(student_data)
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

@app.route('/manage_students', methods=['GET', 'POST'])
def manage_students():
    students = dbInfo.students_collection.find()
    return render_template('manage_students.html', students=students)