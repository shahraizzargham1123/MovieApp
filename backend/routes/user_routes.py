from flask import Blueprint, jsonify, request, session
from models.movie_model import db, Movie
from models.user_model import User
from models.review_model import Review
from services import tmdb_service

user_bp = Blueprint("user", __name__)


@user_bp.route("/me")
def get_my_profile():
    """
    Get current user profile
    ---
    tags:
      - User
    responses:
      200:
        description: Current user details
      401:
        description: Not logged in
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.get(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email, "is_admin": user.is_admin})


@user_bp.route("/reviews", methods=["POST"])
def create_review():
    """
    Submit a review for a movie
    ---
    tags:
      - User
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [movie_id]
          properties:
            movie_id:
              type: integer
              example: 550
            rating:
              type: integer
              minimum: 1
              maximum: 5
              example: 4
            comment:
              type: string
              example: Great movie!
    responses:
      201:
        description: Review created
      400:
        description: Invalid input
      401:
        description: Not logged in
      409:
        description: Already reviewed this movie
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    if not data or not data.get("movie_id"):
        return jsonify({"error": "movie_id is required"}), 400

    rating = data.get("rating")
    if rating is not None and not (1 <= int(rating) <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    tmdb_id = int(data["movie_id"])

    movie = Movie.query.filter_by(tmdb_id=tmdb_id).first()
    if not movie:
        details = tmdb_service.get_movie_details(tmdb_id)
        movie = Movie(
            tmdb_id=tmdb_id,
            title=details.get("title", ""),
            overview=details.get("overview"),
            release_date=details.get("release_date"),
            poster_path=details.get("poster_path")
        )
        db.session.add(movie)
        db.session.flush()

    existing = Review.query.filter_by(user_id=user_id, movie_id=movie.id).first()
    if existing:
        return jsonify({"error": "You already reviewed this movie"}), 409

    review = Review(
        user_id=user_id,
        movie_id=movie.id,
        rating=rating,
        comment=data.get("comment")
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review created", "id": review.id}), 201


@user_bp.route("/reviews/<int:review_id>", methods=["PUT"])
def update_review(review_id):
    """
    Update a review
    ---
    tags:
      - User
    parameters:
      - name: review_id
        in: path
        required: true
        type: integer
      - in: body
        name: body
        schema:
          type: object
          properties:
            rating:
              type: integer
              minimum: 1
              maximum: 5
              example: 5
            comment:
              type: string
              example: Updated thoughts
    responses:
      200:
        description: Review updated
      401:
        description: Not logged in
      404:
        description: Review not found
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    review = Review.query.get(review_id)
    if not review or review.user_id != user_id:
        return jsonify({"error": "Review not found"}), 404

    data = request.json
    if "rating" in data and data["rating"] is not None:
        if not (1 <= int(data["rating"]) <= 5):
            return jsonify({"error": "Rating must be between 1 and 5"}), 400
        review.rating = data["rating"]
    if "comment" in data:
        review.comment = data["comment"]

    db.session.commit()
    return jsonify({"message": "Review updated"})


@user_bp.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    """
    Delete a review
    ---
    tags:
      - User
    parameters:
      - name: review_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Review deleted
      401:
        description: Not logged in
      404:
        description: Review not found
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    review = Review.query.get(review_id)
    if not review or review.user_id != user_id:
        return jsonify({"error": "Review not found"}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"})
