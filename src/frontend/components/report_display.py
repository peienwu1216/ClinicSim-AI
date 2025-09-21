"""
報告顯示組件
"""

import os
import streamlit as st
from typing import Optional, List, Dict, Any
from datetime import datetime

from .base import BaseComponent
from .notion_integration import NotionIntegrationComponent
from .custom_toggle import create_custom_expander
from ...utils.text_processing import highlight_citations
from ...utils.pdf_visualizer import pdf_visualizer


class ReportDisplayComponent(BaseComponent):
    """報告顯示組件"""
    
    def __init__(self, component_id: str = "report_display"):
        super().__init__(component_id)
        self.notion_component = NotionIntegrationComponent("notion_integration")
    
    def render(self,
               session_ended: bool = False,
               feedback_report: Optional[str] = None,
               detailed_report: Optional[str] = None,
               citations: Optional[List[Dict[str, Any]]] = None,
               rag_queries: Optional[List[str]] = None,
               report_data: Optional[Dict[str, Any]] = None) -> None:
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
        
        # 顯示 Notion 整合功能
        if session_ended:
            self._render_notion_integration(report_data)
    
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
        
        # 顯示 Notion 匯出按鈕（舊版，保持向後兼容）
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
        def render_rag_content():
            st.markdown("**本次報告基於以下查詢獲取臨床指引：**")
            for i, query in enumerate(rag_queries, 1):
                st.markdown(f"{i}. {query}")
        
        create_custom_expander(
            title="RAG 查詢摘要",
            content_func=render_rag_content,
            key="rag_queries_toggle",
            style="emoji",
            emoji="🔍",
            default_expanded=False
        )
    
    def _render_notion_export_button(self) -> None:
        """渲染 Notion 匯出按鈕"""
        st.markdown("---")
        st.subheader("📝 學習記錄管理")
        
        # 檢查 Notion 配置狀態
        notion_status = self._check_notion_status()
        
        if not notion_status['configured']:
            st.warning("⚠️ Notion API 未配置")
            
            def render_notion_setup():
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
            
            create_custom_expander(
                title="如何設定 Notion 整合",
                content_func=render_notion_setup,
                key="notion_setup_toggle",
                style="emoji",
                emoji="🔧",
                default_expanded=False
            )
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
            # 檢查是否有詳細報告和報告檔案
            if not hasattr(st.session_state, 'detailed_report') or not st.session_state.detailed_report:
                st.error("❌ 請先生成完整報告後再匯出到 Notion")
                return
                
            if not hasattr(st.session_state, 'current_report_file') or not st.session_state.current_report_file:
                st.error("❌ 無法找到當前報告檔案")
                return
            
            report_filename = st.session_state.current_report_file
            case_id = st.session_state.get('case_id', 'case_chest_pain_acs_01')
            
            # 顯示匯出信息
            st.info(f"📝 準備匯出報告到 Notion...")
            
            # 發送匯出請求
            import requests
            from ..app import StreamlitApp
            
            app = StreamlitApp()
            api_base_url = app.api_base_url
            
            with st.spinner("正在匯出到 Notion..."):
                try:
                    response = requests.post(
                        f"{api_base_url}/notion/export_report",
                        json={
                            'report_text': st.session_state.detailed_report,
                            'case_id': case_id,
                            'report_title': f"學習報告 - {case_id}"
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
                    elif response.status_code == 400:
                        # 處理 400 錯誤
                        try:
                            error_data = response.json()
                            error_msg = error_data.get('error', '請求參數錯誤')
                            st.error(f"❌ 匯出失敗: {error_msg}")
                            
                            # 顯示詳細的調試信息
                            st.info(f"📝 調試信息:")
                            st.info(f"- 報告檔案: {report_filename}")
                            st.info(f"- 案例ID: {case_id}")
                            
                        except:
                            st.error(f"❌ 匯出請求失敗: HTTP {response.status_code}")
                    elif response.status_code == 500:
                        # 處理 500 錯誤
                        try:
                            error_data = response.json()
                            error_msg = error_data.get('error', '伺服器內部錯誤')
                            st.error(f"❌ 伺服器錯誤: {error_msg}")
                            
                            # 顯示 Notion 配置檢查
                            st.warning("💡 請檢查 Notion API 配置:")
                            st.info("- 確保已設定 Notion API Key")
                            st.info("- 確保已設定 Notion Database ID")
                            st.info("- 檢查 Notion 權限設定")
                            
                        except:
                            st.error(f"❌ 伺服器內部錯誤: HTTP {response.status_code}")
                    else:
                        st.error(f"❌ 匯出請求失敗: HTTP {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ 無法連接到後端服務")
                    st.info("💡 請確保後端服務正在運行 (python main.py)")
                except requests.exceptions.Timeout:
                    st.error("❌ 請求超時，請稍後再試")
                except Exception as e:
                    st.error(f"❌ 匯出時發生錯誤: {str(e)}")
                    
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
    
    def _render_notion_integration(self, report_data: Optional[Dict[str, Any]] = None) -> None:
        """渲染 Notion 整合功能"""
        # 準備報告數據
        if not report_data:
            report_data = self._prepare_report_data()
        
        # 使用新的 Notion 整合組件
        self.notion_component.render_notion_dashboard(
            report_data=report_data,
            show_setup_guide=st.session_state.get('show_notion_setup', False)
        )
    
    def _prepare_report_data(self) -> Dict[str, Any]:
        """準備報告數據用於 Notion 整合"""
        # 從 session state 獲取數據
        case_id = st.session_state.get('case_id', 'case_chest_pain_acs_01')
        feedback_report = st.session_state.get('feedback_report', '')
        detailed_report = st.session_state.get('detailed_report', '')
        
        # 嘗試從報告中提取評分信息
        total_score = self._extract_score_from_report(feedback_report or detailed_report, "總體評分")
        coverage = self._extract_score_from_report(feedback_report or detailed_report, "問診覆蓋率")
        interview_score = self._extract_score_from_report(feedback_report or detailed_report, "問診表現")
        decision_score = self._extract_score_from_report(feedback_report or detailed_report, "臨床決策")
        knowledge_score = self._extract_score_from_report(feedback_report or detailed_report, "知識應用")
        
        return {
            'case_id': case_id,
            'case_type': '胸痛',  # 可以根據 case_id 動態設定
            'total_score': total_score,
            'coverage': coverage,
            'interview_score': interview_score,
            'decision_score': decision_score,
            'knowledge_score': knowledge_score,
            'report_content': detailed_report or feedback_report,
            'report_type': 'detailed' if detailed_report else 'feedback',
            'generated_at': datetime.now().isoformat()
        }
    
    def _extract_score_from_report(self, report_text: str, score_type: str) -> float:
        """從報告文本中提取評分"""
        import re
        
        if not report_text:
            return 0.0
        
        # 根據評分類型匹配不同的模式
        patterns = {
            "總體評分": r"總體評分[：:]\s*(\d+(?:\.\d+)?)%",
            "問診覆蓋率": r"問診覆蓋率[：:]\s*(\d+(?:\.\d+)?)%",
            "問診表現": r"問診表現[：:]\s*(\d+(?:\.\d+)?)%",
            "臨床決策": r"臨床決策[：:]\s*(\d+(?:\.\d+)?)%",
            "知識應用": r"知識應用[：:]\s*(\d+(?:\.\d+)?)%"
        }
        
        pattern = patterns.get(score_type)
        if not pattern:
            return 0.0
        
        match = re.search(pattern, report_text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return 0.0
        
        return 0.0
