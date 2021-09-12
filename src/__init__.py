from datetime import timedelta
from flask import Flask, redirect, jsonify
import os
from flask.helpers import make_response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended.utils import unset_access_cookies, unset_jwt_cookies
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from src.constants.http_status_codes import HTTP_302_FOUND, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.config import config
from flasgger import swag_from, Swagger
from src.resources.routes import init_api
from flask_cors import CORS
from swagger import swagger_config, template

cors = CORS()
db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()
api = Api()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            BASE_URL='http://localhost:5000',  # Running on localhost
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            BCRYPT_LOG_ROUNDS=4,
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            JWT_TOKEN_LOCATION=['cookies'],
            JWT_SESSION_COOKIE=True,
            JWT_ACCESS_COOKIE_PATH='/',
            JWT_REFRESH_COOKIE_PATH='/',
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(seconds=10),
            JWT_COOKIE_CSRF_PROTECT=False,
            JWT_CSRF_CHECK_FORM=True,

            SWAGGER={
                "title": "Surveys API",
                "uiversion": 3,
                # "specs_route": "/swagger/"
            }
        )
    else:
        app_settings = os.environ.get(
            'APP_SETTINGS',
            test_config
        )
        app.config.from_object(app_settings)

    db.app = app
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    Swagger(app, config=swagger_config, template=template, parse=True)

    # with app.app_context():
    #     # db.drop_all()
    #     db.create_all()

    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        # No auth header
        # return redirect(app.config['BASE_URL'] + '/', 302)
        return jsonify({
            "message": "No auth header"
        }), HTTP_302_FOUND

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        # Invalid Fresh/Non-Fresh Access token in auth header
        # resp = make_response(redirect(app.config['BASE_URL'] + '/'))
        resp = make_response(jsonify({
            "message": "Invalid Fresh/Non-Fresh Access token in auth header"
        }), HTTP_302_FOUND)
        unset_jwt_cookies(resp)
        return resp, 302

    @jwt.expired_token_loader
    def expired_token_callback(self, callback):
        # Expired auth header
        resp = make_response(
            redirect(app.config['BASE_URL'] + '/user/refresh'))
        unset_access_cookies(resp)
        return resp, 302

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "Page not Found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({"error": "Something went wrong"}), HTTP_500_INTERNAL_SERVER_ERROR

    return app


init_api(api)
