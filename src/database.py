# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


# class User(db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.Text(), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utc_now())
#     updated_at = db.Column(db.DateTime, onupdate=datetime.utc_now())

#     def __repr__(self) -> str:
#         return 'User>> {self.username}'

# class Survey(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Integer)
#     url = db.Column(db.Integer)
#     short_url = db.Column(db.String(3))
#     visits = db.Column(db.Integer, default=0)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))