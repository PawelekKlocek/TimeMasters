from flask import Flask
from .models import db, User
from .auth import auth_bp
from flask_login import LoginManager

def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static', instance_relative_config=True)
    app.config.from_object('instance.config.Config')
    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)

    # Inicjalizacja LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Rejestracja blueprintu
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()  # Tworzenie tabel w bazie danych

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)