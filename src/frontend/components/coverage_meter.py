"""
覆蓋率儀表板組件
"""

import streamlit as st
from typing import Optional

from .base import BaseComponent


class CoverageMeterComponent(BaseComponent):
    """覆蓋率儀表板組件"""
    
    def render(self, coverage: int, show_details: bool = True) -> None:
        """渲染覆蓋率儀表板"""
        
        st.subheader("📈 問診覆蓋率")
        
        # 主要進度條
        st.progress(coverage / 100, text=f"{coverage}%")
        
        if show_details:
            # 詳細資訊
            self._render_coverage_details(coverage)
    
    def _render_coverage_details(self, coverage: int) -> None:
        """渲染覆蓋率詳細資訊"""
        
        # 根據覆蓋率給出評價
        if coverage >= 90:
            st.success("🎉 優秀！覆蓋率很高")
        elif coverage >= 70:
            st.warning("👍 良好，還有改進空間")
        elif coverage >= 50:
            st.info("📝 一般，建議加強問診技巧")
        else:
            st.error("⚠️ 需要加強，建議重新練習")
        
        # 進度條顏色說明
        with st.expander("覆蓋率說明", expanded=False):
            st.markdown("""
            **覆蓋率計算方式：**
            - 系統會根據你的提問內容，自動比對標準問診檢查清單
            - 每個相關關鍵字都會被計入覆蓋率
            - 建議目標覆蓋率：80% 以上
            
            **提升建議：**
            - 使用標準化的問診結構（如 OPQRST）
            - 涵蓋所有重要症狀和危險因子
            - 注意問診的系統性和完整性
            """)
