"""
基礎組件類別
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import streamlit as st


class BaseComponent(ABC):
    """基礎組件抽象類別"""
    
    def __init__(self, key_prefix: str = ""):
        self.key_prefix = key_prefix
    
    @abstractmethod
    def render(self, **kwargs) -> Any:
        """渲染組件"""
        pass
    
    def get_state_key(self, key: str) -> str:
        """取得狀態鍵名"""
        if self.key_prefix:
            return f"{self.key_prefix}_{key}"
        return key
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """取得狀態值"""
        return st.session_state.get(self.get_state_key(key), default)
    
    def set_state(self, key: str, value: Any) -> None:
        """設定狀態值"""
        st.session_state[self.get_state_key(key)] = value
    
    def has_state(self, key: str) -> bool:
        """檢查是否有狀態值"""
        return self.get_state_key(key) in st.session_state
