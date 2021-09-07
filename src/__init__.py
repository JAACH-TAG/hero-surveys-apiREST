from flask import Flask, redirect, jsonify
import os
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.auth import auth
from src.surveys import surveys
from src.models import db, bcrypt, Survey
from src.config import config

def create_app(test_config=config.ProductionConfig):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY"),
            BCRYPT_LOG_ROUNDS = 4,
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
        )
    else :
        app_settings = os.environ.get(
        'APP_SETTINGS',
        test_config
        )
        app.config.from_object(app_settings)
        
    db.app = app
    db.init_app(app)

    with app.app_context():
        db.create_all()

    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(surveys)

    bcrypt.init_app(app)
    
    @app.get("/<url>")
    def to_url(url):
        survey = Survey.query.filter_by(url=url).first_or_404()
        if survey:
            survey.visits = survey.visits+1
            db.session.commit()
            return redirect(survey.url)
        
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "Not found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({"error": "Something went wrong"}), HTTP_500_INTERNAL_SERVER_ERROR

    return app











# ###################################################
# # config
# app = Flask(__name__, instance_relative_config=False)
# CORS(app)
# # app.config['SECRET_KEY'] = 'hardsecretkey'
# app_settings = environ.get(
#     'APP_SETTINGS',
#     'api.server.config.DevelopmentConfig'
# )
# app.config.from_object(app_settings)