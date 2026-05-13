from flask import Blueprint, request, jsonify

from extensions import db

from models.user import User

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from datetime import timedelta

from utils.validators import validate_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not all([full_name, email, password, confirm_password]):
        return jsonify({
            "message": "All fields are required"
        }), 400

    if not validate_email(email):
        return jsonify({
            "message": "Invalid email format"
        }), 400

    if len(password) < 8:
        return jsonify({
            "message": "Password must be at least 8 characters"
        }), 400

    if password != confirm_password:
        return jsonify({
            "message": "Passwords do not match"
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "Account already exists"
        }), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        full_name=full_name,
        email=email,
        password_hash=hashed_password
    )

    db.session.add(new_user)

    db.session.commit()

    return jsonify({
        "message": "Signup successful"
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    remember_me = data.get("remember_me", False)

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    expiry = timedelta(days=30) if remember_me else timedelta(hours=2)

    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=expiry
    )

    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email
        }
    }), 200


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if user:

        reset_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=1)
        )

        reset_link = f"http://127.0.0.1:3000/qatar-foundation-admin-portal/sky/admin.html?reset_token={reset_token}"

        print("\nRESET LINK:")
        print(reset_link)
        print()

    return jsonify({
        "message": "If the email exists, a reset link has been generated."
    }), 200


@auth_bp.route("/reset-password", methods=["POST"])
@jwt_required()
def reset_password():

    user_id = get_jwt_identity()

    data = request.get_json()

    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not password or not confirm_password:
        return jsonify({
            "message": "All fields required"
        }), 400

    if len(password) < 8:
        return jsonify({
            "message": "Password must be at least 8 characters"
        }), 400

    if password != confirm_password:
        return jsonify({
            "message": "Passwords do not match"
        }), 400

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    user.password_hash = generate_password_hash(password)

    db.session.commit()

    return jsonify({
        "message": "Password reset successful"
    }), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    return jsonify({
        "message": "Logout successful"
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify({
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email
    })