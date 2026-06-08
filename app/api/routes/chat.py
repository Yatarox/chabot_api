from flask import Blueprint, request, jsonify
from app.core.model import Data
from app.services.model_services import ModelService
from app.core.config import Config
chat_router = Blueprint("chat_router", __name__)

ConfigInstance = Config()
ModelServiceInstance = ModelService(config=ConfigInstance)

@chat_router.route("/health", methods=["GET"])
def health():
    is_healthy = ModelServiceInstance.health_check()
    if is_healthy:
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "unhealthy"}), 503
    

@chat_router.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json() or {}
        data_obj = Data(**data)
        user_msg = data_obj.message
    except Exception as e:
        return jsonify({"error": "Invalid input", "details": str(e)}), 400
    try:
        if not user_msg:
            raise ValueError("Message field is required.")
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    
    try:
        ModelResponse = ModelServiceInstance.generate_response(prompt=user_msg)
        return jsonify({"response": ModelResponse})
    except Exception as e:
        return jsonify({"error": "Failed to generate response", "details": str(e)}), 500
