from flask import Flask
from .models import db, User

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('instance.config.Config')
app.config.from_pyfile('config.py', silent=True)
db.init_app(app)

def create_superuser(email, username, password, first_name, last_name): 
    with app.app_context():
        db.create_all() 

        if User.query.filter_by(email=email).first():
            print("Superuser already exists.")
            return

        superuser = User(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=User.hash_password(password),  # Użyj metody hash_password
            is_admin=True
        )
        db.session.add(superuser)
        db.session.commit()
        print(f"Superuser {username} created successfully.")

if __name__ == "__main__":
    email = "admin@example.com"
    password = "supersecretpassword"
    first_name = "Admin"
    last_name = "Admin"
    username = first_name+ last_name

    create_superuser(email, username, password, first_name, last_name)