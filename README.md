# Movie Web Application

A full-stack movie browsing web application built with Flask and Vanilla JavaScript, integrating the TMDB API for real time movie data.

## Team Members

- **Shahraiz Zargham** – Backend Development/API Integration and database management
- **Michael Oladapo** – Frontend Development (Vanilla JavaScript UI/UX) and Report proof reading
- **Oluwaseun** – Frontend Development (Vanilla JavaScript UI/UX) and Report writing
- **Joseph George** – Frontend Development (Vanilla JavaScript UI/UX) and Report proof reading

## Features

### User Features
- Browse popular and trending movies
- Search movies by title
- View movie details (poster, description, genre, rating)
- Similar movie recommendations ("More Like This")
- Add/remove movies to a personal watchlist
- Write, edit, and delete reviews with star ratings (1–5 stars)
- User registration, login, and logout

### Admin Features
- View all user accounts with status
- Deactivate and reactivate user accounts
- View and delete user reviews

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, Vanilla JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| External API | TMDB (The Movie Database) |
| Auth | Flask-Bcrypt, Flask sessions |
| ORM | Flask-SQLAlchemy |

## Project Structure

```
MovieApp/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models/
│   │   ├── user_model.py
│   │   ├── movie_model.py
│   │   ├── review_model.py
│   │   └── watchlist_model.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── movie_routes.py
│   │   ├── user_routes.py
│   │   ├── watchlist_routes.py
│   │   └── admin_routes.py
│   └── services/
│       └── tmdb_service.py
├── frontend/
│   ├── index.html
│   ├── auth.html
│   ├── search.html
│   ├── movie.html
│   ├── admin.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── auth.js
│       ├── search.js
│       ├── movie.js
│       └── admin.js
└── database/
    └── schema.sql
```

## Setup

### Prerequisites
- Python 3.x
- MySQL
- TMDB API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shahraizzargham1123/MovieApp.git
   cd MovieApp/backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install flask flask-sqlalchemy flask-cors flask-bcrypt pymysql python-dotenv requests flasgger
   ```

4. Create a `.env` file inside `backend/`:
   ```
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_HOST=localhost
   DB_NAME=movie_app
   SECRET_KEY=any_random_string
   TMDB_API_KEY=your_tmdb_api_key
   ```
   Get a free TMDB API key at https://www.themoviedb.org/settings/api

5. Create the database and tables in MySQL:
   ```sql
   CREATE DATABASE IF NOT EXISTS movie_app;
   USE movie_app;
   ```
   Then run the full schema:
   ```bash
   mysql -u your_mysql_username -p movie_app < database/schema.sql
   ```

6. Set the first admin manually in MySQL:
   ```sql
   UPDATE user SET is_admin = 1 WHERE email = 'your@email.com';
   ```

7. Run the backend:
   ```bash
   python app.py
   ```

8. Open the frontend:
   - Open `frontend/index.html` with a live server (e.g. VS Code Live Server extension) or any local HTTP server
   - The backend must be running on `http://127.0.0.1:5000` for the frontend to connect

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login |
| POST | `/auth/logout` | Logout |

### Movies
| Method | Endpoint | Description |
|---|---|---|
| GET | `/movies/popular` | Get popular movies |
| GET | `/movies/search?q=` | Search movies by title |
| GET | `/movies/<id>` | Get movie details |
| GET | `/movies/<id>/recommendations` | Get similar movies |
| GET | `/movies/<id>/reviews` | Get reviews for a movie |

### Watchlist
| Method | Endpoint | Description |
|---|---|---|
| GET | `/watchlist/` | Get current user's watchlist |
| POST | `/watchlist/add` | Add a movie to watchlist |
| DELETE | `/watchlist/remove/<tmdb_id>` | Remove a movie from watchlist |

### User
| Method | Endpoint | Description |
|---|---|---|
| GET | `/user/me` | Get current user profile |
| POST | `/user/reviews` | Write a review |
| PUT | `/user/reviews/<id>` | Edit a review |
| DELETE | `/user/reviews/<id>` | Delete a review |

### Admin (requires admin account)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/admin/users` | List all users |
| PUT | `/admin/users/<id>/deactivate` | Deactivate a user |
| PUT | `/admin/users/<id>/activate` | Reactivate a user |
| GET | `/admin/reviews` | View all reviews |
| DELETE | `/admin/reviews/<id>` | Delete a review |

## API Documentation

Swagger UI is available at `http://127.0.0.1:5000/apidocs` when the backend is running.

## Running Tests

```bash
cd backend
venv\Scripts\activate
pytest tests/ -v
```

All 28 unit tests cover authentication, reviews, watchlist, and admin endpoints.

## Security

- Passwords hashed with bcrypt — never stored as plain text
- TMDB API key stored server-side only, never exposed to the client
- Session-based authentication
- Role-based access control for admin endpoints
- Input validation on all user-submitted data
- Deactivated users are blocked from logging in
