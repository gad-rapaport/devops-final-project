import pytest
import os
from app import create_app, db as _db

TEST_DB_URL = os.getenv(
    "TEST_DATABASE_URL",
    "mysql+pymysql://smartrecipe:smartrecipe@localhost:3307/smartrecipe_test",
)


@pytest.fixture(scope="session")
def app():
    application = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DB_URL,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        yield _db
        _db.session.rollback()
