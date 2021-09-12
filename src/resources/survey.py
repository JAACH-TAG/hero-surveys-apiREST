import os
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.utils import redirect
from src import db
from src.models import Survey, SurveySchema
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
# from werkzeug.utils import secure_filename

# SCHEMAS
survey_schema = SurveySchema()
surveys_schema = SurveySchema(many=True)

# CREAR UNA ENCUESTA U OBTENER TODAS


class ManipulateSurveyApi(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        title = request.json.get("title", None)
        image = request.json.get("image", None)
        url = request.json.get("url", None)

        if not title:
            return {
                "error": "Title is required"
            }, HTTP_400_BAD_REQUEST

        if not image:
            return {
                "error": "Image is required"
            }, HTTP_400_BAD_REQUEST

        # filename = secure_filename(image.filename)
        # mimetype = image.mimetype
        base_url = ("http://localhost:5000/s/" if os.environ.get("FLASK_ENV")
                    == "development" else "https://surveys-api-rest.herokuapp.com/s/")
        public_url = base_url + url

        survey = Survey(title=title, image=image,
                        url=public_url, user_id=current_user)
        survey.save_to_db()

        return make_response(jsonify({
            "id": survey.id,
            "title": survey.title,
            "image_name": survey.image_name,
            "image": survey.image,
            "mime_type": survey.mime_type,
            "short_url": survey.short_url,
            "url": survey.url,
            "visits": survey.visits,
            "date_created": survey.date_created,
            "date_updated": survey.date_updated,
            "user_id": survey.user_id,
            "sections": survey.sections,
        }), HTTP_201_CREATED)

    @jwt_required()
    def get(self):

        current_user = get_jwt_identity()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        surveys = Survey.query.filter_by(
            user_id=current_user).paginate(page=page, per_page=per_page)

        if not surveys:
            return {
                "message": "Items not found"
            }, HTTP_204_NO_CONTENT

        data = []

        for survey in surveys.items:
            data.append({
                "id": survey.id,
                "title": survey.title,
                "image_name": survey.image_name,
                "image": survey.image,
                "mime_type": survey.mime_type,
                "short_url": survey.short_url,
                "url": survey.url,
                "visits": survey.visits,
                "date_created": survey.date_created,
                "date_updated": survey.date_updated,
                "user_id": survey.user_id,
                "sections": survey.sections,
            })

        meta = {
            "page": surveys.page,
            "pages": surveys.pages,
            "total_count": surveys.total,
            "prev_page": surveys.prev_num,
            "next_page": surveys.next_num,
            "has_prev": surveys.has_prev,
            "has_next": surveys.has_next
        }

        return make_response(jsonify({
            "data": data,
            "meta": meta
        }), HTTP_200_OK)

# URL PUBLICA DE UNA ENCUESTA


class GetUrlApi(Resource):
    @jwt_required(optional=True)
    def get(self, url):

        base_url = ("http://localhost:5000/s/" if os.environ.get("FLASK_ENV")
                    == "development" else "https://surveys-api-rest.herokuapp.com/s/")
        public_url = base_url + url
        survey = Survey.query.filter_by(url=public_url).first()

        if not survey:
            return {
                "error": "Item not found"
            }, HTTP_404_NOT_FOUND

        return make_response(jsonify({
            "id": survey.id,
            "title": survey.title,
            "image_name": survey.image_name,
            "image": survey.image,
            "mime_type": survey.mime_type,
            "short_url": survey.short_url,
            "url": survey.url,
            "visits": survey.visits,
            "date_created": survey.date_created,
            "date_updated": survey.date_updated,
            "user_id": survey.user_id,
            "sections": survey.sections,
        }), HTTP_200_OK)


class RedirectToUrlApi(Resource):
    def get(self, short_url):
        survey = Survey.query.filter_by(short_url=short_url).first_or_404()
        if survey:
            survey.visits = survey.visits+1
            db.session.commit()
            return redirect(survey.url)

# OBTENER UNA ENCUESTA


class GetSurveyApi(Resource):
    @jwt_required()
    def get(self, id):
        current_user = get_jwt_identity()

        survey = Survey.query.filter_by(user_id=current_user, id=id).first()

        if not survey:
            return {
                "error": "Item not found"
            }, HTTP_404_NOT_FOUND

        return make_response(jsonify({
            "id": survey.id,
            "title": survey.title,
            "image_name": survey.image_name,
            "image": survey.image,
            "mime_type": survey.mime_type,
            "short_url": survey.short_url,
            "url": survey.url,
            "visits": survey.visits,
            "date_created": survey.date_created,
            "date_updated": survey.date_updated,
            "user_id": survey.user_id,
            "sections": survey.sections,
        }), HTTP_200_OK)

# ACTUALIZAR ENCUESTA


class UpdateSurveyApi(Resource):
    @jwt_required()
    def put(self, id):

        current_user = get_jwt_identity()
        survey = Survey.query.filter_by(user_id=current_user, id=id).first()

        if not survey:
            return {
                "error": "Item not found"
            }, HTTP_404_NOT_FOUND

        title = request.json.get('title')
        image = request.json.get('image')
        url = request.json.get('url')

        if not title:
            return {
                "error": "Title is required"
            }, HTTP_400_BAD_REQUEST

        if not image:
            return {
                "error": "Image is required"
            }, HTTP_400_BAD_REQUEST

        base_url = ("http://localhost:5000/s/" if os.environ.get("FLASK_ENV")
                    == "development" else "https://surveys-api-rest.herokuapp.com/s/")
        public_url = base_url + url

        survey.title = title
        survey.image = image
        survey.url = public_url

        db.session.commit()

        return make_response(jsonify({
            "id": survey.id,
            "title": survey.title,
            "image_name": survey.image_name,
            "image": survey.image,
            "mime_type": survey.mime_type,
            "short_url": survey.short_url,
            "url": survey.url,
            "visits": survey.visits,
            "date_created": survey.date_created,
            "date_updated": survey.date_updated,
            "user_id": survey.user_id,
            "sections": survey.sections,
        }), HTTP_200_OK)

# ELIMINAR ENCUESTA


class DeleteSurveyApi(Resource):
    @jwt_required()
    def delete(self, id):

        current_user = get_jwt_identity()
        survey = Survey.query.filter_by(user_id=current_user, id=id).first()

        if not survey:
            return jsonify({
                "error": "Item not found"
            }), HTTP_404_NOT_FOUND

        db.session.delete(survey)
        db.session.commit()

        return jsonify({}), HTTP_204_NO_CONTENT

# ESTADISTICAS DE LA ENCUESTA


class StatsApi(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        data = []

        items = Survey.query.filter_by(user_id=current_user).all()

        for item in items:
            new_link = {
                "visits": item.visits,
                "short_url": item.short_url,
                "url": item.url,
                "id": item.id,
                "sections": item.sections
            }
            data.append(new_link)

        return make_response(jsonify({"data": data}), HTTP_200_OK)
