from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.logger import Logger
from app.validation.validator import GenerateTextSchema
from app.services.text import TextService
from app.services.ai import ai_service

text_bp = Blueprint("text", __name__)
logger = Logger('TextRouter')

# use jwt_required_int() decorator, create a decorator that gets the id from get_jwt_identity() and convert it to an integer
# if the conversion fails, return a 401 response with a message "Invalid token"
# if the user id is valid, call the function and return the response
def jwt_required_int():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                user_id = int(get_jwt_identity())
            except ValueError:
                return jsonify({"error": "Invalid token"}), 401
            return f(user_id, *args, **kwargs)
        return wrapper
    return decorator

@text_bp.route("/generate-text", methods=["POST"])
@jwt_required()
@jwt_required_int()
def generate_text(user_id):
    data = request.get_json()
    errors = GenerateTextSchema().validate(data)
    if errors:
        logger.error("Validation error", errors)
        return jsonify(errors), 400

    prompt = data["prompt"]
    response = ai_service.generate_text(prompt)
    if not response:
        logger.error("Error generating text", {"prompt": prompt})
        return jsonify({"error": "Error generating text"}), 500

    text_record = TextService.save_generated_text(user_id, prompt, response)

    return jsonify({
        "message": "Text generated successfully",
        "data": text_record.toJSON()
    }), 201

@text_bp.route("/generated-text/<int:text_id>", methods=["GET"])
@jwt_required()
@jwt_required_int()
def get_text(user_id, text_id):
    text = TextService.get_text_by_id(text_id, user_id)

    if not text:
        logger.error("Text not found", {"text_id": text_id, "user_id": user_id})
        return jsonify({"error": "Text not found"}), 404

    return jsonify({
        "message": "Text retrieved successfully",
        "data": text.toJSON()
    }), 200

@text_bp.route("/generated-text/<int:text_id>", methods=["PUT"])
@jwt_required()
@jwt_required_int()
def update_text(user_id, text_id):
    text = TextService.get_text_by_id(text_id, user_id)
    if not text:
        logger.error("Text not found", {"text_id": text_id, "user_id": user_id})
        return jsonify({"error": "Text not found"}), 404
    response = ai_service.generate_text(text.prompt)
    updated_text = TextService.update_text(text, response)

    return jsonify({
        "message": "Text updated successfully",
        "data": updated_text.toJSON()
    }), 200

@text_bp.route("/generated-text/<int:text_id>", methods=["DELETE"])
@jwt_required()
@jwt_required_int()
def delete_text(user_id, text_id):
    if not TextService.delete_text(text_id, user_id):
        logger.error("Text not found", {"text_id": text_id, "user_id": user_id})
        return jsonify({"error": "Text not found"}), 404

    return jsonify({"message": "Text deleted successfully", "data": {}}), 200
