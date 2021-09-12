from datetime import datetime
from typing import List
from src import db, ma


class User(db.Model):
    # user model for storing user info
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin

    @classmethod
    def find_by_id(self, _id) -> "User":
        return self.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(self, _email) -> "User":
        return self.query.filter_by(email=_email).first()

    @classmethod
    def find_by_username(self, _username) -> "User":
        return self.query.filter_by(username=_username).first()

    @classmethod
    def find_all(self) -> List["User"]:
        return self.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    username = ma.auto_field()
    email = ma.auto_field()
