from src import db, ma


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    comment = db.Column(db.String(500), nullable=False)

    def __init__(self, id, name, email, comment) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.comment = comment

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()


class FeedbackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feedback
