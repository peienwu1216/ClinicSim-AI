"""
增強的聊天介面組件
實現直觀的聊天室UI互動
"""

import streamlit as st
from typing import List, Dict, Any, Optional, Callable
import time

from .base import BaseComponent


class EnhancedChatInterfaceComponent(BaseComponent):
    """增強的聊天介面組件 - 實現聊天室風格的UI"""
    
    def render(self,
               messages: List[Dict[str, str]],
               session_ended: bool = False,
               on_send_message: Optional[Callable[[str], None]] = None,
               on_quick_action: Optional[Callable[[str], None]] = None) -> None:
        """渲染增強的聊天介面"""
        
        # 如果沒有訊息，顯示歡迎訊息
        if not messages:
            st.info("👋 歡迎來到臨床診斷考試訓練系統！我是您的AI病人，請開始問診...")
        
        # 顯示所有訊息 - 確保訊息正確顯示
        if messages:
            # 調試信息：顯示訊息數量
            st.caption(f"💬 共 {len(messages)} 條訊息")
            
            for i, message in enumerate(messages):
                if message["role"] == "user":
                    with st.chat_message("user"):
                        st.markdown(message["content"])
                        # 調試信息
                        st.caption(f"用戶訊息 #{i+1}")
                else:
                    with st.chat_message("assistant"):
                        st.markdown(message["content"])
                        # 調試信息
                        st.caption(f"AI回應 #{i+1}")
        
        # 快速操作按鈕 - 只在對話開始前顯示
        if on_quick_action and not session_ended and not messages:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 16px; border-radius: 12px; margin: 12px 0; border-left: 4px solid #2196f3;">
                <h4 style="margin: 0 0 8px 0; color: #2c3e50;">🚀 快速開始</h4>
                <p style="margin: 0 0 12px 0; color: #6c757d; font-size: 0.9rem;">點擊下方按鈕快速開始問診，或直接在輸入框中輸入您的問題</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🩺 測量生命徵象", key="quick_vitals", use_container_width=True):
                    on_quick_action("/測量生命徵象")
            with col2:
                if st.button("❓ 詢問病史", key="quick_history", use_container_width=True):
                    on_quick_action("/詢問病史")
        
        # 聊天輸入框
        if on_send_message and not session_ended:
            if prompt := st.chat_input("請輸入您的問題..."):
                on_send_message(prompt)
        elif session_ended:
            st.info("💬 問診已結束，無法繼續對話")
    


class FixedHeaderComponent(BaseComponent):
    """固定頭部組件 - 包含標題和診斷按鈕"""
    
    def render(self, 
               case_title: str,
               session_ended: bool = False,
               on_end_session: Optional[Callable[[], None]] = None,
               on_generate_report: Optional[Callable[[], None]] = None) -> None:
        """渲染固定頭部"""
        
        # 固定頭部容器
        st.markdown('<div class="fixed-header">', unsafe_allow_html=True)
        
        # 標題和按鈕區域
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div>
                <h1>🏥 {case_title}</h1>
                <p>臨床診斷考試訓練系統</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if not session_ended and on_end_session:
                if st.button("🏁 結束問診", key="end_session_header", use_container_width=True):
                    on_end_session()
                    st.rerun()
        
        with col3:
            if session_ended and on_generate_report:
                if st.button("📊 生成報告", key="generate_report_header", use_container_width=True):
                    on_generate_report()
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

