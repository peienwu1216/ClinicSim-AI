"""
報告顯示組件
"""

import os
import streamlit as st
from typing import Optional, List, Dict, Any

from .base import BaseComponent
from ...utils.text_processing import highlight_citations
from ...utils.pdf_visualizer import pdf_visualizer


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
        processed_report = self._process_report_formatting(report_text)
        st.markdown(processed_report)
    
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
            processed_report = self._process_report_formatting(highlighted_report)
            # 使用 unsafe_allow_html=True 來支持 HTML 格式
            st.markdown(processed_report, unsafe_allow_html=True)
        else:
            processed_report = self._process_report_formatting(report_text)
            # 使用 unsafe_allow_html=True 來支持 HTML 格式
            st.markdown(processed_report, unsafe_allow_html=True)
        
        # 顯示引註資訊
        if citations:
            self._render_citations(citations)
        
        # 顯示 RAG 查詢摘要
        if rag_queries:
            self._render_rag_queries(rag_queries)
        
        # 顯示 Notion 匯出按鈕
        self._render_notion_export_button()
    
    def _render_citations(self, citations: List[Dict[str, Any]]) -> None:
        """渲染引註資訊，現在包含 PDF 截圖"""
        st.markdown("---")
        st.subheader("📚 附錄：引註來源視覺化")
        st.info("以下為報告中引用的臨床指引來源。我們已為您從原始 PDF 中截取出相關段落並高亮顯示。")
        
        # 將 st.session_state.citations 轉換回物件
        from ...models.report import Citation
        citation_objects = [Citation(**c) for c in citations]

        for citation in citation_objects:
            self._render_citation_with_visualization(citation)
    
    def _render_citation_with_visualization(self, citation) -> None:
        """渲染帶有 PDF 視覺化的引註"""
        source_info = f"引註 {citation.id}: **{citation.source}**"
        if citation.page_number:
            source_info += f" (第 {citation.page_number} 頁)"
        
        with st.expander(source_info, expanded=True):
            # 顯示查詢資訊
            st.markdown(f"**查詢：** {citation.query}")
            
            # 嘗試產生 PDF 截圖
            if citation.page_number and citation.metadata and citation.metadata.get('original_source'):
                with st.spinner("正在產生 PDF 截圖..."):
                    snippet_path = pdf_visualizer.create_source_snippet(citation)
                
                if snippet_path:
                    st.markdown("**原始文件截圖：**")
                    st.image(snippet_path, caption=f"原始文件 '{citation.source}' 第 {citation.page_number} 頁的內容截圖")
                    
                    # 顯示檔案資訊
                    if os.path.exists(snippet_path):
                        file_size = os.path.getsize(snippet_path) / 1024  # KB
                        st.caption(f"截圖檔案大小: {file_size:.1f} KB")
                else:
                    st.warning("⚠️ 無法產生此引註的視覺化截圖")
            else:
                st.info("ℹ️ 此引註沒有頁碼資訊，無法產生 PDF 截圖")
            
            # 顯示文字內容作為備用
            st.markdown("**引用的內容：**")
            st.markdown(f"> {citation.content}")
    
    def _render_citation_modal(self, citation: Dict[str, Any]) -> None:
        """渲染單個引註模態框（向後兼容）"""
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
    
    def _render_notion_export_button(self) -> None:
        """渲染 Notion 匯出按鈕"""
        st.markdown("---")
        st.subheader("📝 學習記錄管理")
        
        # 檢查 Notion 配置狀態
        notion_status = self._check_notion_status()
        
        if not notion_status['configured']:
            st.warning("⚠️ Notion API 未配置")
            with st.expander("🔧 如何設定 Notion 整合", expanded=False):
                st.markdown("""
                **步驟 1: 創建 Notion Integration**
                1. 前往 [Notion Developers](https://www.notion.so/my-integrations)
                2. 點擊 "New integration"
                3. 填寫名稱和選擇工作區
                4. 複製 "Internal Integration Token"
                
                **步驟 2: 創建 Database**
                1. 在 Notion 中創建新的 Database
                2. 添加以下欄位：
                   - 案例標題 (Title)
                   - 學習日期 (Date)
                   - 案例類型 (Select)
                   - 問診表現 (Number)
                   - 臨床決策 (Number)
                   - 知識應用 (Number)
                   - 總體評價 (Number)
                   - 複習狀態 (Select)
                
                **步驟 3: 設定環境變數**
                ```bash
                export NOTION_API_KEY="your_integration_token"
                export NOTION_DATABASE_ID="your_database_id"
                ```
                """)
            return
        
        if not notion_status['connected']:
            st.error(f"❌ Notion 連線失敗: {notion_status['message']}")
            return
        
        # 顯示匯出按鈕
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("📤 將學習報告輸出至 Notion", 
                        help="將完整的學習報告匯出到 Notion 作為學習記錄",
                        type="primary"):
                self._handle_notion_export()
        
        with col2:
            if st.button("🔄 重新測試連線", help="重新測試 Notion API 連線"):
                st.rerun()
        
        with col3:
            if st.button("📋 查看最近報告", help="查看最近的報告檔案"):
                self._show_recent_reports()
    
    def _check_notion_status(self) -> Dict[str, Any]:
        """檢查 Notion 配置和連線狀態"""
        try:
            import requests
            from ..app import StreamlitApp
            
            # 使用動態配置的 API 基礎 URL
            app = StreamlitApp()
            api_base_url = app.api_base_url
            
            # 檢查配置
            response = requests.get(
                f"{api_base_url}/notion/test_connection",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'configured': data.get('configured', False),
                    'connected': data.get('success', False),
                    'message': data.get('message', '')
                }
            else:
                return {
                    'configured': False,
                    'connected': False,
                    'message': 'API 請求失敗'
                }
                
        except Exception as e:
            return {
                'configured': False,
                'connected': False,
                'message': f'連線錯誤: {str(e)}'
            }
    
    def _handle_notion_export(self) -> None:
        """處理 Notion 匯出"""
        try:
            # 獲取當前報告的檔案名稱
            if not hasattr(st.session_state, 'current_report_file'):
                st.error("❌ 無法找到當前報告檔案")
                return
            
            report_filename = st.session_state.current_report_file
            case_id = st.session_state.get('case_id', 'case_chest_pain_acs_01')
            
            # 發送匯出請求
            import requests
            from ..app import StreamlitApp
            
            app = StreamlitApp()
            api_base_url = app.api_base_url
            
            response = requests.post(
                f"{api_base_url}/notion/export_report",
                json={
                    'report_filename': report_filename,
                    'case_id': case_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    st.success(f"✅ {data.get('message', '匯出成功')}")
                    
                    # 顯示 Notion 頁面連結
                    if '頁面連結' in data.get('message', ''):
                        st.markdown("🔗 [點擊此處開啟 Notion 頁面]({})".format(
                            data['message'].split('頁面連結: ')[1]
                        ))
                else:
                    st.error(f"❌ 匯出失敗: {data.get('message', '未知錯誤')}")
            else:
                st.error(f"❌ 匯出請求失敗: HTTP {response.status_code}")
                
        except Exception as e:
            st.error(f"❌ 匯出時發生錯誤: {str(e)}")
    
    def _show_recent_reports(self) -> None:
        """顯示最近的報告檔案"""
        try:
            import requests
            from ..app import StreamlitApp
            
            app = StreamlitApp()
            api_base_url = app.api_base_url
            
            response = requests.get(
                f"{api_base_url}/notion/get_recent_reports",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                reports = data.get('reports', [])
                
                if reports:
                    st.markdown("**最近的報告檔案:**")
                    for report in reports[:5]:  # 只顯示最近5個
                        filename = report.get('filename', '未知檔案')
                        case_id = report.get('case_id', '未知案例')
                        report_type = report.get('report_type', '未知類型')
                        
                        st.markdown(f"- **{filename}** ({case_id}, {report_type})")
                else:
                    st.info("📁 暫無報告檔案")
            else:
                st.error(f"❌ 無法取得報告列表: HTTP {response.status_code}")
                
        except Exception as e:
            st.error(f"❌ 取得報告列表時發生錯誤: {str(e)}")
    
    def _process_report_formatting(self, text: str) -> str:
        """處理報告文本格式，避免 Markdown 格式問題"""
        import re
        
        # 1. 處理 RAG 來源標題格式，將 **Review xxx** 轉換為普通文字
        # 匹配模式：📚 **Review xxx**
        pattern = r'📚 \*\*(Review [^*]+)\*\*'
        replacement = r'📚 \1'
        text = re.sub(pattern, replacement, text)
        
        # 2. 處理所有孤立的粗體格式（除了標題）
        # 將 **text** 轉換為普通文字（如果不是在標題行中）
        pattern = r'(?<!### )\*\*([^*]+)\*\*(?! :)'
        replacement = r'\1'
        text = re.sub(pattern, replacement, text)
        
        # 3. 處理可能的 Markdown 標題格式問題
        # 確保只有真正的標題使用 ### 格式
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            # 如果行以 ### 開頭但不是真正的標題，移除 ###
            if line.startswith('### ') and not any(keyword in line for keyword in ['問診表現', '臨床決策', '知識應用', '改進建議', '總結', '相關臨床指引']):
                processed_lines.append(line[4:])  # 移除 '### '
            else:
                processed_lines.append(line)
        
        text = '\n'.join(processed_lines)
        
        # 4. 最後清理：移除任何剩餘的 Markdown 格式符號
        # 處理可能導致顯示問題的特殊字符組合
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # 移除所有剩餘的 **
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)  # 移除行首的 # 標題符號
        
        # 5. 使用強制性的 CSS 樣式來確保文字大小一致
        # 使用 !important 聲明來覆蓋 Streamlit 的默認樣式
        text = f'<div style="font-size: 14px !important; line-height: 1.6 !important; font-family: inherit !important;">{text}</div>'
        
        return text
    
    def _render_report_prompt(self) -> None:
        """渲染報告提示"""
        st.markdown("---")
        st.info("💡 點擊左側「生成完整報告」按鈕，獲取包含 RAG 臨床指引的詳細分析。")
