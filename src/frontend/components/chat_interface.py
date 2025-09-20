"""
聊天介面組件
"""

import streamlit as st
from typing import List, Dict, Any, Optional, Callable

from .base import BaseComponent


class ChatInterfaceComponent(BaseComponent):
    """聊天介面組件"""
    
    def render(self,
               messages: List[Dict[str, str]],
               session_ended: bool = False,
               on_send_message: Optional[Callable[[str], None]] = None,
               on_quick_action: Optional[Callable[[str], None]] = None) -> None:
        """渲染聊天介面"""
        
        # 常用指令按鈕
        self._render_quick_actions(on_quick_action)
        
        # 顯示歷史對話
        self._render_message_history(messages)
        
        # 聊天輸入框
        self._render_chat_input(session_ended, on_send_message)
    
    def _render_quick_actions(self, on_quick_action: Optional[Callable[[str], None]]) -> None:
        """渲染快速操作按鈕"""
        if on_quick_action:
            with st.container():
                with st.popover("常用指令"):
                    st.markdown("點擊下方按鈕，快速執行臨床操作：")
                    
                    if st.button("測量生命徵象", use_container_width=True):
                        on_quick_action("/測量生命徵象")
    
    def _render_message_history(self, messages: List[Dict[str, str]]) -> None:
        """渲染訊息歷史"""
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def _render_chat_input(self, 
                          session_ended: bool, 
                          on_send_message: Optional[Callable[[str], None]]) -> None:
        """渲染聊天輸入框"""
        if on_send_message:
            if prompt := st.chat_input("請開始問診...", disabled=session_ended):
                on_send_message(prompt)
