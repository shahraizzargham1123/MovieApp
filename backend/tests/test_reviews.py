from unittest.mock import patch
from app import app
from models.movie_model import db, Movie


def setup_user_and_movie(client, email="user@test.com", username="reviewer"):
    client.post("/auth/register", json={
        "username": username, "email": email, "password": "pass123"
    })
    client.post("/auth/login", json={"email": email, "password": "pass123"})
    with app.app_context():
        movie = Movie(tmdb_id=550, title="Fight Club", overview="...",
                      release_date="1999-10-15", poster_path="/path.jpg")
        db.session.add(movie)
        db.session.commit()


MOCK_TMDB = {
    "id": 550, "title": "Fight Club", "overview": "...",
    "release_date": "1999-10-15", "poster_path": "/path.jpg"
}


def test_submit_review(client):
    setup_user_and_movie(client)
    with patch("services.tmdb_service.get_movie_details", return_value=MOCK_TMDB):
        res = client.post("/user/reviews", json={
            "movie_id": 550, "rating": 4, "comment": "Great movie!"
        })
    assert res.status_code == 201
    assert b"Review created" in res.data


def test_submit_review_not_logged_in(client):
    res = client.post("/user/reviews", json={"movie_id": 550, "rating": 3})
    assert res.status_code == 401


def test_submit_review_invalid_rating(client):
    setup_user_and_movie(client)
    with patch("services.tmdb_service.get_movie_details", return_value=MOCK_TMDB):
        res = client.post("/user/reviews", json={"movie_id": 550, "rating": 10})
    assert res.status_code == 400


def test_submit_duplicate_review(client):
    setup_user_and_movie(client)
    with patch("services.tmdb_service.get_movie_details", return_value=MOCK_TMDB):
        client.post("/user/reviews", json={"movie_id": 550, "rating": 4, "comment": "Good"})
        res = client.post("/user/reviews", json={"movie_id": 550, "rating": 3, "comment": "Again"})
    assert res.status_code == 409


def test_update_review(client):
    setup_user_and_movie(client)
    with patch("services.tmdb_service.get_movie_details", return_value=MOCK_TMDB):
        post = client.post("/user/reviews", json={"movie_id": 550, "rating": 4, "comment": "Good"})
    review_id = post.get_json()["id"]
    res = client.put(f"/user/reviews/{review_id}", json={"rating": 5, "comment": "Updated"})
    assert res.status_code == 200


def test_delete_review(client):
    setup_user_and_movie(client)
    with patch("services.tmdb_service.get_movie_details", return_value=MOCK_TMDB):
        post = client.post("/user/reviews", json={"movie_id": 550, "rating": 4, "comment": "Good"})
    review_id = post.get_json()["id"]
    res = client.delete(f"/user/reviews/{review_id}")
    assert res.status_code == 200


def test_get_reviews_for_movie(client):
    setup_user_and_movie(client)
    with patch("services.tmdb_service.get_movie_details", return_value=MOCK_TMDB):
        client.post("/user/reviews", json={"movie_id": 550, "rating": 4, "comment": "Good"})
    res = client.get("/movies/550/reviews")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["rating"] == 4
