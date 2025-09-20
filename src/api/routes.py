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
    
    @app.route('/ask_patient', methods=['POST'])
    def ask_patient_route():
        """詢問病人端點"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "缺少請求數據"}), 400
            
            history = data.get('history', [])
            case_id = data.get('case_id')
            
            if not case_id:
                return jsonify({"error": "缺少 case_id"}), 400
            
            if not validate_conversation_data(history):
                return jsonify({"error": "無效的對話數據格式"}), 400
            
            # 取得服務依賴
            deps = get_dependencies()
            conversation_service = deps['conversation_service']
            
            # 創建或取得對話
            conversation_id = f"{case_id}_session"
            conversation = conversation_service.get_conversation(conversation_id)
            
            if not conversation:
                conversation, conversation_id = conversation_service.create_conversation(case_id)
            
            # 添加使用者訊息
            last_user_message = history[-1] if history else None
            if last_user_message and last_user_message.get('role') == 'user':
                conversation_service.add_message(
                    conversation_id, 
                    MessageRole.USER, 
                    last_user_message['content']
                )
            
            # 生成 AI 回應
            print(f"[DEBUG] 開始生成 AI 回應，conversation_id: {conversation_id}")
            ai_reply = conversation_service.generate_ai_response(conversation_id)
            print(f"[DEBUG] AI 回應結果: {ai_reply}")
            
            if not ai_reply:
                return jsonify({"error": "無法生成 AI 回應"}), 500
            
            # 取得更新後的對話
            updated_conversation = conversation_service.get_conversation(conversation_id)
            
            return jsonify({
                "reply": ai_reply,
                "coverage": updated_conversation.coverage if updated_conversation else 0,
                "vital_signs": updated_conversation.vital_signs if updated_conversation else None
            })
            
        except CaseNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except AIServiceError as e:
            return jsonify({"error": f"AI 服務錯誤: {str(e)}"}), 503
        except Exception as e:
            app.logger.error(f"ask_patient 錯誤: {traceback.format_exc()}")
            return jsonify({"error": f"內部伺服器錯誤: {str(e)}"}), 500
    
    @app.route('/get_feedback_report', methods=['POST'])
    def get_feedback_report_route():
        """生成即時回饋報告端點"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "缺少請求數據"}), 400
            
            full_conversation = data.get('full_conversation', [])
            case_id = data.get('case_id')
            
            if not case_id:
                return jsonify({"error": "缺少 case_id"}), 400
            
            if not validate_conversation_data(full_conversation):
                return jsonify({"error": "無效的對話數據格式"}), 400
            
            # 取得服務依賴
            deps = get_dependencies()
            conversation_service = deps['conversation_service']
            report_service = deps['report_service']
            
            # 創建對話對象
            conversation, conversation_id = conversation_service.create_conversation(case_id)
            
            # 添加對話歷史
            for msg in full_conversation:
                role = MessageRole(msg['role'])
                conversation_service.add_message(conversation_id, role, msg['content'])
            
            # 取得對話對象
            conversation = conversation_service.get_conversation(conversation_id)
            if not conversation:
                print(f"[DEBUG] 無法取得對話，conversation_id: {conversation_id}")
                print(f"[DEBUG] 可用對話: {list(conversation_service._conversations.keys())}")
                return jsonify({"error": "無法創建對話"}), 500
            
            # 生成報告
            print(f"[DEBUG] 開始生成報告，conversation_id: {conversation_id}")
            report = report_service.generate_feedback_report(conversation)
            print(f"[DEBUG] 報告生成完成")
            
            return jsonify({
                "report_text": report.content,
                "coverage": report.coverage,
                "metadata": report.metadata
            })
            
        except CaseNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            app.logger.error(f"get_feedback_report 錯誤: {traceback.format_exc()}")
            print(f"[ERROR] get_feedback_report 錯誤: {e}")
            print(f"[ERROR] 詳細錯誤: {traceback.format_exc()}")
            return jsonify({"error": f"內部伺服器錯誤: {str(e)}"}), 500
    
    @app.route('/get_detailed_report', methods=['POST'])
    def get_detailed_report_route():
        """生成詳細報告端點"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "缺少請求數據"}), 400
            
            full_conversation = data.get('full_conversation', [])
            case_id = data.get('case_id')
            
            if not case_id:
                return jsonify({"error": "缺少 case_id"}), 400
            
            if not validate_conversation_data(full_conversation):
                return jsonify({"error": "無效的對話數據格式"}), 400
            
            # 取得服務依賴
            deps = get_dependencies()
            conversation_service = deps['conversation_service']
            report_service = deps['report_service']
            
            # 創建對話對象
            conversation, conversation_id = conversation_service.create_conversation(case_id)
            
            # 添加對話歷史
            for msg in full_conversation:
                role = MessageRole(msg['role'])
                conversation_service.add_message(conversation_id, role, msg['content'])
            
            # 取得對話對象
            conversation = conversation_service.get_conversation(conversation_id)
            if not conversation:
                return jsonify({"error": "無法創建對話"}), 500
            
            # 生成詳細報告
            report = report_service.generate_detailed_report(conversation)
            
            return jsonify({
                "report_text": report.content,
                "citations": [citation.model_dump() for citation in report.citations],
                "rag_queries": report.rag_queries,
                "coverage": report.coverage,
                "metadata": report.metadata
            })
            
        except CaseNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            app.logger.error(f"get_detailed_report 錯誤: {traceback.format_exc()}")
            return jsonify({"error": "內部伺服器錯誤"}), 500
    
    @app.route('/cases', methods=['GET'])
    def list_cases_route():
        """列出所有可用案例"""
        try:
            deps = get_dependencies()
            case_service = deps['case_service']
            
            cases = case_service.list_available_cases()
            
            return jsonify({
                "cases": cases,
                "count": len(cases)
            })
            
        except Exception as e:
            app.logger.error(f"list_cases 錯誤: {traceback.format_exc()}")
            return jsonify({"error": "內部伺服器錯誤"}), 500
    
    @app.route('/cases/<case_id>', methods=['GET'])
    def get_case_route(case_id: str):
        """取得特定案例資訊"""
        try:
            deps = get_dependencies()
            case_service = deps['case_service']
            
            case = case_service.get_case(case_id)
            if not case:
                return jsonify({"error": f"案例未找到: {case_id}"}), 404
            
            return jsonify({
                "case_id": case.data.case_id,
                "case_title": case.data.case_title,
                "station_info": case.data.station_info,
                "patient_profile": case.data.patient_profile.model_dump()
            })
            
        except Exception as e:
            app.logger.error(f"get_case 錯誤: {traceback.format_exc()}")
            return jsonify({"error": "內部伺服器錯誤"}), 500
    
    @app.route('/rag/status', methods=['GET'])
    def rag_status_route():
        """RAG 服務狀態檢查"""
        try:
            deps = get_dependencies()
            rag_service = deps['rag_service']
            
            status_info = rag_service.get_index_info()
            
            return jsonify(status_info)
            
        except Exception as e:
            app.logger.error(f"rag_status 錯誤: {traceback.format_exc()}")
            return jsonify({"error": "內部伺服器錯誤"}), 500


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
