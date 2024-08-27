from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
from service.db.redis import get_user, check_key, add_user

auth_bp = Blueprint('auth', __name__)

def init_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key
    jwt = JWTManager(app)
    return jwt

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = get_user(username)
    
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            access_token = create_access_token(identity={'username': username})
            return jsonify({
                'access_token': access_token,
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify({"error": "User does not exist"}), 404

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if check_key(f"user:{username}"):
        return jsonify({"error": "User already exists"}), 409
    add_user(username, password)

    return jsonify({"message": "User registered successfully"}), 201
