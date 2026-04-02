from flask import Blueprint, jsonify, session
from models.user_model import User
from models.movie_model import db
from models.review_model import Review

admin_bp = Blueprint("admin", __name__)


def admin_required():
    user_id = session.get("user_id")
    if not user_id:
        return None, jsonify({"error": "Not logged in"}), 401
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return None, jsonify({"error": "Admin access required"}), 403
    return user, None, None

@admin_bp.route("/users")
def get_all_users():
    _, err, status = admin_required()
    if err:
        return err, status

    users = User.query.filter_by(is_admin=False).all()
    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email, "is_active": u.is_active}
        for u in users
    ])


@admin_bp.route("/users/<int:user_id>/deactivate", methods=["PUT"])
def deactivate_user(user_id):
    _, err, status = admin_required()
    if err:
        return err, status

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_active = False
    db.session.commit()
    return jsonify({"message": f"{user.username} has been deactivated"})


@admin_bp.route("/users/<int:user_id>/activate", methods=["PUT"])
def activate_user(user_id):
    _, err, status = admin_required()
    if err:
        return err, status

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_active = True
    db.session.commit()
    return jsonify({"message": f"{user.username} has been activated"})


@admin_bp.route("/reviews")
def get_all_reviews():
    _, err, status = admin_required()
    if err:
        return err, status

    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return jsonify([
        {
            "id": r.id,
            "user_id": r.user_id,
            "movie_id": r.movie_id,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at.isoformat()
        }
        for r in reviews
    ])


@admin_bp.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    _, err, status = admin_required()
    if err:
        return err, status

    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"})