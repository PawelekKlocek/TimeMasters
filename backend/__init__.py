from flask import Flask
from config import Config
from models import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/')
    def home():
        return 'Hello World!'

    with app.app_context():
        db.create_all()  # Tworzenie tabel w bazie danych

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)