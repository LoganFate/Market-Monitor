from flask import Blueprint, jsonify, request
from flask_login import login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db

user_routes = Blueprint('users', __name__)


@user_routes.route('/')
@login_required
def users():
    """
    Query for all users and returns them in a list of user dictionaries
    """
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
@login_required
def user(id):
    """
    Query for a user by id and returns that user in a dictionary
    """
    user = User.query.get(id)
    return user.to_dict()


@user_routes.route('/signup', methods=['POST'])
def signup():
    """
    Register a new user with the provided details.
    """
    data = request.get_json()


    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required.'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already in use.'}), 409

    new_user = User(
        email=data['email'],
        password=generate_password_hash(data['password']),
        name=data.get('name'),
        username=data.get('username'),
        user_about=data.get('user_about')
    )

    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({'message': 'User created successfully.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@user_routes.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user and returns a token.
    """
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):

        login_user(user)

        return jsonify({'message': 'Login successful.'}), 200
    else:
        return jsonify({'error': 'Invalid credentials.'}), 401

@user_routes.route('/profile', methods=['GET'])
@login_required
def get_user_profile():
    """
    Retrieves the profile of the currently logged-in user.
    """
    user = current_user
    if user is not None:

        user_profile = {
            "email": user.email,
            "username": user.username,
            "user_intro": user.user_intro,
            "profile_pic": user.profile_pic
        }
        return jsonify(user_profile), 200
    else:
        return jsonify({"error": "User not found"}), 404


@user_routes.route('/profile', methods=['PUT'])
@login_required
def update_user_profile():
    """
    Allows users to update their profile information.
    """
    user = current_user
    if user is None:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.username = data.get('username', user.username)
    user.user_intro = data.get('user_intro', user.user_intro)

    # Add validation errors here ***

    if user.name is not None:
        user.name = user.name
    if  user.username is not None:
        user.username = user.username
    if user.user_intro is not None:
        user.user_intro = user.user_intro

    db.session.commit()

    return jsonify({
        "name": user.name,
        "username": user.username,
        "user_intro": user.user_intro
    }), 200


@user_routes.route('/profile', methods=['DELETE'])
@login_required
def delete_profile():
    """
    Allows users to delete their account.
    """
    user = current_user
    db.session.delete(user)
    db.session.commit()
    return '', 204
