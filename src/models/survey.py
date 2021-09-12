from datetime import datetime
import string
import random
from src import db, ma


class Survey(db.Model):
    __tablename__ = "survey"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    image_name = db.Column(db.String(255))
    mime_type = db.Column(db.String(20), default="*")
    short_url = db.Column(db.String(10), unique=True)
    url = db.Column(db.String(120), unique=True)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship("User", backref='surveys')

    def generate_short_characters(self):
        characters = string.digits+string.ascii_letters
        picked_chars = ''.join(random.choices(characters, k=5))

        record_exists = self.query.filter_by(short_url=picked_chars).first()

        if record_exists:
            self.generate_short_characters()
        else:
            return picked_chars

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def __init__(self, title, image, url, user_id):
        self.title = title
        self.image = image
        self.short_url = self.generate_short_characters()
        self.url = url
        self.user_id = user_id


class SurveySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Survey
        include_fk = True
