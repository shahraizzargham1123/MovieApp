import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")  
    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")