from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_jwt_extended.utils import set_access_cookies, set_refresh_cookies, unset_jwt_cookies
import validators
from src import db, bcrypt
from src.models import User, UserSchema
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_302_FOUND, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_404_NOT_FOUND

# schemas

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# methods


def assign_access_refresh_token(user_id, message):

    user = User.find_by_id(user_id)

    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)
    resp = jsonify({"message": message, "access": access_token,
                   "username": user.username, "email": user.email})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    resp.status_code = HTTP_302_FOUND
    return resp


def unset_jwt():
    resp = make_response(jsonify({"message": "Logout"}))
    unset_jwt_cookies(resp)
    return resp

# refresh token


class RefreshApi(Resource):
    @jwt_required(refresh=True)
    def get(self):
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id, fresh=False)
        resp = make_response(jsonify({"access_token": new_token}))
        set_access_cookies(resp, new_token)
        return resp

# action to register


class RegisterApi(Resource):
    def post(self):
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        if len(password) < 6:

            return {"error": "Password is too short"}, HTTP_400_BAD_REQUEST

        if len(username) < 3:
            return {"error": "User is too short"}, HTTP_400_BAD_REQUEST

        if not username.isalnum() or " " in username:
            return {"error": "Username should be alphanumeric, also no spaces"}, HTTP_400_BAD_REQUEST

        if not validators.email(email):
            return {"error": "Email is not valid"}, HTTP_400_BAD_REQUEST

        if User.find_by_email(email) is not None:
            return {"error": "Email is taken"}, HTTP_409_CONFLICT

        if User.find_by_username(username) is not None:
            return {"error": "User is taken"}, HTTP_409_CONFLICT

        pwd_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(username=username, email=email, password=pwd_hash)
        user.save_to_db()

        return make_response(jsonify({"username": username, "email": email}), HTTP_201_CREATED)

# action to login


class LoginApi(Resource):
    def post(self):
        email = request.json['email']
        password = request.json['password']

        user = User.find_by_email(email)

        if user:
            is_pass_correct = bcrypt.check_password_hash(
                user.password, password)

            if is_pass_correct:
                return assign_access_refresh_token(user.id, "Enabled to access")

            return make_response(jsonify({'error': 'Wrong credentials.'}), HTTP_401_UNAUTHORIZED)

        return make_response(jsonify({'error': 'User not exists'}), HTTP_404_NOT_FOUND)

# show profile of the current user


class MeApi(Resource):
    @jwt_required(fresh=True)
    def get(self):
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        return make_response(jsonify({
            "username": user.username,
            "email": user.email
        }), HTTP_200_OK)

# action to logout


class LogoutApi(Resource):
    @jwt_required()
    def get(self):
        # Revoke Fresh/Non-fresh Access and Refresh tokens
        return unset_jwt(), HTTP_204_NO_CONTENT
