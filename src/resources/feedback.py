# src/models/feedback.py
from flask import request, jsonify, make_response
from flask_restful import Resource
import validators
from src.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from src.services.sendmail import send_mail
from src.models import Feedback


class FeedbackApi(Resource):
    def post(self):

        name = request.json["name"]
        email = request.json["email"]
        comment = request.json["comment"]

        if not validators.email(email) :
            return {
                "error": "Please enter a valid email"
            }, HTTP_400_BAD_REQUEST

        if not name or not comment:
            return {
                "error": "Please fill all the information"
            }, HTTP_400_BAD_REQUEST

        visitor = Feedback.query.filter_by(email=email).first()

        if visitor :
            return {
                "message": "You have already submitted feedback"
            }, HTTP_409_CONFLICT

        feedback = Feedback(name=name, email=email, comment=comment)

        send_mail(name, email, comment)

        feedback.save_to_db()

        return make_response(jsonify({
            "name": name,
            "email": email,
            "comment": comment,
        }), HTTP_200_OK)