"""
報告顯示組件
"""

import streamlit as st
from typing import Optional, List, Dict, Any

from .base import BaseComponent
from ...utils.text_processing import highlight_citations


class ReportDisplayComponent(BaseComponent):
    """報告顯示組件"""
    
    def render(self,
               session_ended: bool = False,
               feedback_report: Optional[str] = None,
               detailed_report: Optional[str] = None,
               citations: Optional[List[Dict[str, Any]]] = None,
               rag_queries: Optional[List[str]] = None) -> None:
        """渲染報告顯示區域"""
        
        if not session_ended:
            return
        
        st.info("本次問診已結束。")
        
        # 顯示即時報告（第一階段）
        if feedback_report:
            self._render_feedback_report(feedback_report)
        
        # 顯示詳細報告（第二階段）
        if detailed_report:
            self._render_detailed_report(detailed_report, citations, rag_queries)
        elif session_ended:
            self._render_report_prompt()
    
    def _render_feedback_report(self, report_text: str) -> None:
        """渲染即時回饋報告"""
        st.markdown("---")
        st.subheader("📊 即時評估報告")
        st.markdown(report_text)
    
    def _render_detailed_report(self, 
                               report_text: str,
                               citations: Optional[List[Dict[str, Any]]],
                               rag_queries: Optional[List[str]]) -> None:
        """渲染詳細報告"""
        st.markdown("---")
        st.subheader("🤖 完整分析報告 (LLM + RAG)")
        st.info("此報告由 AI 教師基於臨床指引生成，包含詳細的學習建議。")
        
        # 顯示報告內容，包含引註高亮
        if citations:
            highlighted_report = highlight_citations(report_text, citations)
            st.markdown(highlighted_report, unsafe_allow_html=True)
        else:
            st.markdown(report_text)
        
        # 顯示引註資訊
        if citations:
            self._render_citations(citations)
        
        # 顯示 RAG 查詢摘要
        if rag_queries:
            self._render_rag_queries(rag_queries)
    
    def _render_citations(self, citations: List[Dict[str, Any]]) -> None:
        """渲染引註資訊"""
        st.markdown("---")
        st.subheader("📚 引註來源")
        st.info("以下為報告中引用的臨床指引來源，點擊可查看詳細內容。")
        
        for citation in citations:
            self._render_citation_modal(citation)
    
    def _render_citation_modal(self, citation: Dict[str, Any]) -> None:
        """渲染單個引註模態框"""
        with st.expander(f"📚 引註 {citation['id']}: {citation['query']}", expanded=False):
            st.markdown("**來源：** " + citation['source'])
            st.markdown("**查詢：** " + citation['query'])
            st.markdown("**內容：**")
            st.markdown(citation['content'])
    
    def _render_rag_queries(self, rag_queries: List[str]) -> None:
        """渲染 RAG 查詢摘要"""
        with st.expander("🔍 RAG 查詢摘要", expanded=False):
            st.markdown("**本次報告基於以下查詢獲取臨床指引：**")
            for i, query in enumerate(rag_queries, 1):
                st.markdown(f"{i}. {query}")
    
    def _render_report_prompt(self) -> None:
        """渲染報告提示"""
        st.markdown("---")
        st.info("💡 點擊左側「生成完整報告」按鈕，獲取包含 RAG 臨床指引的詳細分析。")
