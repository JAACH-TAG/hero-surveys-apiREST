from flask import Blueprint, jsonify, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from src.models import db, Survey
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

surveys  = Blueprint("surveys", __name__, url_prefix="/api/v1/surveys")

# CREAR UNA ENCUESTA U OBTENER TODAS
@surveys.route("/" , methods=["GET", "POST"])
@swag_from("./docs/surveys/create_survey.yml")
@jwt_required()
def all_surveys():

    current_user = get_jwt_identity()

    if request.method == "POST":

        title = request.json['title']
        image = request.json['image']
        url = request.json['url']

        if not title:
            return jsonify({
                "error" : "Title is required"
            }), HTTP_400_BAD_REQUEST

        if not url:
            return jsonify({
                "message": "Url is not valid"
            }), HTTP_400_BAD_REQUEST


        survey = Survey(title=title, image=image, url=url, user_id = current_user)
        db.session.add(survey)
        db.session.commit()

        return jsonify({
            "id" : survey.id,
            "title" : survey.title,
            "image" : survey.image,
            "url": survey.url,
            "visits": survey.visits,
            "date_created" : survey.date_created,
            "date_updated" : survey.date_updated,
            "user_id" : survey.user_id,
            "sections": survey.sections,
        }), HTTP_201_CREATED

    else :

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        surveys = Survey.query.filter_by(user_id = current_user).paginate(page=page, per_page=per_page)

        data = []


        for survey in surveys.items:
            data.append({
            "id" : survey.id,
            "title" : survey.title,
            "image" : survey.image,
            "url": survey.url,
            "visits" : survey.visits,
            "date_created" : survey.date_created,
            "date_updated" : survey.date_updated,
            "user_id" : survey.user_id,
            "sections": survey.sections,
            })

        meta = {
        "page" : surveys.page, 
        "pages": surveys.pages, 
        "total_count": surveys.total, 
        "prev_page": surveys.prev_num, 
        "next_page": surveys.next_num,
        "has_prev": surveys.has_prev,
        "has_next": surveys.has_next
        }

        return jsonify({
                "data": data,
                "meta": meta
            }), HTTP_200_OK

# OBTENER UNA ENCUESTA
@surveys.get("/<int:id>/")
@jwt_required()
def survey(id):
    current_user = get_jwt_identity()

    survey = Survey.query.filter_by(user_id = current_user, id=id).first()

    if not survey:
        return jsonify({
            "error": "Item not found"
        }), HTTP_404_NOT_FOUND

    return jsonify({
        "id" : survey.id,
        "title" : survey.title,
        "image" : survey.image,
        "url": survey.url,
        "visits" : survey.visits,
        "date_created" : survey.date_created,
        "date_updated" : survey.date_updated,
        "user_id" : survey.user_id,
        "sections": survey.sections,
    }), HTTP_200_OK

# ACTUALIZAR
@surveys.put("/<int:id>/")
@surveys.patch("/<int:id>/")
@jwt_required()
def update_survey(id):
    current_user = get_jwt_identity()
    survey = Survey.query.filter_by(user_id = current_user, id=id).first()

    if not survey:
        return jsonify({
            "error": "Item not found"
        }), HTTP_404_NOT_FOUND


    title = request.json['title']
    image = request.json['image']
    url = request.json['url']

    if not title:
            return jsonify({
                "error" : "Title is required"
            }), HTTP_400_BAD_REQUEST

    if not url:
            return jsonify({
                "message": "Url is not valid"
            }), HTTP_400_BAD_REQUEST

    survey.title = title
    survey.image = image
    survey.url = url

    db.session.commit()

    return jsonify({
        "id" : survey.id,
        "title" : survey.title,
        "image" : survey.image,
        "url" : survey.url,
        "visits" : survey.visits,
        "date_created" : survey.date_created,
        "date_updated" : survey.date_updated,
        "user_id" : survey.user_id,
        "sections": survey.sections,
    }), HTTP_200_OK
    
# ELIMINAR
@surveys.delete("/<int:id>/")
@jwt_required()
def delete_survey(id):

    current_user = get_jwt_identity()
    survey = Survey.query.filter_by(user_id=current_user,id=id).first()

    if not survey:
        return jsonify({
            "error": "Item not found"
        }), HTTP_404_NOT_FOUND

    db.session.delete(survey)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT

# STATS
@surveys.get("/stats")
@jwt_required()
def get_stats():
    current_user = get_jwt_identity()
    data = []

    items = Survey.query.filter_by(user_id=current_user).all()

    for item in items:
        new_link = {
            "visits": item.visits,
            "url": item.url,
            "id": item.id,
        }
        data.append(new_link)

    return jsonify({"data": data}), HTTP_200_OK