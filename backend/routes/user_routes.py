from flask import Blueprint, jsonify, session
from models.user_model import User

user_bp = Blueprint("user", __name__)

@user_bp.route("/me")
def get_my_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.get(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email})