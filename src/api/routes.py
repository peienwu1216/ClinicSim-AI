"""
API routes definition
"""

from flask import Flask, request, jsonify
from typing import Dict, Any
import traceback
from datetime import datetime

from .dependencies import get_dependencies
from ..models.conversation import MessageRole
from ..exceptions import ClinicSimError, CaseNotFoundError, AIServiceError
from ..utils.validation import validate_conversation_data
from ..utils.json_serializer import safe_model_dump, safe_jsonify_data
from ..services.notion_service import NotionService


def create_app() -> Flask:
    """Create Flask application"""
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    
    # Setup error handlers
    setup_error_handlers(app)
    
    # Register routes
    register_routes(app)
    
    return app


def register_routes(app: Flask) -> None:
    """Register all routes"""
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "service": "ClinicSim-AI",
            "version": "2.0.0"
        })
    
    @app.route('/cases/random', methods=['GET'])
    def get_random_case():
        """Get random case endpoint"""
        try:
            # Get service dependencies
            deps = get_dependencies()
            case_service = deps['case_service']
            
            # Get random case ID
            random_case_id = case_service.get_random_case_id()
            
            if not random_case_id:
                return jsonify({"error": "No cases available"}), 404
            
            # Get case details
            case = case_service.get_case(random_case_id)
            if not case:
                return jsonify({"error": "Failed to load case"}), 500
            
            return jsonify({
                "case_id": random_case_id,
                "case_title": case.data.case_title if case.data.case_title else "未知病例",
                "description": case.data.station_info.get("description", "") if case.data.station_info else "",
                "difficulty": case.data.station_info.get("difficulty", "未知") if case.data.station_info else "未知"
            })
            
        except Exception as e:
            app.logger.error(f"get_random_case error: {traceback.format_exc()}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route('/ask_patient', methods=['POST'])
    def ask_patient_route():
        """Ask patient endpoint"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "Missing request data"}), 400
            
            history = data.get('history', [])
            case_id = data.get('case_id')
            
            if not case_id:
                return jsonify({"error": "Missing case_id"}), 400
            
            if not validate_conversation_data(history):
                return jsonify({"error": "Invalid conversation data format"}), 400
            
            # Get service dependencies
            deps = get_dependencies()
            conversation_service = deps['conversation_service']
            
            # Create or get conversation
            conversation_id = f"{case_id}_session"
            conversation = conversation_service.get_conversation(conversation_id)
            
            if not conversation:
                conversation, conversation_id = conversation_service.create_conversation(case_id)
            
            # Add user message
            last_user_message = history[-1] if history else None
            if last_user_message and last_user_message.get('role') == 'user':
                conversation_service.add_message(
                    conversation_id, 
                    MessageRole.USER, 
                    last_user_message['content']
                )
            
            # Generate AI response
            print(f"[DEBUG] Starting AI response generation, conversation_id: {conversation_id}")
            ai_reply = conversation_service.generate_ai_response(conversation_id)
            print(f"[DEBUG] AI response result: {ai_reply}")
            
            if not ai_reply:
                return jsonify({"error": "Unable to generate AI response"}), 500
            
            # Get updated conversation
            updated_conversation = conversation_service.get_conversation(conversation_id)
            
            return jsonify({
                "reply": ai_reply,
                "coverage": updated_conversation.coverage if updated_conversation else 0,
                "vital_signs": updated_conversation.vital_signs if updated_conversation else None
            })
            
        except CaseNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except AIServiceError as e:
            return jsonify({"error": f"AI service error: {str(e)}"}), 503
        except Exception as e:
            app.logger.error(f"ask_patient error: {traceback.format_exc()}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route('/get_feedback_report', methods=['POST'])
    def get_feedback_report_route():
        """Generate feedback report endpoint"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "Missing request data"}), 400
            
            full_conversation = data.get('full_conversation', [])
            case_id = data.get('case_id')
            
            if not case_id:
                return jsonify({"error": "Missing case_id"}), 400
            
            if not validate_conversation_data(full_conversation):
                return jsonify({"error": "Invalid conversation data format"}), 400
            
            # Get service dependencies
            deps = get_dependencies()
            conversation_service = deps['conversation_service']
            report_service = deps['report_service']
            
            # Create conversation object
            conversation, conversation_id = conversation_service.create_conversation(case_id)
            
            # Add conversation history
            for msg in full_conversation:
                role = MessageRole(msg['role'])
                conversation_service.add_message(conversation_id, role, msg['content'])
            
            # Get conversation object
            conversation = conversation_service.get_conversation(conversation_id)
            if not conversation:
                print(f"[DEBUG] Unable to get conversation, conversation_id: {conversation_id}")
                print(f"[DEBUG] Available conversations: {list(conversation_service._conversations.keys())}")
                return jsonify({"error": "Unable to create conversation"}), 500
            
            # Generate report
            print(f"[DEBUG] Starting report generation, conversation_id: {conversation_id}")
            report = report_service.generate_feedback_report(conversation)
            print(f"[DEBUG] Report generation completed")
            
            return jsonify({
                "report_text": report.content,
                "coverage": report.coverage,
                "metadata": report.metadata
            })
            
        except CaseNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            app.logger.error(f"get_feedback_report error: {traceback.format_exc()}")
            print(f"[ERROR] get_feedback_report error: {e}")
            print(f"[ERROR] Detailed error: {traceback.format_exc()}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route('/get_detailed_report', methods=['POST'])
    def get_detailed_report_route():
        """Generate detailed report endpoint"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "Missing request data"}), 400
            
            full_conversation = data.get('full_conversation', [])
            case_id = data.get('case_id')
            
            if not case_id:
                return jsonify({"error": "Missing case_id"}), 400
            
            if not validate_conversation_data(full_conversation):
                return jsonify({"error": "Invalid conversation data format"}), 400
            
            # Get service dependencies
            deps = get_dependencies()
            conversation_service = deps['conversation_service']
            report_service = deps['report_service']
            
            # Create conversation object
            conversation, conversation_id = conversation_service.create_conversation(case_id)
            
            # Add conversation history
            for msg in full_conversation:
                role = MessageRole(msg['role'])
                conversation_service.add_message(conversation_id, role, msg['content'])
            
            # Get conversation object
            conversation = conversation_service.get_conversation(conversation_id)
            if not conversation:
                return jsonify({"error": "Unable to create conversation"}), 500
            
            # Generate detailed report
            report = report_service.generate_detailed_report(conversation)
            
            # Use safe JSON serialization tools
            citations_data = [safe_model_dump(citation) for citation in report.citations]
            
            response_data = safe_jsonify_data({
                "report_text": report.content,
                "citations": citations_data,
                "rag_queries": report.rag_queries,
                "coverage": report.coverage,
                "metadata": report.metadata,
                "filename": report.metadata.get('filename')
            })
            
            return jsonify(response_data)
            
        except CaseNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            app.logger.error(f"get_detailed_report error: {traceback.format_exc()}")
            return jsonify({"error": "Internal server error"}), 500
    
    # Notion API routes
    @app.route('/notion/test_connection', methods=['GET'])
    def test_notion_connection():
        """Test Notion API connection"""
        try:
            notion_service = NotionService()
            
            if not notion_service.is_configured():
                return jsonify({
                    "configured": False,
                    "success": False,
                    "message": "Notion API 未配置，請先設定 API Key 和 Database ID"
                }), 400
            
            success, message = notion_service.test_connection()
            
            return jsonify({
                "configured": True,
                "success": success,
                "message": message
            })
            
        except Exception as e:
            app.logger.error(f"test_notion_connection error: {traceback.format_exc()}")
            return jsonify({
                "configured": False,
                "success": False,
                "message": f"測試連線時發生錯誤: {str(e)}"
            }), 500
    
    @app.route('/notion/export_report', methods=['POST'])
    def export_report_to_notion():
        """Export report to Notion"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "Missing request data"}), 400
            
            report_text = data.get('report_text')
            case_id = data.get('case_id')
            report_title = data.get('report_title', f"學習報告 - {case_id}")
            
            if not report_text or not case_id:
                return jsonify({"error": "Missing report_text or case_id"}), 400
            
            notion_service = NotionService()
            
            if not notion_service.is_configured():
                return jsonify({"error": "Notion API 未配置"}), 400
            
            # Create learning record
            success, message = notion_service.create_learning_record(
                report_path="",  # Not needed for direct text export
                case_data={
                    "case_id": case_id,
                    "report_title": report_title,
                    "report_content": report_text,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            if success:
                return jsonify({
                    "success": True,
                    "message": "報告已成功匯出到 Notion"
                })
            else:
                return jsonify({
                    "success": False,
                    "message": f"匯出失敗: {message}"
                }), 500
                
        except Exception as e:
            app.logger.error(f"export_report_to_notion error: {traceback.format_exc()}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route('/notion/get_learning_history', methods=['GET'])
    def get_learning_history():
        """Get learning history from Notion"""
        try:
            notion_service = NotionService()
            
            if not notion_service.is_configured():
                return jsonify({"error": "Notion API 未配置"}), 400
            
            # Get learning history
            history_data = notion_service.get_learning_history()
            
            return jsonify({
                "success": True,
                "data": history_data
            })
            
        except Exception as e:
            app.logger.error(f"get_learning_history error: {traceback.format_exc()}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route('/notion/batch_export', methods=['POST'])
    def batch_export_to_notion():
        """Batch export reports to Notion"""
        try:
            data = request.json
            if not data:
                return jsonify({"error": "Missing request data"}), 400
            
            reports = data.get('reports', [])
            
            if not reports:
                return jsonify({"error": "No reports to export"}), 400
            
            notion_service = NotionService()
            
            if not notion_service.is_configured():
                return jsonify({"error": "Notion API 未配置"}), 400
            
            results = []
            for report in reports:
                success, message = notion_service.create_learning_record(
                    report_path="",
                    case_data=report
                )
                results.append({
                    "case_id": report.get('case_id'),
                    "success": success,
                    "message": message
                })
            
            return jsonify({
                "success": True,
                "results": results
            })
            
        except Exception as e:
            app.logger.error(f"batch_export_to_notion error: {traceback.format_exc()}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500


def setup_error_handlers(app: Flask) -> None:
    """Setup error handlers"""
    
    @app.errorhandler(ClinicSimError)
    def handle_clinic_sim_error(error):
        return jsonify({"error": str(error)}), 400
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        app.logger.error(f"Internal error: {traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500
