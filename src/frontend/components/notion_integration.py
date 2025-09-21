"""
Notion 整合 UI 組件
提供完整的 Notion 串接功能和用戶體驗
"""

import streamlit as st
import requests
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

from .base import BaseComponent


class NotionIntegrationComponent(BaseComponent):
    """Notion 整合 UI 組件"""
    
    def __init__(self, component_id: str = "notion_integration"):
        super().__init__(component_id)
        self.api_base_url = self._get_api_base_url()
    
    def render(self, **kwargs) -> None:
        """實作 BaseComponent 的抽象方法"""
        report_data = kwargs.get('report_data')
        show_setup_guide = kwargs.get('show_setup_guide', False)
        self.render_notion_dashboard(report_data, show_setup_guide)
    
    def _get_api_base_url(self) -> str:
        """獲取 API 基礎 URL"""
        try:
            from ..app import StreamlitApp
            app = StreamlitApp()
            return app.api_base_url
        except:
            return "http://localhost:5000"
    
    def render_notion_dashboard(self, 
                              report_data: Optional[Dict[str, Any]] = None,
                              show_setup_guide: bool = False) -> None:
        """渲染 Notion 整合儀表板"""
        
        st.markdown("---")
        st.subheader("📝 學習記錄管理")
        
        # 檢查 Notion 狀態
        notion_status = self._check_notion_status()
        
        if show_setup_guide or not notion_status['configured']:
            self._render_setup_guide()
            return
        
        if not notion_status['connected']:
            self._render_connection_error(notion_status['message'])
            return
        
        # 顯示主要功能區域
        self._render_main_functions(report_data)
        
        # 顯示歷史記錄
        self._render_history_section()
    
    def _render_setup_guide(self) -> None:
        """渲染 Notion 設定指南"""
        st.warning("⚠️ Notion API 未配置")
        
        with st.expander("🔧 Notion 整合設定指南", expanded=True):
            st.markdown("""
            ### 步驟 1: 創建 Notion Integration
            
            1. 前往 [Notion Developers](https://www.notion.so/my-integrations)
            2. 點擊 "New integration"
            3. 填寫以下資訊：
               - **名稱**: ClinicSim-AI 學習記錄
               - **工作區**: 選擇您的工作區
               - **功能**: 選擇 "Read content" 和 "Update content"
            4. 複製 "Internal Integration Token"
            
            ### 步驟 2: 創建學習記錄 Database
            
            在 Notion 中創建新的 Database，並添加以下欄位：
            
            | 欄位名稱 | 類型 | 說明 |
            |---------|------|------|
            | 案例標題 | Title | 學習案例的名稱 |
            | 學習日期 | Date | 學習日期 |
            | 案例類型 | Select | 胸痛、腹痛等 |
            | 問診表現 | Number | 問診技巧評分 (0-100) |
            | 臨床決策 | Number | 臨床決策評分 (0-100) |
            | 知識應用 | Number | 知識應用評分 (0-100) |
            | 總體評價 | Number | 總體評分 (0-100) |
            | 複習狀態 | Select | 未複習、已複習、需加強 |
            | 學習筆記 | Text | 個人學習筆記 |
            | 報告內容 | Text | 完整報告內容 |
            
            ### 步驟 3: 設定環境變數
            
            在您的系統中設定以下環境變數：
            
            ```bash
            # Windows (PowerShell)
            $env:NOTION_API_KEY="your_integration_token"
            $env:NOTION_DATABASE_ID="your_database_id"
            
            # Linux/Mac
            export NOTION_API_KEY="your_integration_token"
            export NOTION_DATABASE_ID="your_database_id"
            ```
            
            ### 步驟 4: 重新啟動應用程式
            
            設定完成後，請重新啟動 ClinicSim-AI 應用程式。
            """)
            
            # 提供測試按鈕
            if st.button("🔄 重新檢查配置", help="重新檢查 Notion 配置狀態"):
                st.rerun()
    
    def _render_connection_error(self, error_message: str) -> None:
        """渲染連線錯誤"""
        st.error(f"❌ Notion 連線失敗: {error_message}")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🔄 重新測試連線", help="重新測試 Notion API 連線"):
                st.rerun()
        
        with col2:
            if st.button("🔧 查看設定指南", help="查看 Notion 設定指南"):
                st.session_state.show_notion_setup = True
                st.rerun()
    
    def _render_main_functions(self, report_data: Optional[Dict[str, Any]]) -> None:
        """渲染主要功能區域"""
        
        # 創建三列布局
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if report_data:
                self._render_export_current_report(report_data)
            else:
                st.info("💡 完成問診後，您可以在這裡管理學習記錄")
        
        with col2:
            if st.button("📋 查看歷史記錄", help="查看所有學習記錄"):
                st.session_state.show_notion_history = True
                st.rerun()
        
        with col3:
            if st.button("⚙️ 管理設定", help="管理 Notion 整合設定"):
                st.session_state.show_notion_settings = True
                st.rerun()
    
    def _render_export_current_report(self, report_data: Dict[str, Any]) -> None:
        """渲染匯出當前報告功能"""
        
        # 顯示報告摘要
        st.markdown("**當前報告摘要:**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("總體評分", f"{report_data.get('total_score', 0):.1f}%")
        with col2:
            st.metric("問診覆蓋率", f"{report_data.get('coverage', 0):.1f}%")
        with col3:
            st.metric("案例類型", report_data.get('case_type', '胸痛'))
        with col4:
            st.metric("學習日期", datetime.now().strftime("%m/%d"))
        
        # 匯出選項
        st.markdown("**匯出選項:**")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("📤 匯出到 Notion", 
                        help="將完整報告匯出到 Notion 學習記錄",
                        type="primary"):
                self._handle_export_to_notion(report_data)
        
        with col2:
            if st.button("💾 下載報告", 
                        help="下載報告為 Markdown 檔案"):
                self._handle_download_report(report_data)
    
    def _render_history_section(self) -> None:
        """渲染歷史記錄區域"""
        
        if st.session_state.get('show_notion_history', False):
            st.markdown("---")
            st.subheader("📚 學習歷史記錄")
            
            # 獲取歷史記錄
            history_data = self._get_learning_history()
            
            if history_data:
                self._render_history_table(history_data)
            else:
                st.info("📁 暫無學習記錄")
            
            if st.button("❌ 關閉歷史記錄"):
                st.session_state.show_notion_history = False
                st.rerun()
    
    def _render_history_table(self, history_data: List[Dict[str, Any]]) -> None:
        """渲染歷史記錄表格"""
        
        # 創建 DataFrame 顯示
        import pandas as pd
        
        df_data = []
        for record in history_data:
            df_data.append({
                "學習日期": record.get('date', 'N/A'),
                "案例標題": record.get('title', 'N/A'),
                "總體評分": f"{record.get('total_score', 0):.1f}%",
                "問診表現": f"{record.get('interview_score', 0):.1f}%",
                "臨床決策": f"{record.get('decision_score', 0):.1f}%",
                "複習狀態": record.get('review_status', '未複習'),
                "Notion 連結": "🔗" if record.get('notion_url') else "❌"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # 提供操作按鈕
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔄 重新整理"):
                st.rerun()
        
        with col2:
            if st.button("📊 查看統計"):
                self._render_learning_statistics(history_data)
        
        with col3:
            if st.button("📤 批量匯出"):
                self._handle_batch_export(history_data)
    
    def _render_learning_statistics(self, history_data: List[Dict[str, Any]]) -> None:
        """渲染學習統計"""
        
        st.markdown("---")
        st.subheader("📊 學習統計分析")
        
        if not history_data:
            st.info("📁 暫無數據可分析")
            return
        
        # 計算統計數據
        total_sessions = len(history_data)
        avg_total_score = sum(record.get('total_score', 0) for record in history_data) / total_sessions
        avg_interview_score = sum(record.get('interview_score', 0) for record in history_data) / total_sessions
        avg_decision_score = sum(record.get('decision_score', 0) for record in history_data) / total_sessions
        
        # 顯示統計卡片
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("總學習次數", total_sessions)
        with col2:
            st.metric("平均總體評分", f"{avg_total_score:.1f}%")
        with col3:
            st.metric("平均問診表現", f"{avg_interview_score:.1f}%")
        with col4:
            st.metric("平均臨床決策", f"{avg_decision_score:.1f}%")
        
        # 學習進度圖表
        if len(history_data) > 1:
            import pandas as pd
            import plotly.express as px
            
            # 準備圖表數據
            chart_data = []
            for i, record in enumerate(history_data):
                chart_data.append({
                    "學習次數": i + 1,
                    "總體評分": record.get('total_score', 0),
                    "問診表現": record.get('interview_score', 0),
                    "臨床決策": record.get('decision_score', 0)
                })
            
            df_chart = pd.DataFrame(chart_data)
            
            # 創建折線圖
            fig = px.line(df_chart, 
                         x="學習次數", 
                         y=["總體評分", "問診表現", "臨床決策"],
                         title="學習進度趨勢",
                         labels={"value": "評分 (%)", "variable": "評分類型"})
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _check_notion_status(self) -> Dict[str, Any]:
        """檢查 Notion 配置和連線狀態"""
        try:
            response = requests.get(
                f"{self.api_base_url}/notion/test_connection",
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
    
    def _handle_export_to_notion(self, report_data: Dict[str, Any]) -> None:
        """處理匯出到 Notion"""
        try:
            with st.spinner("正在匯出到 Notion..."):
                response = requests.post(
                    f"{self.api_base_url}/notion/export_report",
                    json={
                        'report_data': report_data,
                        'export_type': 'current_report'
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        st.success(f"✅ {data.get('message', '匯出成功')}")
                        
                        # 顯示 Notion 頁面連結
                        if 'notion_url' in data:
                            st.markdown(f"🔗 [點擊此處開啟 Notion 頁面]({data['notion_url']})")
                    else:
                        st.error(f"❌ 匯出失敗: {data.get('message', '未知錯誤')}")
                else:
                    st.error(f"❌ 匯出請求失敗: HTTP {response.status_code}")
                    
        except Exception as e:
            st.error(f"❌ 匯出時發生錯誤: {str(e)}")
    
    def _handle_download_report(self, report_data: Dict[str, Any]) -> None:
        """處理下載報告"""
        try:
            # 生成報告內容
            report_content = self._generate_download_content(report_data)
            
            # 創建下載按鈕
            st.download_button(
                label="💾 下載報告 (Markdown)",
                data=report_content,
                file_name=f"學習報告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"❌ 下載時發生錯誤: {str(e)}")
    
    def _get_learning_history(self) -> List[Dict[str, Any]]:
        """獲取學習歷史記錄"""
        try:
            response = requests.get(
                f"{self.api_base_url}/notion/get_learning_history",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('history', [])
            else:
                st.error(f"❌ 無法取得歷史記錄: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            st.error(f"❌ 取得歷史記錄時發生錯誤: {str(e)}")
            return []
    
    def _handle_batch_export(self, history_data: List[Dict[str, Any]]) -> None:
        """處理批量匯出"""
        try:
            with st.spinner("正在批量匯出到 Notion..."):
                response = requests.post(
                    f"{self.api_base_url}/notion/batch_export",
                    json={
                        'history_data': history_data
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        st.success(f"✅ 批量匯出成功: {data.get('message', '')}")
                    else:
                        st.error(f"❌ 批量匯出失敗: {data.get('message', '未知錯誤')}")
                else:
                    st.error(f"❌ 批量匯出請求失敗: HTTP {response.status_code}")
                    
        except Exception as e:
            st.error(f"❌ 批量匯出時發生錯誤: {str(e)}")
    
    def _generate_download_content(self, report_data: Dict[str, Any]) -> str:
        """生成下載內容"""
        content = f"""# 學習報告

## 基本資訊
- **學習日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **案例類型**: {report_data.get('case_type', '胸痛')}
- **總體評分**: {report_data.get('total_score', 0):.1f}%
- **問診覆蓋率**: {report_data.get('coverage', 0):.1f}%

## 評分詳情
- **問診表現**: {report_data.get('interview_score', 0):.1f}%
- **臨床決策**: {report_data.get('decision_score', 0):.1f}%
- **知識應用**: {report_data.get('knowledge_score', 0):.1f}%

## 報告內容
{report_data.get('report_content', '無報告內容')}

---
*此報告由 ClinicSim-AI 系統生成於 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return content
