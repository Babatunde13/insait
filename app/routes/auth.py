from flask import Blueprint, request, jsonify
from app.services.auth import AuthService
from app.logger import Logger
from app.validation.validator import RegisterSchema, LoginSchema

auth_bp = Blueprint("auth", __name__)
logger = Logger('AuthRouter')

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    errors = RegisterSchema().validate(data)
    if errors:
        logger.error("Validation error", errors)
        return jsonify(errors), 400

    response = AuthService.register_user(data["username"], data["password"])
    if "error" in response:
        logger.error(response["error"], response)
        return jsonify(response), 400
    return jsonify(response), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    errors = LoginSchema().validate(data)
    if errors:
        logger.error("Validation error", errors)
        return jsonify(errors), 400
    response = AuthService.authenticate_user(data["username"], data["password"])
    if "error" in response:
        logger.error(response["error"], response)
        return jsonify(response), 401
    return jsonify(response)
