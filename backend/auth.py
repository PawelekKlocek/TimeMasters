from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
import pandas as pd
from io import BytesIO
from .models import db, User, Timer
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

def generate_unique_username(first_name, last_name):
    base_username = f"{first_name}.{last_name}".lower()
    username = base_username
    counter = 1
    while User.query.filter_by(username=username).first():
        username = f"{base_username}{counter}"
        counter += 1
    return username

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully', 'success')
            if user.is_admin:
                return redirect(url_for('auth.admin'))
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Login unsuccessful. Check email and password', 'danger')
    return render_template('login.html')

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@auth_bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('auth.dashboard'))
    return render_template('admin.html')

@auth_bp.route('/save_timer', methods=['POST'])
@login_required
def save_timer():
    data = request.get_json()
    hours = data.get('hours')
    minutes = data.get('minutes')
    seconds = data.get('seconds')
    total_seconds = hours * 3600 + minutes * 60 + seconds

    new_timer = Timer(
        user_id=current_user.id,
        time=total_seconds,
        date=datetime.utcnow()
    )
    db.session.add(new_timer)
    db.session.commit()

    return jsonify({"status": "success", "message": "Timer data saved"})

@auth_bp.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        return jsonify({"status": "error", "message": "Access denied"}), 403

    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    username = generate_unique_username(first_name, last_name)
    hashed_password = User.hash_password(password)

    new_user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
        is_admin=False
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "User added successfully", "username": username})


@auth_bp.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    if not current_user.is_admin:
        return jsonify({"status": "error", "message": "Access denied"}), 403

    data = request.get_json()
    user_id = data.get('ID')

    user = User.query.filter_by(id=user_id).first()

    if user:
        # Usuwanie powiązanych rekordów z tabeli Timer
        Timer.query.filter_by(user_id=user.id).delete()

        # Usunięcie użytkownika za pomocą metody statycznej
        result = User.delete_user(user.id)
        if result:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Could not delete user."})
    else:
        return jsonify({"status": "error", "message": "User not found."})


@auth_bp.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username} for user in users]
    return jsonify(user_list)
    

def generate_excel_report(user_id, start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        user = User.query.get(user_id)
        if not user:
            return None, "User not found."

        timers = Timer.query.filter(
            Timer.user_id == user_id,
            Timer.date >= start_date,
            Timer.date <= end_date
        ).all()

        data = {
            "Date": [timer.date.strftime("%Y-%m-%d") for timer in timers],
            "Time (seconds)": [timer.time for timer in timers]
        }
        df = pd.DataFrame(data)

        total_time = df["Time (seconds)"].sum()


        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Report")

            workbook = writer.book
            worksheet = writer.sheets["Report"]
            worksheet.write(len(df) + 1, 0, "Total Time (seconds)")
            worksheet.write(len(df) + 1, 1, total_time)

        output.seek(0)

        return output, None
    except Exception as e:
        return None, f"Error generating report: {user_id}"

@auth_bp.route('/generate_report', methods=['POST'])
@login_required
def generate_report():
    data = request.get_json()
    user_id = data.get('user_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    report_file, message = generate_excel_report(user_id, start_date, end_date)

    if report_file:
        return send_file(
            report_file,
            as_attachment=True,
            download_name=f"report_{user_id}_{start_date}_to_{end_date}.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        return jsonify({"status": "error", "message": message}), 400

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))
