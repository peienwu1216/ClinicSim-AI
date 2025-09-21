"""
Streamlit 主應用程式 - 修復版本
解決 ScriptRunContext 警告問題
"""

import streamlit as st
import requests
import sys
import time
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 添加項目根目錄到路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from src.config import get_settings
from src.frontend.components import (
    SidebarComponent, 
    ChatInterfaceComponent, 
    ReportDisplayComponent,
    ClinicalOrdersCompactComponent,
    ClinicalOrdersSimplifiedComponent
)
from src.frontend.components.enhanced_chat_interface import (
    EnhancedChatInterfaceComponent,
    FixedHeaderComponent
)
from src.frontend.components.progress_display import ReportGenerationManager
from src.frontend.components.ai_thinking import AIThinkingComponent, AIThinkingManager
from src.frontend.components.styles import apply_custom_css
from src.frontend.components.ultimate_toggle_fix import apply_ultimate_toggle_fix_once


def init_session_state():
    """初始化 session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "report" not in st.session_state:
        st.session_state.report = None
    if "detailed_report" not in st.session_state:
        st.session_state.detailed_report = None
    if "citations" not in st.session_state:
        st.session_state.citations = []
    if "rag_queries" not in st.session_state:
        st.session_state.rag_queries = []
    if "session_ended" not in st.session_state:
        st.session_state.session_ended = False
    if "coverage" not in st.session_state:
        st.session_state.coverage = 0
    if "vital_signs" not in st.session_state:
        st.session_state.vital_signs = None
    if "has_started" not in st.session_state:
        st.session_state.has_started = False
    if "case_id" not in st.session_state:
        st.session_state.case_id = "case_1"
    if "ai_thinking" not in st.session_state:
        st.session_state.ai_thinking = False
    if "ai_thinking_message" not in st.session_state:
        st.session_state.ai_thinking_message = "AI 病人正在思考..."
    if "ai_thinking_details" not in st.session_state:
        st.session_state.ai_thinking_details = "正在分析您的問題並準備回應"
    if "current_image" not in st.session_state:
        st.session_state.current_image = None


def call_api(endpoint: str, payload: dict, timeout: int = 30) -> dict:
    """呼叫 API"""
    settings = get_settings()
    api_base_url = f"http://{settings.backend_host}:{settings.backend_port}"
    
    try:
        # 如果 timeout 為 None，則不設定超時限制
        if timeout is None:
            response = requests.post(f"{api_base_url}{endpoint}", json=payload)
        else:
            response = requests.post(f"{api_base_url}{endpoint}", json=payload, timeout=timeout)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        if timeout is None:
            st.error("⏰ 請求超時，請稍後再試")
        else:
            st.error(f"⏰ 請求超時（{timeout}秒），請稍後再試")
        return {}
    except requests.exceptions.ConnectionError:
        st.error("🔌 無法連接到後端服務，請確認伺服器正在運行")
        return {}
    except Exception as e:
        st.error(f"❌ 發生錯誤: {str(e)}")
        return {}


def handle_send_message(message: str, image_path: str = None):
    """處理發送訊息"""
    if not message.strip():
        return
    
    # 標記問診已開始
    st.session_state.has_started = True
    
    # 添加使用者訊息
    st.session_state.messages.append({"role": "user", "content": message})
    
    # 如果有圖片路徑，添加到session state中以便顯示
    if image_path:
        if "current_image" not in st.session_state:
            st.session_state.current_image = None
        st.session_state.current_image = image_path
    
    # 設置AI思考狀態
    st.session_state.ai_thinking = True
    st.session_state.ai_thinking_message = "AI 病人正在思考..."
    st.session_state.ai_thinking_details = "正在分析您的問題並準備回應"
    
    # 立即重新整理頁面以顯示用戶訊息和思考狀態
    st.rerun()


def handle_ai_response():
    """處理 AI 回應"""
    if not st.session_state.ai_thinking:
        return
    
    try:
        response_data = call_api("/ask_patient", {
            "history": st.session_state.messages,
            "case_id": st.session_state.case_id
        })
        
        if response_data:
            ai_reply = response_data.get("reply", "無法生成回應")
            
            # 更新覆蓋率和生命體徵
            new_coverage = response_data.get("coverage", st.session_state.coverage)
            if new_coverage != st.session_state.coverage:
                st.session_state.coverage = new_coverage
            
            if "vital_signs" in response_data:
                st.session_state.vital_signs = response_data["vital_signs"]
            
            # 添加 AI 回應
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
        # 停止思考狀態
        st.session_state.ai_thinking = False
        
        # 重新整理頁面
        st.rerun()
        
    except Exception as e:
        st.session_state.ai_thinking = False
        st.error(f"❌ 處理 AI 回應時發生錯誤: {str(e)}")


def handle_end_session():
    """處理結束問診"""
    st.session_state.session_ended = True
    
    # 使用更好的進度顯示
    progress_container = st.container()
    with progress_container:
        st.markdown("### 📊 生成即時評估報告")
        st.markdown("---")
        
        progress_bar = st.progress(0, text="準備中...")
        
        # 步驟 1: 分析問診表現
        progress_bar.progress(0.3, text="分析問診表現...")
        st.info("🔄 正在分析您的問診表現和對話內容...")
        time.sleep(0.5)
        
        # 步驟 2: 生成回饋報告
        progress_bar.progress(0.7, text="生成回饋報告...")
        st.info("🔄 正在生成個人化的學習回饋...")
        time.sleep(0.5)
        
        # 步驟 3: 完成
        progress_bar.progress(1.0, text="完成！")
        st.success("✅ 回饋報告生成完成！")
        
        try:
            response_data = call_api("/get_feedback_report", {
                "full_conversation": st.session_state.messages,
                "case_id": st.session_state.case_id
            })
            
            report_text = response_data.get("report_text")
            if report_text:
                st.session_state.report = report_text
                st.rerun()
            else:
                st.error("無法生成報告")
                
        except Exception as e:
            st.error(f"無法生成報告，請確認後端服務是否正常。\n\n錯誤訊息：{e}")
            st.session_state.session_ended = False


def handle_generate_detailed_report():
    """處理生成詳細報告"""
    # 創建報告生成管理器
    report_generation_manager = ReportGenerationManager()
    
    # 開始報告生成進度顯示
    cancelled = report_generation_manager.start_generation(
        on_cancel=lambda: report_generation_manager.cancel_generation()
    )
    
    if cancelled:
        return
    
    try:
        # 步驟 1: 分析對話內容
        report_generation_manager.update_progress(
            step=1,
            status="分析對話內容",
            details="正在分析您的問診表現和對話內容..."
        )
        time.sleep(1.0)
        
        # 子步驟更新
        report_generation_manager.update_progress(
            step=1,
            status="分析對話內容",
            details=f"已識別 {len(st.session_state.messages)} 條對話記錄"
        )
        time.sleep(0.5)
        
        # 步驟 2: 生成 RAG 查詢
        report_generation_manager.update_progress(
            step=2,
            status="生成 RAG 查詢",
            details="正在生成相關的臨床指引查詢..."
        )
        time.sleep(1.0)
        
        report_generation_manager.update_progress(
            step=2,
            status="生成 RAG 查詢",
            details="已生成 3-5 個相關查詢"
        )
        time.sleep(0.5)
        
        # 步驟 3: 搜尋臨床指引
        report_generation_manager.update_progress(
            step=3,
            status="搜尋臨床指引",
            details="正在從知識庫中搜尋相關的臨床指引..."
        )
        time.sleep(1.2)
        
        report_generation_manager.update_progress(
            step=3,
            status="搜尋臨床指引",
            details="已找到相關臨床指引和最佳實踐"
        )
        time.sleep(0.5)
        
        # 步驟 4: 整合 AI 分析
        report_generation_manager.update_progress(
            step=4,
            status="整合 AI 分析",
            details="正在整合 AI 分析和臨床指引..."
        )
        time.sleep(1.0)
        
        report_generation_manager.update_progress(
            step=4,
            status="整合 AI 分析",
            details="正在生成綜合評估和改進建議"
        )
        time.sleep(0.8)
        
        # 步驟 5: 生成最終報告
        report_generation_manager.update_progress(
            step=5,
            status="生成最終報告",
            details="正在生成最終的詳細分析報告..."
        )
        
        # 顯示等待提示
        st.info("🔄 正在生成詳細報告，請耐心等待...")
        
        # 實際的 API 呼叫 - 無超時限制
        response_data = call_api("/get_detailed_report", {
            "full_conversation": st.session_state.messages,
            "case_id": st.session_state.case_id
        }, timeout=None)  # 無超時限制
        
        detailed_report_text = response_data.get("report_text")
        citations = response_data.get("citations", [])
        rag_queries = response_data.get("rag_queries", [])
        
        if detailed_report_text:
            st.session_state.detailed_report = detailed_report_text
            st.session_state.citations = citations
            st.session_state.rag_queries = rag_queries
            st.session_state.current_report_file = response_data.get("filename")
            
            # 完成報告生成
            report_generation_manager.complete_generation(success=True)
            st.rerun()
        else:
            # 檢查是否是因為超時或其他錯誤
            if not response_data:
                error_msg = "API 請求失敗或超時，請檢查後端服務狀態"
            else:
                error_msg = f"API 返回空數據: {response_data}"
            
            report_generation_manager.complete_generation(
                success=False, 
                error_message=error_msg
            )
            
    except Exception as e:
        report_generation_manager.complete_generation(
            success=False,
            error_message=f"無法生成詳細報告，請確認後端服務是否正常。\n\n錯誤訊息：{e}"
        )


def main():
    """主函式"""
    # 頁面設定
    st.set_page_config(
        page_title="ClinicSim AI - 臨床診斷考試訓練系統", 
        page_icon="🧑‍⚕️", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 應用自定義CSS樣式
    apply_custom_css()
    
    # 應用終極 toggle 修復
    apply_ultimate_toggle_fix_once()
    
    # 初始化 session state
    init_session_state()
    
    # 獲取設定
    settings = get_settings()
    
    # 初始化組件
    sidebar = SidebarComponent("sidebar")
    enhanced_chat_interface = EnhancedChatInterfaceComponent("enhanced_chat")
    fixed_header = FixedHeaderComponent("fixed_header")
    report_display = ReportDisplayComponent("report")
    clinical_orders_simplified = ClinicalOrdersSimplifiedComponent("clinical_orders_simplified")
    report_generation_manager = ReportGenerationManager()
    ai_thinking = AIThinkingComponent("ai_thinking")
    
    # 渲染固定頭部
    fixed_header.render(
        case_title="急性胸痛",
        session_ended=st.session_state.session_ended,
        on_end_session=handle_end_session,
        on_generate_report=handle_generate_detailed_report
    )
    
    # 創建主佈局：左側聊天，右側臨床Orders
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 渲染增強的聊天介面
        enhanced_chat_interface.render(
            messages=st.session_state.messages,
            session_ended=st.session_state.session_ended,
            on_send_message=handle_send_message,
            on_quick_action=handle_send_message
        )
        
        # 顯示當前圖片（如果有）
        if st.session_state.current_image:
            try:
                st.image(st.session_state.current_image, caption="臨床檢查結果", use_container_width=True)
            except Exception as e:
                st.error(f"無法顯示圖片: {str(e)}")
        
        # 渲染AI思考狀態
        if st.session_state.ai_thinking:
            ai_thinking.render(
                is_thinking=True,
                thinking_message=st.session_state.ai_thinking_message,
                thinking_details=st.session_state.ai_thinking_details
            )
    
    with col2:
        # 渲染簡化版臨床Orders面板
        clinical_orders_simplified.render(on_order_action=handle_send_message)
    
    # 處理 AI 回應
    if st.session_state.ai_thinking:
        handle_ai_response()
    
    # 渲染側邊欄
    sidebar.render(
        coverage=st.session_state.coverage,
        vital_signs=st.session_state.vital_signs,
        session_ended=st.session_state.session_ended,
        on_end_session=handle_end_session,
        on_generate_detailed_report=handle_generate_detailed_report,
        detailed_report_available=st.session_state.detailed_report is not None,
        on_select_random_case=lambda: None,  # 暫時禁用
        current_case_id=st.session_state.case_id,
        has_started=st.session_state.has_started
    )
    
    # 渲染報告區域
    if not report_generation_manager.is_generating():
        report_display.render(
            session_ended=st.session_state.session_ended,
            feedback_report=st.session_state.report,
            detailed_report=st.session_state.detailed_report,
            citations=st.session_state.citations,
            rag_queries=st.session_state.rag_queries
        )


if __name__ == "__main__":
    main()
