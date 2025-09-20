"""
文字處理工具函式
"""

import re
from typing import List, Dict, Any


def highlight_citations(text: str, citations: List[Dict[str, Any]]) -> str:
    """在文字中高亮顯示引註標記"""
    if not citations:
        return text
    
    # 為每個引註標記添加樣式，確保字體大小與其他文字一致
    for citation in citations:
        citation_id = citation['id']
        pattern = f'\\[引註 {citation_id}\\]'
        replacement = f'<span style="background-color: #e1f5fe !important; padding: 2px 6px !important; border-radius: 4px !important; font-weight: bold !important; color: #0277bd !important; font-size: 14px !important; line-height: 1.6 !important; display: inline !important;">[引註 {citation_id}]</span>'
        text = re.sub(pattern, replacement, text)
    
    return text


def extract_keywords(text: str, keywords: List[str]) -> List[str]:
    """從文字中提取匹配的關鍵字"""
    text_lower = text.lower()
    matched_keywords = []
    
    for keyword in keywords:
        if keyword.lower() in text_lower:
            matched_keywords.append(keyword)
    
    return matched_keywords


def clean_text(text: str) -> str:
    """清理文字內容"""
    # 移除多餘的空白字符
    text = re.sub(r'\s+', ' ', text)
    # 移除首尾空白
    text = text.strip()
    return text


def extract_citation_references(text: str) -> List[int]:
    """從文字中提取引註編號"""
    pattern = r'\[引註 (\d+)\]'
    matches = re.findall(pattern, text)
    return [int(match) for match in matches]


def format_conversation_for_display(messages: List[Dict[str, str]]) -> str:
    """格式化對話內容用於顯示"""
    formatted_lines = []
    
    for msg in messages:
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        
        if role == 'user':
            formatted_lines.append(f"👤 學生：{content}")
        elif role == 'assistant':
            formatted_lines.append(f"🤖 AI病人：{content}")
        else:
            formatted_lines.append(f"{role}：{content}")
    
    return "\n\n".join(formatted_lines)
