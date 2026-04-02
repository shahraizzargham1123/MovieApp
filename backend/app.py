import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import Config
from models.movie_model import db
from routes.movie_routes import movies_bp
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp
from routes.watchlist_routes import watchlist_bp
from models.watchlist_model import Watchlist

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True, origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500"
])

bcrypt = Bcrypt(app)


load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

db.init_app(app)

app.register_blueprint(movies_bp, url_prefix="/movies")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(watchlist_bp, url_prefix="/watchlist")

@app.route("/")
def home():
    return {"message": "Movie Recommendation API Running"}

if __name__ == "__main__":
    app.run(debug=True)