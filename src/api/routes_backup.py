"""
API 路由定義
"""

from flask import Flask, request, jsonify
from typing import Dict, Any
import traceback

from .dependencies import get_dependencies
from ..models.conversation import MessageRole
from ..exceptions import ClinicSimError, CaseNotFoundError, AIServiceError
from ..utils.validation import validate_conversation_data
from ..utils.json_serializer import safe_model_dump, safe_jsonify_data


def create_app() -> Flask:
    """創建 Flask 應用程式"""
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    
    # 設定錯誤處理器
    setup_error_handlers(app)
    
    # 註冊路由
    register_routes(app)
    
    return app


def register_routes(app: Flask) -> None:
    """註冊所有路由"""
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """健康檢查端點"""
        return jsonify({
            "status": "healthy",
            "service": "ClinicSim-AI",
            "version": "2.0.0"
        })


def setup_error_handlers(app: Flask) -> None:
    """設定錯誤處理器"""
    
    @app.errorhandler(ClinicSimError)
    def handle_clinic_sim_error(error):
        return jsonify({"error": str(error)}), 400
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "端點未找到"}), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"error": "方法不允許"}), 405
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        app.logger.error(f"內部錯誤: {traceback.format_exc()}")
        return jsonify({"error": "內部伺服器錯誤"}), 500
