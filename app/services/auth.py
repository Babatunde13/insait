from flask_jwt_extended import create_access_token
from datetime import timedelta, datetime
from app.models import User
from app.extensions import db

class AuthService:
    @staticmethod
    def generate_token(user_id):
        return create_access_token(identity=str(user_id), expires_delta=timedelta(days=1))

    @staticmethod
    def register_user(username, password):
        if User.query.filter_by(username=username).first():
            return {"error": "User already exists"}

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully", "data": {} }

    @staticmethod
    def authenticate_user(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return { "error": "Invalid credentials" }

        token = AuthService.generate_token(user.id)
        return {
            "data": {"access_token": token},
            "message": "User authenticated successfully"
        }
