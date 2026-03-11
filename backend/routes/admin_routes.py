from flask import Blueprint, jsonify
from models.user_model import User

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users")
def get_all_users():
    users = User.query.all()
    results = []
    for user in users:
        results.append({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })
    return jsonify(results)