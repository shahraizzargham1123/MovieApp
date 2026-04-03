from app import app
from models.movie_model import db
from models.user_model import User


def register(client, username="testuser", email="test@test.com", password="pass123"):
    return client.post("/auth/register", json={
        "username": username, "email": email, "password": password
    })


def login(client, email="test@test.com", password="pass123"):
    return client.post("/auth/login", json={"email": email, "password": password})


def test_register_success(client):
    res = register(client)
    assert res.status_code == 200
    assert b"registered" in res.data


def test_register_missing_fields(client):
    res = client.post("/auth/register", json={"username": "x"})
    assert res.status_code == 400


def test_register_duplicate_email(client):
    register(client)
    res = register(client, username="other")
    assert res.status_code == 400
    assert b"already registered" in res.data


def test_login_success(client):
    register(client)
    res = login(client)
    assert res.status_code == 200
    assert b"Login successful" in res.data


def test_login_wrong_password(client):
    register(client)
    res = login(client, password="wrongpass")
    assert res.status_code == 401


def test_login_unknown_email(client):
    res = login(client, email="nobody@test.com")
    assert res.status_code == 401


def test_login_deactivated_account(client):
    register(client)
    with app.app_context():
        user = User.query.filter_by(email="test@test.com").first()
        user.is_active = False
        db.session.commit()
    res = login(client)
    assert res.status_code == 403


def test_logout(client):
    register(client)
    login(client)
    res = client.post("/auth/logout")
    assert res.status_code == 200
    assert b"Logged out" in res.data
