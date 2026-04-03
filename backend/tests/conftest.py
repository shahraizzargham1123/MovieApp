import os
import sys

# Must be set BEFORE app.py is imported so the engine uses SQLite
os.environ["DATABASE_URL_OVERRIDE"] = "sqlite:///:memory:"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
