from app import app
from models.movie_model import db


def login_user(client, email="user@test.com", username="watcher"):
    client.post("/auth/register", json={
        "username": username, "email": email, "password": "pass123"
    })
    client.post("/auth/login", json={"email": email, "password": "pass123"})


MOVIE = {"tmdb_id": 550, "title": "Fight Club", "poster_path": "/path.jpg"}


def test_add_to_watchlist(client):
    login_user(client)
    res = client.post("/watchlist/add", json=MOVIE)
    assert res.status_code == 201
    assert b"Added to watchlist" in res.data


def test_add_duplicate_to_watchlist(client):
    login_user(client)
    client.post("/watchlist/add", json=MOVIE)
    res = client.post("/watchlist/add", json=MOVIE)
    assert res.status_code == 409


def test_get_watchlist(client):
    login_user(client)
    client.post("/watchlist/add", json=MOVIE)
    res = client.get("/watchlist/")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Fight Club"


def test_remove_from_watchlist(client):
    login_user(client)
    client.post("/watchlist/add", json=MOVIE)
    res = client.delete("/watchlist/remove/550")
    assert res.status_code == 200
    assert b"Removed from watchlist" in res.data


def test_remove_nonexistent_from_watchlist(client):
    login_user(client)
    res = client.delete("/watchlist/remove/999")
    assert res.status_code == 404


def test_watchlist_requires_login(client):
    res = client.get("/watchlist/")
    assert res.status_code == 401


def test_add_watchlist_requires_login(client):
    res = client.post("/watchlist/add", json=MOVIE)
    assert res.status_code == 401
