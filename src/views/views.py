# src/auth/views.py
from flask import Blueprint, json, request, make_response, jsonify
from flask.views import MethodView

from server import bcrypt, db
from server.src.models import User, BlacklistToken

# auth_blueprint = Blueprint('auth', __name__, url_prefix="/api/v1/auth") 


# class RegisterAPI(MethodView):
#     # registration resource
    
#     def post(self):
#         post_data = request.get_json()
#         user = User.query.filter_by(email=post_data.get('email')).first()
#         if not user:
#             try:
#                 user = User(
#                     email=post_data.get('email'),
#                     password=post_data.get('password')
#                 )
#                 db.session.add(user)
#                 db.session.commit()
#                 auth_token = user.encode_auth_token(user.id)
#                 responseObject = {
#                     'status': 'success',
#                     'message': 'Successfully registered',
#                     'auth_token': auth_token.decode()
#                 }
#                 return make_response(jsonify(responseObject)), 201
#             except Exception as e:
#                 responseObject = {
#                     'status':'fail',
#                     'message': 'Some error occurred. Please try again.'
#                 }
#                 return make_response(jsonify(responseObject)), 401
#         else:
#             responseObject = {
#                 'status': 'fail',
#                 'message': 'User already exists. Please Log in.'
#             }
#             return make_response(jsonify(responseObject)), 202

# registration_view = RegisterAPI.as_view('register_api')

# auth_blueprint.add_url_rule(
#     '/auth/register',
#     view_func=registration_view,
#     methods=['POST']
# )