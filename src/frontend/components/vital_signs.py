"""
生命體徵組件
"""

import streamlit as st
from typing import Optional, Dict, Any

from .base import BaseComponent


class VitalSignsComponent(BaseComponent):
    """生命體徵顯示組件"""
    
    def render(self, vital_signs: Optional[Dict[str, Any]]) -> None:
        """渲染生命體徵組件"""
        
        if not vital_signs:
            st.info("生命體徵尚未測量")
            return
        
        st.subheader("📊 生命體徵")
        
        # 使用兩欄佈局
        col1, col2 = st.columns(2)
        
        # 左欄：心率和血氧
        with col1:
            st.metric(
                "心率 (HR)", 
                f"{vital_signs.get('HR_bpm', 'N/A')} bpm",
                delta_color="inverse"
            )
            st.metric(
                "血氧 (SpO2)", 
                f"{vital_signs.get('SpO2_room_air', 'N/A')}%",
                delta_color="inverse"
            )
        
        # 右欄：血壓和呼吸
        with col2:
            st.metric(
                "血壓 (BP)", 
                f"{vital_signs.get('BP_mmHg', 'N/A')} mmHg",
                delta_color="inverse"
            )
            st.metric(
                "呼吸 (RR)", 
                f"{vital_signs.get('RR_bpm', 'N/A')} /min",
                delta_color="inverse"
            )
        
        # 體溫（如果有）
        if vital_signs.get('Temperature'):
            st.metric(
                "體溫", 
                f"{vital_signs.get('Temperature', 'N/A')}°C",
                delta_color="inverse"
            )
