from flask import Flask, render_template
from backend.config import Config
from backend.models import db, User

def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/')
    def login():
        return render_template('login.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/admin')
    def admin():
        return render_template('admin.html')

    with app.app_context():
        db.create_all()  # Tworzenie tabel w bazie danych

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)