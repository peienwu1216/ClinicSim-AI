"""
自定義 Toggle 組件 - 解決 Streamlit expander 圖標文字問題
提供多種美觀的 toggle 按鈕替代方案
"""

import streamlit as st
from typing import Callable, Optional, Any, Dict
from pathlib import Path


class CustomToggleComponent:
    """自定義 Toggle 組件"""
    
    def __init__(self):
        self._apply_toggle_css()
    
    def _apply_toggle_css(self):
        """應用自定義 toggle CSS 樣式"""
        st.markdown("""
        <style>
        /* 自定義 Toggle 按鈕樣式 */
        .custom-toggle-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 8px;
            width: 100%;
            text-align: left;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .custom-toggle-button:hover {
            background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        .custom-toggle-button.expanded {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }
        
        .custom-toggle-button.expanded:hover {
            background: linear-gradient(135deg, #0f8a7e 0%, #32d96b 100%);
        }
        
        /* Toggle 圖標樣式 */
        .toggle-icon {
            font-size: 1.2rem;
            transition: transform 0.3s ease;
        }
        
        .toggle-icon.expanded {
            transform: rotate(180deg);
        }
        
        /* 內容區域樣式 */
        .toggle-content {
            margin-top: 8px;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #667eea;
            animation: slideDown 0.3s ease;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* 替代方案：使用 Emoji 圖標的 Toggle */
        .emoji-toggle {
            background: #ffffff;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 8px 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 6px;
        }
        
        .emoji-toggle:hover {
            border-color: #667eea;
            background: #f8f9ff;
        }
        
        .emoji-toggle.expanded {
            border-color: #11998e;
            background: #f0fff4;
        }
        
        /* 替代方案：使用 Unicode 符號的 Toggle */
        .unicode-toggle {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            border: none;
            border-radius: 6px;
            padding: 6px 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 4px;
            font-size: 0.85rem;
        }
        
        .unicode-toggle:hover {
            background: linear-gradient(135deg, #ffe0b3 0%, #fca085 100%);
        }
        
        .unicode-toggle.expanded {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        }
        
        /* 替代方案：使用 CSS 箭頭的 Toggle */
        .arrow-toggle {
            background: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 10px 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
            position: relative;
        }
        
        .arrow-toggle:hover {
            border-color: #667eea;
            box-shadow: 0 2px 4px rgba(102, 126, 234, 0.1);
        }
        
        .arrow-toggle.expanded {
            border-color: #28a745;
            background: #f8fff9;
        }
        
        .arrow-toggle::after {
            content: "▶";
            color: #6c757d;
            transition: transform 0.3s ease;
        }
        
        .arrow-toggle.expanded::after {
            content: "▼";
            color: #28a745;
        }
        
        /* 替代方案：使用 Bootstrap 風格的 Toggle */
        .bootstrap-toggle {
            background: #007bff;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 6px;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .bootstrap-toggle:hover {
            background: #0056b3;
        }
        
        .bootstrap-toggle.expanded {
            background: #28a745;
        }
        
        .bootstrap-toggle.expanded:hover {
            background: #218838;
        }
        
        /* 隱藏 Streamlit expander 的預設樣式 */
        [data-testid="stExpander"] .streamlit-expanderHeader {
            display: none !important;
        }
        
        [data-testid="stExpander"] .streamlit-expanderContent {
            border: none !important;
            padding: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def create_toggle_with_emoji(
        self, 
        title: str, 
        content_func: Callable, 
        key: str,
        default_expanded: bool = False,
        emoji: str = "📁"
    ) -> None:
        """使用 Emoji 圖標創建 Toggle"""
        if key not in st.session_state:
            st.session_state[key] = default_expanded
        
        # 創建 toggle 按鈕
        toggle_text = f"{emoji} {title}"
        arrow = "📂" if st.session_state[key] else "📁"
        
        if st.button(f"{toggle_text} {arrow}", key=f"emoji_toggle_{key}"):
            st.session_state[key] = not st.session_state[key]
            st.rerun()
        
        # 顯示內容
        if st.session_state[key]:
            with st.container():
                st.markdown('<div class="toggle-content">', unsafe_allow_html=True)
                content_func()
                st.markdown('</div>', unsafe_allow_html=True)
    
    def create_toggle_with_unicode(
        self, 
        title: str, 
        content_func: Callable, 
        key: str,
        default_expanded: bool = False
    ) -> None:
        """使用 Unicode 符號創建 Toggle"""
        if key not in st.session_state:
            st.session_state[key] = default_expanded
        
        # 創建 toggle 按鈕
        arrow = "▼" if st.session_state[key] else "▶"
        
        if st.button(f"{arrow} {title}", key=f"unicode_toggle_{key}"):
            st.session_state[key] = not st.session_state[key]
            st.rerun()
        
        # 顯示內容
        if st.session_state[key]:
            with st.container():
                st.markdown('<div class="toggle-content">', unsafe_allow_html=True)
                content_func()
                st.markdown('</div>', unsafe_allow_html=True)
    
    def create_toggle_with_arrows(
        self, 
        title: str, 
        content_func: Callable, 
        key: str,
        default_expanded: bool = False
    ) -> None:
        """使用箭頭符號創建 Toggle"""
        if key not in st.session_state:
            st.session_state[key] = default_expanded
        
        # 創建 toggle 按鈕
        arrow = "🔽" if st.session_state[key] else "🔸"
        
        if st.button(f"{arrow} {title}", key=f"arrow_toggle_{key}"):
            st.session_state[key] = not st.session_state[key]
            st.rerun()
        
        # 顯示內容
        if st.session_state[key]:
            with st.container():
                st.markdown('<div class="toggle-content">', unsafe_allow_html=True)
                content_func()
                st.markdown('</div>', unsafe_allow_html=True)
    
    def create_toggle_with_plus_minus(
        self, 
        title: str, 
        content_func: Callable, 
        key: str,
        default_expanded: bool = False
    ) -> None:
        """使用加減號創建 Toggle"""
        if key not in st.session_state:
            st.session_state[key] = default_expanded
        
        # 創建 toggle 按鈕
        symbol = "➖" if st.session_state[key] else "➕"
        
        if st.button(f"{symbol} {title}", key=f"plus_minus_toggle_{key}"):
            st.session_state[key] = not st.session_state[key]
            st.rerun()
        
        # 顯示內容
        if st.session_state[key]:
            with st.container():
                st.markdown('<div class="toggle-content">', unsafe_allow_html=True)
                content_func()
                st.markdown('</div>', unsafe_allow_html=True)
    
    def create_toggle_with_icons(
        self, 
        title: str, 
        content_func: Callable, 
        key: str,
        default_expanded: bool = False,
        icon_pair: tuple = ("👁️", "🙈")
    ) -> None:
        """使用自定義圖標對創建 Toggle"""
        if key not in st.session_state:
            st.session_state[key] = default_expanded
        
        # 創建 toggle 按鈕
        icon = icon_pair[0] if st.session_state[key] else icon_pair[1]
        
        if st.button(f"{icon} {title}", key=f"icon_toggle_{key}"):
            st.session_state[key] = not st.session_state[key]
            st.rerun()
        
        # 顯示內容
        if st.session_state[key]:
            with st.container():
                st.markdown('<div class="toggle-content">', unsafe_allow_html=True)
                content_func()
                st.markdown('</div>', unsafe_allow_html=True)
    
    def create_toggle_with_text(
        self, 
        title: str, 
        content_func: Callable, 
        key: str,
        default_expanded: bool = False,
        expand_text: str = "[展開]",
        collapse_text: str = "[收合]"
    ) -> None:
        """使用文字創建 Toggle"""
        if key not in st.session_state:
            st.session_state[key] = default_expanded
        
        # 創建 toggle 按鈕
        action_text = collapse_text if st.session_state[key] else expand_text
        
        if st.button(f"{title} {action_text}", key=f"text_toggle_{key}"):
            st.session_state[key] = not st.session_state[key]
            st.rerun()
        
        # 顯示內容
        if st.session_state[key]:
            with st.container():
                st.markdown('<div class="toggle-content">', unsafe_allow_html=True)
                content_func()
                st.markdown('</div>', unsafe_allow_html=True)


# 使用範例和工具函數
def create_custom_expander(
    title: str,
    content_func: Callable,
    key: str,
    style: str = "emoji",
    default_expanded: bool = False,
    **kwargs
) -> None:
    """
    創建自定義的 expander，替代 st.expander
    
    Args:
        title: 標題文字
        content_func: 內容渲染函數
        key: 唯一的 session state key
        style: 樣式類型 ("emoji", "unicode", "arrows", "plus_minus", "icons", "text")
        default_expanded: 預設是否展開
        **kwargs: 額外的參數（如 icon_pair, expand_text 等）
    """
    toggle_component = CustomToggleComponent()
    
    if style == "emoji":
        toggle_component.create_toggle_with_emoji(title, content_func, key, default_expanded, **kwargs)
    elif style == "unicode":
        toggle_component.create_toggle_with_unicode(title, content_func, key, default_expanded)
    elif style == "arrows":
        toggle_component.create_toggle_with_arrows(title, content_func, key, default_expanded)
    elif style == "plus_minus":
        toggle_component.create_toggle_with_plus_minus(title, content_func, key, default_expanded)
    elif style == "icons":
        toggle_component.create_toggle_with_icons(title, content_func, key, default_expanded, **kwargs)
    elif style == "text":
        toggle_component.create_toggle_with_text(title, content_func, key, default_expanded, **kwargs)
    else:
        # 預設使用 emoji 樣式
        toggle_component.create_toggle_with_emoji(title, content_func, key, default_expanded, **kwargs)
