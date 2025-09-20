"""
Streamlit 主應用程式
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
sys.path.insert(0, str(project_root / "src"))

from src.config import get_settings
from src.frontend.components import (
    SidebarComponent, 
    ChatInterfaceComponent, 
    ReportDisplayComponent,
    ClinicalOrdersCompactComponent
)
from src.frontend.components.progress_display import ReportGenerationManager
from src.frontend.components.styles import apply_custom_css


class StreamlitApp:
    """Streamlit 應用程式主類別"""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_base_url = f"http://{self.settings.host}:{self.settings.port}"
        self.case_id = self.settings.default_case_id
        
        # 初始化組件
        self.sidebar = SidebarComponent("sidebar")
        self.chat_interface = ChatInterfaceComponent("chat")
        self.report_display = ReportDisplayComponent("report")
        self.clinical_orders_compact = ClinicalOrdersCompactComponent("clinical_orders")
        self.report_generation_manager = ReportGenerationManager()
        
        # 初始化 session state
        self._init_session_state()
    
    def _init_session_state(self):
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
    
    def run(self):
        """運行應用程式"""
        # 頁面設定
        st.set_page_config(
            page_title="ClinicSim AI - 臨床技能教練", 
            page_icon="🧑‍⚕️", 
            layout="wide"
        )
        
        # 應用自定義CSS樣式
        apply_custom_css()
        
        # 渲染側邊欄
        self._render_sidebar()
        
        # 渲染主內容區域
        self._render_main_content()
        
        # 渲染報告區域
        self._render_report_area()
    
    def _render_sidebar(self):
        """渲染側邊欄"""
        self.sidebar.render(
            coverage=st.session_state.coverage,
            vital_signs=st.session_state.vital_signs,
            session_ended=st.session_state.session_ended,
            on_end_session=self._handle_end_session,
            on_generate_detailed_report=self._handle_generate_detailed_report,
            detailed_report_available=st.session_state.detailed_report is not None,
            on_select_random_case=self._handle_select_random_case,
            current_case_id=self.case_id,
            has_started=st.session_state.has_started
        )
    
    def _render_main_content(self):
        """渲染主內容區域"""
        # 創建主佈局：左側聊天，右側臨床Orders
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # 統一顯示主訴，不透露具體診斷
            st.title("模擬診間：急性胸痛")
            st.write("您現在正在與一位模擬病人進行問診。請開始您的提問。")
            
            # 渲染聊天介面
            self.chat_interface.render(
                messages=st.session_state.messages,
                session_ended=st.session_state.session_ended,
                on_send_message=self._handle_send_message,
                on_quick_action=self._handle_quick_action
            )
            
            # 在聊天介面下方顯示報告生成進度
            self._render_progress_ui()
        
        with col2:
            # 渲染緊湊版臨床Orders面板
            self.clinical_orders_compact.render(on_order_action=self._handle_order_action)
    
    def _render_progress_ui(self):
        """渲染進度 UI（在聊天介面下方）"""
        # 檢查是否正在生成報告
        if self.report_generation_manager.is_generating():
            # 顯示進度
            progress_data = st.session_state.get("report_generation_progress", {})
            current_step = progress_data.get("current_step", 0)
            total_steps = progress_data.get("total_steps", 5)
            status = progress_data.get("status", "處理中...")
            
            self.report_generation_manager.progress_component.render_report_generation_progress(
                progress=current_step / total_steps if total_steps > 0 else 0,
                status=status,
                current_step=f"步驟 {current_step}/{total_steps}",
                total_steps=total_steps,
                on_cancel=self._cancel_report_generation,
                compact=True  # 使用緊湊模式，適合在對話下方顯示
            )
    
    def _render_report_area(self):
        """渲染報告區域"""
        # 只在非生成狀態時顯示報告
        if not self.report_generation_manager.is_generating():
            self.report_display.render(
                session_ended=st.session_state.session_ended,
                feedback_report=st.session_state.report,
                detailed_report=st.session_state.detailed_report,
                citations=st.session_state.citations,
                rag_queries=st.session_state.rag_queries
            )
    
    def _handle_send_message(self, message: str):
        """處理發送訊息"""
        if not message.strip():
            return
        
        # 標記問診已開始
        st.session_state.has_started = True
        
        # 添加使用者訊息
        st.session_state.messages.append({"role": "user", "content": message})
        
        # 顯示使用者訊息
        with st.chat_message("user"):
            st.markdown(message)
        
        # 生成 AI 回應
        with st.chat_message("assistant"):
            with st.spinner("AI 病人正在思考..."):
                try:
                    response_data = self._call_api("/ask_patient", {
                        "history": st.session_state.messages,
                        "case_id": self.case_id
                    })
                    
                    ai_reply = response_data.get("reply", "無法生成回應")
                    
                    # 更新覆蓋率和生命體徵（累加式）
                    new_coverage = response_data.get("coverage", st.session_state.coverage)
                    # 只會增加，不會減少
                    if new_coverage > st.session_state.coverage:
                        st.session_state.coverage = new_coverage
                    
                    if "vital_signs" in response_data:
                        st.session_state.vital_signs = response_data["vital_signs"]
                    
                    # 添加 AI 回應
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                    st.markdown(ai_reply)
                    
                    # 重新整理頁面以更新側邊欄
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"無法連接到後端服務，請確認伺服器正在運行。\n\n錯誤訊息：{e}")
    
    def _handle_quick_action(self, action: str):
        """處理快速操作"""
        self._handle_send_message(action)
    
    def _handle_order_action(self, action: str, image_path: Optional[str] = None):
        """處理臨床檢測Orders"""
        if not action.strip():
            return
        
        # 標記問診已開始
        st.session_state.has_started = True
        
        # 添加使用者訊息
        st.session_state.messages.append({"role": "user", "content": action})
        
        # 顯示使用者訊息
        with st.chat_message("user"):
            st.markdown(action)
        
        # 如果有圖片，顯示圖片
        if image_path:
            image_full_path = self._get_image_path(image_path)
            if image_full_path and os.path.exists(image_full_path):
                st.image(image_full_path, caption=f"{self._get_order_name_from_action(action)} 檢查結果", use_column_width=True)
        
        # 生成 AI 回應
        with st.chat_message("assistant"):
            with st.spinner("AI 病人正在處理您的臨床指令..."):
                try:
                    response_data = self._call_api("/ask_patient", {
                        "history": st.session_state.messages,
                        "case_id": self.case_id
                    })
                    
                    ai_reply = response_data.get("reply", "無法生成回應")
                    
                    # 更新覆蓋率和生命體徵（累加式）
                    new_coverage = response_data.get("coverage", st.session_state.coverage)
                    # 只會增加，不會減少
                    if new_coverage > st.session_state.coverage:
                        st.session_state.coverage = new_coverage
                    
                    if "vital_signs" in response_data:
                        st.session_state.vital_signs = response_data["vital_signs"]
                    
                    # 添加 AI 回應
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                    st.markdown(ai_reply)
                    
                    # 重新整理頁面以更新側邊欄
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"無法連接到後端服務，請確認伺服器正在運行。\n\n錯誤訊息：{e}")
    
    def _get_image_path(self, image_filename: str) -> Optional[str]:
        """獲取圖片完整路徑"""
        if not image_filename:
            return None
        
        # 檢查static/samples目錄
        static_path = Path(__file__).parent.parent.parent.parent / "static" / "samples" / image_filename
        if static_path.exists():
            return str(static_path)
        
        return None
    
    def _get_order_name_from_action(self, action: str) -> str:
        """從action文字中提取Order名稱"""
        if "心電圖" in action or "ECG" in action:
            return "12導程心電圖"
        elif "X光" in action or "X-ray" in action:
            return "胸部X光"
        elif "抽血" in action or "檢驗" in action:
            return "實驗室檢驗"
        else:
            return "臨床檢測"
    
    def _handle_end_session(self):
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
                response_data = self._call_api("/get_feedback_report", {
                    "full_conversation": st.session_state.messages,
                    "case_id": self.case_id
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
    
    def _handle_generate_detailed_report(self):
        """處理生成詳細報告"""
        # 開始報告生成進度顯示
        cancelled = self.report_generation_manager.start_generation(
            on_cancel=self._cancel_report_generation
        )
        
        if cancelled:
            return
        
        try:
            # 步驟 1: 分析對話內容
            self.report_generation_manager.update_progress(
                step=1,
                status="分析對話內容",
                details="正在分析您的問診表現和對話內容..."
            )
            time.sleep(0.5)  # 模擬處理時間
            
            # 步驟 2: 生成 RAG 查詢
            self.report_generation_manager.update_progress(
                step=2,
                status="生成 RAG 查詢",
                details="正在生成相關的臨床指引查詢..."
            )
            time.sleep(0.5)
            
            # 步驟 3: 搜尋臨床指引
            self.report_generation_manager.update_progress(
                step=3,
                status="搜尋臨床指引",
                details="正在從知識庫中搜尋相關的臨床指引..."
            )
            time.sleep(0.5)
            
            # 步驟 4: 整合 AI 分析
            self.report_generation_manager.update_progress(
                step=4,
                status="整合 AI 分析",
                details="正在整合 AI 分析和臨床指引..."
            )
            time.sleep(0.5)
            
            # 步驟 5: 生成最終報告
            self.report_generation_manager.update_progress(
                step=5,
                status="生成最終報告",
                details="正在生成最終的詳細分析報告..."
            )
            
            # 實際的 API 呼叫
            response_data = self._call_api("/get_detailed_report", {
                "full_conversation": st.session_state.messages,
                "case_id": self.case_id
            })
            
            detailed_report_text = response_data.get("report_text")
            citations = response_data.get("citations", [])
            rag_queries = response_data.get("rag_queries", [])
            
            if detailed_report_text:
                st.session_state.detailed_report = detailed_report_text
                st.session_state.citations = citations
                st.session_state.rag_queries = rag_queries
                st.session_state.current_report_file = response_data.get("filename")
                
                # 完成報告生成
                self.report_generation_manager.complete_generation(success=True)
                st.rerun()
            else:
                self.report_generation_manager.complete_generation(
                    success=False, 
                    error_message="無法生成詳細報告"
                )
                
        except Exception as e:
            self.report_generation_manager.complete_generation(
                success=False,
                error_message=f"無法生成詳細報告，請確認後端服務是否正常。\n\n錯誤訊息：{e}"
            )
    
    def _cancel_report_generation(self):
        """取消報告生成"""
        self.report_generation_manager.cancel_generation()
        st.rerun()
    
    def _call_api(self, endpoint: str, payload: dict) -> dict:
        """呼叫 API"""
        response = requests.post(f"{self.api_base_url}{endpoint}", json=payload)
        response.raise_for_status()
        return response.json()
    
    def _handle_select_random_case(self):
        """處理隨機選擇病例"""
        try:
            # 呼叫 API 取得隨機病例
            response = requests.get(f"{self.api_base_url}/cases/random")
            response.raise_for_status()
            
            case_data = response.json()
            new_case_id = case_data.get("case_id")
            case_title = case_data.get("case_title", "未知病例")
            
            if new_case_id:
                # 更新當前病例 ID
                self.case_id = new_case_id
                
                # 重置 session state
                st.session_state.messages = []
                st.session_state.report = None
                st.session_state.detailed_report = None
                st.session_state.citations = []
                st.session_state.rag_queries = []
                st.session_state.session_ended = False
                st.session_state.coverage = 0
                st.session_state.vital_signs = None
                st.session_state.has_started = False
                
                # 顯示成功訊息（不透露具體診斷）
                st.success("已切換到新病例，請開始問診")
                st.rerun()
            else:
                st.error("無法取得隨機病例")
                
        except requests.exceptions.RequestException as e:
            st.error(f"無法連接到後端服務：{e}")
        except Exception as e:
            st.error(f"選擇隨機病例時發生錯誤：{e}")
    


def create_streamlit_app():
    """創建 Streamlit 應用程式"""
    app = StreamlitApp()
    return app


def main():
    """主函式"""
    app = create_streamlit_app()
    app.run()


if __name__ == "__main__":
    main()
