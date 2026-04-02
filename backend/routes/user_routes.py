from flask import Blueprint, jsonify, request, session
from models.movie_model import db
from models.user_model import User
from models.review_model import Review

user_bp = Blueprint("user", __name__)


@user_bp.route("/me")
def get_my_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.get(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email, "is_admin": user.is_admin})


@user_bp.route("/reviews", methods=["POST"])
def create_review():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    if not data or not data.get("movie_id"):
        return jsonify({"error": "movie_id is required"}), 400

    rating = data.get("rating")
    if rating is not None and not (1 <= int(rating) <= 10):
        return jsonify({"error": "Rating must be between 1 and 10"}), 400

    existing = Review.query.filter_by(user_id=user_id, movie_id=data["movie_id"]).first()
    if existing:
        return jsonify({"error": "You already reviewed this movie"}), 409

    review = Review(
        user_id=user_id,
        movie_id=data["movie_id"],
        rating=rating,
        comment=data.get("comment")
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review created", "id": review.id}), 201


@user_bp.route("/reviews/<int:review_id>", methods=["PUT"])
def update_review(review_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    review = Review.query.get(review_id)
    if not review or review.user_id != user_id:
        return jsonify({"error": "Review not found"}), 404

    data = request.json
    if "rating" in data and data["rating"] is not None:
        if not (1 <= int(data["rating"]) <= 10):
            return jsonify({"error": "Rating must be between 1 and 10"}), 400
        review.rating = data["rating"]
    if "comment" in data:
        review.comment = data["comment"]

    db.session.commit()
    return jsonify({"message": "Review updated"})


@user_bp.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    review = Review.query.get(review_id)
    if not review or review.user_id != user_id:
        return jsonify({"error": "Review not found"}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"})
