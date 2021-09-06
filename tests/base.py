# src/test/base.py

from flask_testing import TestCase
from server import app, db

class BaseTestCase(TestCase):
    
    def create_app(self):
        app.config.from_object('api.server.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()