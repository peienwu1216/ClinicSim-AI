"""
Streamlit 主應用程式
"""

import streamlit as st
import requests
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# 添加項目根目錄到路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from src.config import get_settings
from src.frontend.components import (
    SidebarComponent, 
    ChatInterfaceComponent, 
    ReportDisplayComponent
)


class StreamlitApp:
    """Streamlit 應用程式主類別"""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_base_url = f"http://{self.settings.backend_host}:{self.settings.backend_port}"
        self.case_id = self.settings.default_case_id
        
        # 初始化組件
        self.sidebar = SidebarComponent("sidebar")
        self.chat_interface = ChatInterfaceComponent("chat")
        self.report_display = ReportDisplayComponent("report")
        
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
    
    def run(self):
        """運行應用程式"""
        # 頁面設定
        st.set_page_config(
            page_title="ClinicSim AI - 臨床技能教練", 
            page_icon="🧑‍⚕️", 
            layout="wide"
        )
        
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
            detailed_report_available=st.session_state.detailed_report is not None
        )
    
    def _render_main_content(self):
        """渲染主內容區域"""
        st.title("模擬診間：急性胸痛")
        st.write("您現在正在與一位模擬病人進行問診。請開始您的提問。")
        
        # 渲染聊天介面
        self.chat_interface.render(
            messages=st.session_state.messages,
            session_ended=st.session_state.session_ended,
            on_send_message=self._handle_send_message,
            on_quick_action=self._handle_quick_action
        )
    
    def _render_report_area(self):
        """渲染報告區域"""
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
                    
                    # 更新覆蓋率和生命體徵
                    st.session_state.coverage = response_data.get("coverage", st.session_state.coverage)
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
    
    def _handle_end_session(self):
        """處理結束問診"""
        st.session_state.session_ended = True
        
        with st.spinner("AI 評估官正在生成您的回饋報告..."):
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
        with st.spinner("AI 教師正在生成詳細分析報告（包含 RAG 臨床指引）..."):
            try:
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
                    st.rerun()
                else:
                    st.error("無法生成詳細報告")
                    
            except Exception as e:
                st.error(f"無法生成詳細報告，請確認後端服務是否正常。\n\n錯誤訊息：{e}")
    
    def _call_api(self, endpoint: str, payload: dict) -> dict:
        """呼叫 API"""
        response = requests.post(f"{self.api_base_url}{endpoint}", json=payload)
        response.raise_for_status()
        return response.json()


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
