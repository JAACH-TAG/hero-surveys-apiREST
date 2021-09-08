from datetime import datetime
from flask_bcrypt import Bcrypt
from sqlalchemy import event, DDL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    # user model for storing user info
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    admin = db.Column(db.Boolean, nullable=False, default=False)
    surveys = db.relationship("Survey", backref="user")


    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin
    
    # def encode_auth_token(self, user_id):
    #     # generate the auth token
    #     # return: string
    #     try:
    #         payload = {
    #             'exp': datetime.utcnow() + timedelta(days=0,seconds=5),
    #             'iat': datetime.utcnow(),
    #             'sub': user_id
    #         }
    #         return jwt.encode(
    #             payload,
    #             os.environ.get("SECRET_KEY"),
    #             algorithm='HS256'
    #         )
    #     except Exception as e:
    #         return e

#     @staticmethod
#     def decode_auth_token(auth_token):
#         "validates the auth token"
#         ":param auth_token"
#         ":return integer|string"
#         try:
#             payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
#             is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
#             if is_blacklisted_token:
#                 return 'Token blacklisted. Please log in again.'
#             else:
#                 return payload['sub']
#         except jwt.ExpiredSignatureError:
#             return 'Signature expired. Please log in again.'
#         except jwt.InvalidTokenError:
#             return 'Invalid token. Please log in again.'
        
# class BlacklistToken(db.Model):
#     # token model for storing JWT tokens
#     __tablename__ = 'blacklist_tokens'

#     id = db.Column(db.Integer, primary_key=True)
#     token = db.Column(db.String(500), unique=True, nullable=False)
#     blacklisted_on = db.Column(db.DateTime, nullable=False)

#     def __init__(self, token):
#         self.token = token
#         self.blacklisted_on = datetime.now()

#     def __repr__(self):
#         return '<id: token: {}'.format(self.token)

#     @staticmethod
#     def check_blacklist(auth_token):
#         res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
#         if res:
#             return True
#         else:
#             return False

# @event.listens_for(Survey, "before_insert")
# @event.listens_for(Survey, "before_update")
# def date_insert(mapper, connection, target):
#     target.date_updated = datetime.utcnow()


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    comment = db.Column(db.String(500), nullable=False)

class Survey(db.Model):
    __tablename__ = "survey"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))
    url = db.Column(db.String(50), nullable=False)
    visits = db.Column(db.Integer, nullable=False, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    sections = db.relationship("Section", backref="survey")


class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    survey_id = db.Column(db.Integer, db.ForeignKey("survey.id"), nullable=False)
    questions = db.relationship("Question", backref="section")

class QuestionType(db.Model):
    __tablename__ = "question_type"
    id = db.Column(db.Integer, primary_key=True)
    type_text = db.Column(db.String(50),unique=True,nullable=False)


# @event.listens_for(QuestionType.__table__, 'after_create')
# def create_question_types(*args, **kwargs):
#     db.session.add(QuestionType(type_text='Abierta'))
#     db.session.add(QuestionType(type_text='Cerrada'))
#     db.session.add(QuestionType(type_text='Multiple'))
#     db.session.commit()
event.listen(QuestionType.__table__, 'after_create',
            DDL(""" INSERT INTO question_type (id, type_text) VALUES (1, 'Abierta'), (2, 'Cerrada'), (3, 'Multiple') """))



class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    questionType_id = db.Column(db.Integer, db.ForeignKey("question_type.id"), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("section.id"), nullable=False)
    answers = db.relationship("Answer", backref="question")

class Answer(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True)
    text_answer = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)

