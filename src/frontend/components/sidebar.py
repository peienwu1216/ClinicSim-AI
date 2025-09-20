"""
側邊欄組件
"""

import streamlit as st
from typing import Optional, Callable

from .base import BaseComponent


class SidebarComponent(BaseComponent):
    """側邊欄組件"""
    
    def render(self, 
               coverage: int = 0,
               vital_signs: Optional[dict] = None,
               session_ended: bool = False,
               on_end_session: Optional[Callable] = None,
               on_generate_detailed_report: Optional[Callable] = None,
               detailed_report_available: bool = False) -> None:
        """渲染側邊欄"""
        
        with st.sidebar:
            # 標題
            st.title("🧑‍⚕️ ClinicSim AI")
            st.info("一個為醫學生設計的 AI 臨床技能教練。")
            
            # 覆蓋率儀表板
            self._render_coverage_meter(coverage)
            
            # 生命體徵監視器
            self._render_vital_signs_monitor(vital_signs)
            
            # 分隔線
            st.markdown("---")
            
            # 控制按鈕
            self._render_control_buttons(
                session_ended, 
                on_end_session, 
                on_generate_detailed_report,
                detailed_report_available
            )
            
            # OSCE 技巧小抄
            self._render_osce_tips()
    
    def _render_coverage_meter(self, coverage: int) -> None:
        """渲染覆蓋率儀表板"""
        st.subheader("問診覆蓋率 (Checklist Coverage)")
        st.progress(coverage, text=f"{coverage}%")
        st.caption("此儀表板會根據你的提問即時更新。")
    
    def _render_vital_signs_monitor(self, vital_signs: Optional[dict]) -> None:
        """渲染生命體徵監視器"""
        st.subheader("生命體徵監視器")
        
        if vital_signs:
            # 使用兩欄佈局來顯示
            col1, col2 = st.columns(2)
            
            col1.metric("心率 (HR)", f"{vital_signs.get('HR_bpm', 'N/A')} bpm", delta_color="inverse")
            col1.metric("血氧 (SpO2)", f"{vital_signs.get('SpO2_room_air', 'N/A')}", delta_color="inverse")
            col2.metric("血壓 (BP)", f"{vital_signs.get('BP_mmHg', 'N/A')} mmHg", delta_color="inverse")
            col2.metric("呼吸 (RR)", f"{vital_signs.get('RR_bpm', 'N/A')} /min", delta_color="inverse")
        else:
            st.info("待測量")
    
    def _render_control_buttons(self, 
                               session_ended: bool,
                               on_end_session: Optional[Callable],
                               on_generate_detailed_report: Optional[Callable],
                               detailed_report_available: bool) -> None:
        """渲染控制按鈕"""
        
        # 結束問診按鈕
        if on_end_session and st.button("進入總結與計畫", disabled=session_ended):
            on_end_session()
        
        # 詳細報告按鈕（只在問診結束後顯示）
        if session_ended and on_generate_detailed_report:
            st.markdown("---")
            st.button(
                "🤖 生成完整報告 (LLM + RAG)", 
                disabled=detailed_report_available,
                help="點擊生成包含 RAG 臨床指引的詳細分析報告",
                on_click=on_generate_detailed_report
            )
    
    def _render_osce_tips(self) -> None:
        """渲染 OSCE 技巧小抄"""
        with st.expander("💡 OSCE 技巧小抄"):
            st.markdown("""
            **開場建議：**
            > 「您好，在您同意下，為您快速了解胸痛細節，目標是盡快找到原因並幫您舒服一些。」
            
            **關鍵決策指令範例：**
            > 「您現在的症狀是我們非常重視的警訊，我會**立刻安排 12 導程心電圖（在 10 分內完成）**與抽血檢驗，同時持續監測您的生命徵象。」
            
            **結尾總結建議：**
            > 「總結一下，目前高度懷疑是心臟的問題。我們會先做檢查，如果症狀加重，請立刻告訴我們。」
            """)
