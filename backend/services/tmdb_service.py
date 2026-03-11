import requests
from config import Config

BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies(page=1):
    url = f"{BASE_URL}/movie/popular?api_key={Config.TMDB_API_KEY}&language=en-US&page={page}"
    return requests.get(url).json()

def search_movies(query):
    url = f"{BASE_URL}/search/movie?api_key={Config.TMDB_API_KEY}&query={query}"
    return requests.get(url).json()

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={Config.TMDB_API_KEY}&language=en-US"
    return requests.get(url).json()

def get_movie_recommendations(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/recommendations?api_key={Config.TMDB_API_KEY}&language=en-US"
    return requests.get(url).json()