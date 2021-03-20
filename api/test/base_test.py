from unittest import TestCase
from api import app, db

class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_db.db"
        app.testing = True

        with app.app_context():
            db.init_app(app)

    def setUp(self):

        # Create all tables
        with app.app_context():
            db.create_all()

        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Remove everything from DB
        with app.app_context():
            db.session.remove()
            db.drop_all()

