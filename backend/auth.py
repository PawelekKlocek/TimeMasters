from flask import Flask, request, jsonify, Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input, please provide both username and password"}), 400

    username = data['username']
    password = data['password']

    return jsonify({"message": "Login successful", "username": username}), 200

app = Flask(__name__)
app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(debug=True, port=8082)
