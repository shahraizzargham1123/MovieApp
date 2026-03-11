from flask import Flask
from flask_cors import CORS
from config import Config
from models.movie_model import db
from routes.movie_routes import movies_bp
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

app.register_blueprint(movies_bp, url_prefix="/movies")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(admin_bp, url_prefix="/admin")

@app.route("/")
def home():
    return {"message": "Movie Recommendation API Running"}

if __name__ == "__main__":
    app.run(debug=True)