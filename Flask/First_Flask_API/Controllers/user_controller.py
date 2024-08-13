from flask import Blueprint, request, jsonify
from Models.models import db, User
from Models.requestModel import UserSchema

user_controller = Blueprint('user_controller', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_controller.route('/users', methods=['POST'])
def create_user():
    json_data = request.get_json()
    errors = user_schema.validate(json_data)
    if errors:
        return jsonify(errors), 400

    data = user_schema.load(json_data)
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@user_controller.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result), 200

@user_controller.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    json_data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    errors = user_schema.validate(json_data, partial=True)
    if errors:
        return jsonify(errors), 400

    data = user_schema.load(json_data, partial=True)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

@user_controller.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
