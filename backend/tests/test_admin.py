from app import app
from models.movie_model import db
from models.user_model import User


def create_admin(client):
    client.post("/auth/register", json={
        "username": "admin", "email": "admin@test.com", "password": "adminpass"
    })
    with app.app_context():
        user = User.query.filter_by(email="admin@test.com").first()
        user.is_admin = True
        db.session.commit()
    client.post("/auth/login", json={"email": "admin@test.com", "password": "adminpass"})


def create_regular_user(client):
    client.post("/auth/register", json={
        "username": "regular", "email": "regular@test.com", "password": "pass123"
    })
    with app.app_context():
        return User.query.filter_by(email="regular@test.com").first().id


def test_admin_can_get_users(client):
    create_admin(client)
    create_regular_user(client)
    res = client.get("/admin/users")
    assert res.status_code == 200
    data = res.get_json()
    assert any(u["username"] == "regular" for u in data)


def test_non_admin_cannot_get_users(client):
    client.post("/auth/register", json={
        "username": "user", "email": "user@test.com", "password": "pass"
    })
    client.post("/auth/login", json={"email": "user@test.com", "password": "pass"})
    res = client.get("/admin/users")
    assert res.status_code == 403


def test_unauthenticated_cannot_access_admin(client):
    res = client.get("/admin/users")
    assert res.status_code == 401


def test_admin_deactivate_user(client):
    create_admin(client)
    user_id = create_regular_user(client)
    res = client.put(f"/admin/users/{user_id}/deactivate")
    assert res.status_code == 200
    with app.app_context():
        user = User.query.get(user_id)
        assert user.is_active is False


def test_admin_activate_user(client):
    create_admin(client)
    user_id = create_regular_user(client)
    client.put(f"/admin/users/{user_id}/deactivate")
    res = client.put(f"/admin/users/{user_id}/activate")
    assert res.status_code == 200
    with app.app_context():
        user = User.query.get(user_id)
        assert user.is_active is True


def test_admin_does_not_appear_in_user_list(client):
    create_admin(client)
    res = client.get("/admin/users")
    data = res.get_json()
    assert all(u["username"] != "admin" for u in data)
