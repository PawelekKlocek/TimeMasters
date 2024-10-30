from models import db, User
from flask import Flask
from config import Config
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Konfiguracja superużytkownika
def create_superuser(email, username, password):
    with app.app_context():
        # Sprawdź, czy użytkownik już istnieje
        if User.query.filter_by(email=email).first():
            print("Superuser already exists.")
            return

        # Utwórz nowego superużytkownika
        superuser = User(
            email=email,
            username=username,
            password=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(superuser)
        db.session.commit()
        print(f"Superuser {username} created successfully.")

# Parametry superużytkownika (przykładowe)
if __name__ == "__main__":
    # Możesz też pobierać dane z input() dla większej interaktywności
    email = "admin@example.com"
    username = "admin"
    password = "supersecretpassword"
    create_superuser(email, username, password)