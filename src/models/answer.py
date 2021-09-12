from datetime import datetime
from src import db, ma


class Answer(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True)
    text_answer = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    question_id = db.Column(db.Integer, db.ForeignKey(
        "question.id"), nullable=False)

    question = db.relationship("Question", backref="answers")

    def __init__(self, id, text_answer, question_id):
        self.id = id
        self.text_answer = text_answer
        self.question_id = question_id


class AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
        include_fk = True
