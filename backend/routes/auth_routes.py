from flask import Blueprint, request, jsonify, session
from models.movie_model import db
from models.user_model import User

auth_bp = Blueprint("auth", __name__)

def get_bcrypt():
    from app import bcrypt
    return bcrypt

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags: [Auth]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [username, email, password]
            properties:
              username: {type: string}
              email:    {type: string}
              password: {type: string}
    responses:
      200: {description: User registered successfully}
      400: {description: Missing fields or email already registered}
    """
    data = request.json
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    bcrypt = get_bcrypt()
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(username=data["username"], email=data["email"], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": {"id": new_user.id, "username": new_user.username, "email": new_user.email}
    })

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login a user
    ---
    tags: [Auth]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [email, password]
            properties:
              email:    {type: string}
              password: {type: string}
    responses:
      200: {description: Login successful}
      401: {description: Invalid credentials}
      403: {description: Account deactivated}
    """
    data = request.json
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    bcrypt = get_bcrypt()
    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"error": "Account has been deactivated"}), 403

    session["user_id"] = user.id

    return jsonify({
        "message": "Login successful",
        "user": {"id": user.id, "username": user.username, "email": user.email, "is_admin": user.is_admin}
    })

@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Logout the current user
    ---
    tags: [Auth]
    responses:
      200: {description: Logged out successfully}
    """
    session.pop("user_id", None)
    return jsonify({"message": "Logged out successfully"})
