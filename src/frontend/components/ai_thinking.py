"""
AI 思考中 UI 組件
提供美觀的 AI 思考中動畫效果
"""

import streamlit as st
from typing import List, Dict, Any, Optional, Callable
import time

from .base import BaseComponent


class AIThinkingComponent(BaseComponent):
    """AI 思考中組件 - 提供美觀的思考動畫"""
    
    def render(self, 
               is_thinking: bool = False,
               thinking_message: str = "AI 病人正在思考...",
               thinking_details: str = "正在分析您的問題並準備回應") -> None:
        """渲染 AI 思考中 UI"""
        
        if is_thinking:
            st.markdown(f"""
            <div class="ai-thinking-container">
                <div class="ai-thinking-header">
                    <span class="ai-thinking-icon">🤖</span>
                    <span>{thinking_message}</span>
                    <div class="ai-thinking-dots">
                        <div class="ai-thinking-dot"></div>
                        <div class="ai-thinking-dot"></div>
                        <div class="ai-thinking-dot"></div>
                    </div>
                </div>
                <div class="ai-thinking-status">
                    {thinking_details}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_simple(self, message: str = "AI 病人正在思考...") -> None:
        """渲染簡單的思考指示器"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 15px;
            margin: 12px 0;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-weight: 600;
            text-align: center;
            animation: pulse 2s ease-in-out infinite;
        ">
            <span style="margin-right: 10px;">🤖</span>
            {message}
            <span style="margin-left: 10px;">⏳</span>
        </div>
        """, unsafe_allow_html=True)


class AIThinkingManager:
    """AI 思考管理器 - 管理思考狀態"""
    
    def __init__(self):
        self._thinking = False
        self._thinking_message = "AI 病人正在思考..."
        self._thinking_details = "正在分析您的問題並準備回應"
    
    def start_thinking(self, 
                      message: str = "AI 病人正在思考...",
                      details: str = "正在分析您的問題並準備回應"):
        """開始思考狀態"""
        self._thinking = True
        self._thinking_message = message
        self._thinking_details = details
    
    def stop_thinking(self):
        """停止思考狀態"""
        self._thinking = False
    
    def is_thinking(self) -> bool:
        """檢查是否正在思考"""
        return self._thinking
    
    def get_thinking_message(self) -> str:
        """獲取思考訊息"""
        return self._thinking_message
    
    def get_thinking_details(self) -> str:
        """獲取思考詳情"""
        return self._thinking_details
