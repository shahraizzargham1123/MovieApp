from datetime import datetime
from models.movie_model import db

class Watchlist(db.Model):
    __tablename__ = "watchlist"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tmdb_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    poster_path = db.Column(db.String(300))
    added_at = db.Column(db.DateTime, server_default=db.func.now(), default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "tmdb_id", name="unique_user_movie"),
    )
