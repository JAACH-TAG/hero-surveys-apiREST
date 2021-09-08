from flask import Blueprint, request, jsonify
from src.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
import validators
from src.services.sendmail import send_mail
from src.models import Feedback, db

feedback = Blueprint("feedback", __name__, url_prefix="/api/v1/feedback")


@feedback.post("/submit")
def submit():

    name = request.json["name"]
    email = request.json["email"]
    comment = request.json["comment"]

    if not validators.email(email) :
        return jsonify({
            "error": "Please enter a valid email"
        }), HTTP_400_BAD_REQUEST

    if not name or not comment:
        return jsonify({
            "error": "Please fill all the information"
        }), HTTP_400_BAD_REQUEST

    visitor = Feedback.query.filter_by(email=email).first()

    if visitor :
        return jsonify({
            "message": "You have already submitted feedback"
        }), HTTP_409_CONFLICT

    feedback = Feedback(name=name, email=email, comment=comment)

    send_mail(name, email, comment)

    db.session.add(feedback)
    db.session.commit()

    return jsonify({
        "name": name,
        "email": email,
        "comment": comment,
    }), HTTP_200_OK