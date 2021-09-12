from src import db, ma


class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    survey_id = db.Column(db.Integer, db.ForeignKey(
        'survey.id'), nullable=False)

    survey = db.relationship(
        "Survey", backref='sections')

    def __init__(self, id, body):
        self.id = id
        self.body = body


class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section
        include_fk = True
