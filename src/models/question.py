from datetime import datetime

from sqlalchemy.orm import backref
from src import db, ma


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    questionType_id = db.Column(db.Integer, db.ForeignKey(
        "question_type.id"), nullable=False)

    section_id = db.Column(db.Integer, db.ForeignKey(
        "section.id"), nullable=False)

    section = db.relationship("Section", backref="questions")

    def __init__(self, id, question_text, questionType_id, section_id) -> None:
        self.id = id
        self.question_text = question_text
        self.questionType_id = questionType_id
        self.section_id = section_id


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        include_fk = True
