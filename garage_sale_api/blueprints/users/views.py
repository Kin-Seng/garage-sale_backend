from flask import Blueprint, jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import (   
    create_access_token,
    get_jwt_identity,
    jwt_required
)
from datetime import datetime,timedelta
import jwt
from models.users import Users
import os

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"

# sending data to react
@users_api_blueprint.route('/userlist', methods=['GET'])
def userlist():
    userlist = Users.select()
    
    return jsonify(
       [
           {
                "username": user.username,
                "email": user.email
            } for user in userlist
        ]
    )   

# create new user
@users_api_blueprint.route('/create', methods=['POST'])
def users_create():

    #chk if the request is in JSON format
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    email = request.json.get('email', None)

    profile = request.json.get('profile', None)
    age = request.json.get('age', None)
    address = request.json.get('address', None)
    phoneNo = request.json.get('phoneNo', None)
    
    password = generate_password_hash(password)
    
    errors=[]

    if not username:
        errors.append('username')
    if not password:
        errors.append('password')
    if not email:
        errors.append('email')
    if errors:
        return jsonify({"msg": {"Missing parameters": [error for error in errors]}}), 400
    
    username_check = Users.get_or_none(Users.username == username)
    email_check = Users.get_or_none(Users.email == email)

    if not username_check and not email_check:

        u = Users(username=username, email=email, pwd=generate_password_hash(password),profile=profile,age=age,address=address, phone_no = phoneNo)
        u.save()
       
        user = Users.get(Users.username == username)
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "message": "Successfully created a user and signed in.",
            "status": "success",
            "user": {
                "id": user.id,
                "profile_picture": user.profile_pic,
                "username": user.username
            }
        }), 200
    else:
        return jsonify({"msg": "username or email already used"}), 400
    

# login
@users_api_blueprint.route('/login', methods=['POST'])
def login():

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
   
    errors = []
    if not email:
        errors.append("email")
    if not password:
        errors.append("password")
    if errors:
        return jsonify({"msg": {"Missing parameters":[error for error in errors]}}), 400

    user = Users.get_or_none(Users.email == email)
    
    
    # if user and check_password_hash(user.pwd, password):
    if user or check_password_hash(user.pwd, password):    
        
        expires = timedelta(days=365)
        access_token = create_access_token(user.id, expires_delta=expires)

        return jsonify({
            "access_token": access_token,
            "message": "Successfully signed in.",
            "status": "success",
            "user": {
                "id": user.id,
                "username": user.username
            }
        }), 200
    else:
        return jsonify({"msg": "Bad login"}), 404

    




