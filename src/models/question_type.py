from sqlalchemy import event, DDL
from src import db, ma


class QuestionType(db.Model):
    __tablename__ = "question_type"
    id = db.Column(db.Integer, primary_key=True)
    type_text = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, id, type_text) -> None:
        self.id = id
        self.type_text = type_text


# @event.listens_for(QuestionType.__table__, 'after_create')
# def create_question_types(*args, **kwargs):
#     db.session.add(QuestionType(type_text='Abierta'))
#     db.session.add(QuestionType(type_text='Cerrada'))
#     db.session.add(QuestionType(type_text='Multiple'))
#     db.session.commit()
event.listen(QuestionType.__table__, 'after_create',
             DDL(""" INSERT INTO question_type (id, type_text) VALUES (1, 'Abierta'), (2, 'Cerrada'), (3, 'Multiple') """))


class QuestionTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuestionType
        include_fk = True
