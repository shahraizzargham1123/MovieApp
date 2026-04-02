from flask import Blueprint, jsonify, request
from services import tmdb_service
from models.review_model import Review

movies_bp = Blueprint("movies", __name__)

@movies_bp.route("/popular")
def popular_movies():
    page = request.args.get("page", 1, type=int)
    data = tmdb_service.get_popular_movies(page)
    return jsonify(data)

@movies_bp.route("/search")
def search_movies():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    data = tmdb_service.search_movies(query)
    return jsonify(data)

@movies_bp.route("/<int:movie_id>")
def movie_details(movie_id):
    data = tmdb_service.get_movie_details(movie_id)
    return jsonify(data)

@movies_bp.route("/<int:movie_id>/recommendations")
def movie_recommendations(movie_id):
    data = tmdb_service.get_movie_recommendations(movie_id)
    return jsonify(data)


@movies_bp.route("/<int:movie_id>/reviews")
def movie_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).order_by(Review.created_at.desc()).all()
    return jsonify([
        {
            "id": r.id,
            "user_id": r.user_id,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at.isoformat()
        }
        for r in reviews
    ])