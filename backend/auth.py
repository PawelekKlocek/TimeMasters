import os

from flask import Flask, render_template, redirect, url_for, flash, request

from config import Config
from models import db, User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__, template_folder=os.path.join("..", "frontend", "templates"))

app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Check email and password', 'danger')
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return f"Hello, {current_user.username}!"


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8082)
