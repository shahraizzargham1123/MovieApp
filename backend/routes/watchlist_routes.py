from flask import Blueprint, jsonify, request, session
from models.movie_model import db
from models.watchlist_model import Watchlist

watchlist_bp = Blueprint("watchlist", __name__)


@watchlist_bp.route("/", methods=["GET"])
def get_watchlist():
    """
    Get current user's watchlist
    ---
    tags: [Watchlist]
    responses:
      200: {description: List of watchlist items}
      401: {description: Not logged in}
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    items = Watchlist.query.filter_by(user_id=user_id).order_by(Watchlist.added_at.desc()).all()
    return jsonify([
        {
            "id": item.id,
            "tmdb_id": item.tmdb_id,
            "title": item.title,
            "poster_path": item.poster_path,
            "added_at": item.added_at.isoformat()
        }
        for item in items
    ])


@watchlist_bp.route("/add", methods=["POST"])
def add_to_watchlist():
    """
    Add a movie to the watchlist
    ---
    tags: [Watchlist]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [tmdb_id, title]
            properties:
              tmdb_id:     {type: integer}
              title:       {type: string}
              poster_path: {type: string}
    responses:
      201: {description: Added to watchlist}
      400: {description: Missing required fields}
      401: {description: Not logged in}
      409: {description: Movie already in watchlist}
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    if not data or not data.get("tmdb_id") or not data.get("title"):
        return jsonify({"error": "tmdb_id and title are required"}), 400

    existing = Watchlist.query.filter_by(user_id=user_id, tmdb_id=data["tmdb_id"]).first()
    if existing:
        return jsonify({"error": "Movie already in watchlist"}), 409

    item = Watchlist(
        user_id=user_id,
        tmdb_id=data["tmdb_id"],
        title=data["title"],
        poster_path=data.get("poster_path")
    )
    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Added to watchlist", "tmdb_id": item.tmdb_id}), 201


@watchlist_bp.route("/remove/<int:tmdb_id>", methods=["DELETE"])
def remove_from_watchlist(tmdb_id):
    """
    Remove a movie from the watchlist
    ---
    tags: [Watchlist]
    parameters:
      - name: tmdb_id
        in: path
        required: true
        schema: {type: integer}
    responses:
      200: {description: Removed from watchlist}
      401: {description: Not logged in}
      404: {description: Movie not in watchlist}
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    item = Watchlist.query.filter_by(user_id=user_id, tmdb_id=tmdb_id).first()
    if not item:
        return jsonify({"error": "Movie not in watchlist"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Removed from watchlist"})
