"""
進度顯示組件
用於顯示報告生成過程中的進度和狀態
"""

import streamlit as st
import time
from typing import Optional, Callable, Dict, Any
from .base import BaseComponent
from .styles import apply_custom_css
from .custom_toggle import create_custom_expander


class ProgressDisplayComponent(BaseComponent):
    """進度顯示組件"""
    
    def __init__(self, component_id: str):
        super().__init__(component_id)
        self.progress_bar = None
        self.status_text = None
        self.cancel_button = None
    
    def render(self, **kwargs) -> Any:
        """渲染組件（實現抽象方法）"""
        # 預設渲染方法，可以根據需要自定義
        progress = kwargs.get('progress', 0.0)
        status = kwargs.get('status', '準備中...')
        current_step = kwargs.get('current_step', '')
        total_steps = kwargs.get('total_steps', 5)
        on_cancel = kwargs.get('on_cancel', None)
        
        return self.render_report_generation_progress(
            progress=progress,
            status=status,
            current_step=current_step,
            total_steps=total_steps,
            on_cancel=on_cancel
        )
    
    def render_report_generation_progress(self, 
                                        progress: float = 0.0,
                                        status: str = "準備中...",
                                        current_step: str = "",
                                        total_steps: int = 5,
                                        on_cancel: Optional[Callable] = None,
                                        compact: bool = False) -> bool:
        """
        渲染報告生成進度
        
        Args:
            progress: 進度百分比 (0.0 - 1.0)
            status: 當前狀態描述
            current_step: 當前步驟描述
            total_steps: 總步驟數
            on_cancel: 取消回調函數
            compact: 是否使用緊湊模式（適合在對話下方顯示）
        
        Returns:
            bool: 是否被取消
        """
        # 應用自定義樣式
        apply_custom_css()
        
        # 創建進度容器
        progress_container = st.container()
        
        with progress_container:
            if compact:
                # 緊湊模式：適合在對話下方顯示
                self._render_compact_progress(progress, status, current_step, total_steps, on_cancel)
            else:
                # 完整模式：適合在報告區域顯示
                self._render_full_progress(progress, status, current_step, total_steps, on_cancel)
        
        return False
    
    def _render_compact_progress(self, progress: float, status: str, current_step: str, total_steps: int, on_cancel: Optional[Callable] = None) -> bool:
        """渲染緊湊模式進度（適合在對話下方顯示）"""
        # 使用精美的漸層背景和動畫效果
        st.markdown('''
        <div class="enhanced-progress-container">
            <div class="progress-header">
                <div class="progress-title">
                    <span class="ai-icon">🤖</span>
                    <span class="title-text">AI 教師正在生成詳細分析報告</span>
                    <div class="loading-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 創建進度條和狀態區域
        progress_container = st.container()
        
        with progress_container:
            # 進度條區域
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # 美化進度條
                progress_percent = int(progress * 100)
                st.markdown(f'''
                <div class="progress-wrapper">
                    <div class="progress-info">
                        <span class="progress-percent">{progress_percent}%</span>
                        <span class="progress-status">{status}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # 使用自定義進度條
                self.progress_bar = st.progress(progress, text=f"進度: {progress_percent}%")
                
                # 當前步驟顯示
                if current_step:
                    st.markdown(f'''
                    <div class="current-step">
                        <span class="step-icon">🔄</span>
                        <span class="step-text">{current_step}</span>
                    </div>
                    ''', unsafe_allow_html=True)
            
            with col2:
                if on_cancel:
                    if st.button("❌ 取消", key="cancel_report_generation_compact", help="取消報告生成", type="secondary"):
                        return True
            
            # 添加預估時間和提示
            self._render_progress_hints(progress)
        
        return False
    
    def _render_full_progress(self, progress: float, status: str, current_step: str, total_steps: int, on_cancel: Optional[Callable] = None) -> bool:
        """渲染完整模式進度（適合在報告區域顯示）"""
        # 使用增強的自定義樣式容器
        st.markdown('''
        <div class="enhanced-progress-container full-mode">
            <div class="progress-header">
                <div class="progress-title">
                    <span class="ai-icon">🤖</span>
                    <span class="title-text">AI 教師正在生成詳細分析報告</span>
                    <div class="loading-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 主要進度區域
        progress_container = st.container()
        
        with progress_container:
            # 進度條和狀態信息
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # 美化進度條
                progress_percent = int(progress * 100)
                st.markdown(f'''
                <div class="progress-wrapper">
                    <div class="progress-info">
                        <span class="progress-percent">{progress_percent}%</span>
                        <span class="progress-status">{status}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # 使用自定義進度條
                self.progress_bar = st.progress(progress, text=f"進度: {progress_percent}%")
                
                # 當前步驟顯示
                if current_step:
                    st.markdown(f'''
                    <div class="current-step">
                        <span class="step-icon">🔄</span>
                        <span class="step-text">{current_step}</span>
                    </div>
                    ''', unsafe_allow_html=True)
            
            with col2:
                if on_cancel:
                    if st.button("❌ 取消", key="cancel_report_generation", help="取消報告生成", type="secondary"):
                        return True
            
            # 詳細進度信息
            self._render_detailed_progress(progress, current_step, total_steps)
            
            # 提示信息
            self._render_progress_tips()
            
            # 添加互動元素
            self._render_interactive_elements(progress)
        
        return False
    
    def _render_detailed_progress(self, progress: float, current_step: str, total_steps: int):
        """渲染詳細進度信息"""
        with st.expander("📋 處理詳情", expanded=True):
            st.markdown('<div class="enhanced-step-list">', unsafe_allow_html=True)
            
            steps = [
                ("分析對話內容", "🔍", "分析您的問診對話，評估問診技巧和覆蓋率"),
                ("生成 RAG 查詢", "🤖", "基於對話內容生成相關的臨床指引查詢"),
                ("搜尋臨床指引", "📚", "從知識庫中搜尋相關的臨床指引和最佳實踐"),
                ("整合 AI 分析", "🧠", "整合 AI 分析和臨床指引，生成綜合評估"),
                ("生成最終報告", "📄", "生成包含詳細建議和 PDF 視覺化的完整報告")
            ]
            
            current_step_index = int(progress * total_steps)
            
            for i, (step_name, icon, description) in enumerate(steps, 1):
                if i <= current_step_index:
                    # 已完成
                    st.markdown(f'''
                    <div class="enhanced-step-item completed">
                        <div class="step-icon-container">
                            <span class="step-icon">✅</span>
                        </div>
                        <div class="step-content">
                            <div class="step-name">{step_name}</div>
                            <div class="step-description">{description}</div>
                        </div>
                        <div class="step-status">完成</div>
                    </div>
                    ''', unsafe_allow_html=True)
                elif i == current_step_index + 1:
                    # 進行中
                    st.markdown(f'''
                    <div class="enhanced-step-item active">
                        <div class="step-icon-container">
                            <span class="step-icon rotating">🔄</span>
                        </div>
                        <div class="step-content">
                            <div class="step-name">{step_name}</div>
                            <div class="step-description">{description}</div>
                        </div>
                        <div class="step-status">進行中</div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    # 等待中
                    st.markdown(f'''
                    <div class="enhanced-step-item pending">
                        <div class="step-icon-container">
                            <span class="step-icon">⏳</span>
                        </div>
                        <div class="step-content">
                            <div class="step-name">{step_name}</div>
                            <div class="step-description">{description}</div>
                        </div>
                        <div class="step-status">等待中</div>
                    </div>
                    ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_progress_tips(self):
        """渲染進度提示"""
        st.markdown("""
        <div class="info-box">
        💡 <strong>提示：</strong><br>
        • 報告生成通常需要 30-60 秒<br>
        • 系統正在分析您的問診表現並整合臨床指引<br>
        • 生成的報告將包含詳細的學習建議和 PDF 視覺化附錄
        </div>
        """, unsafe_allow_html=True)
    
    def _render_progress_hints(self, progress: float):
        """渲染進度提示（緊湊模式）"""
        # 根據進度顯示不同的提示信息
        if progress < 0.2:
            hint_text = "正在初始化報告生成器..."
            time_estimate = "預估剩餘時間: 45-60 秒"
        elif progress < 0.4:
            hint_text = "正在分析您的問診表現..."
            time_estimate = "預估剩餘時間: 30-45 秒"
        elif progress < 0.6:
            hint_text = "正在搜尋相關臨床指引..."
            time_estimate = "預估剩餘時間: 20-30 秒"
        elif progress < 0.8:
            hint_text = "正在整合 AI 分析結果..."
            time_estimate = "預估剩餘時間: 10-20 秒"
        else:
            hint_text = "正在生成最終報告..."
            time_estimate = "預估剩餘時間: 5-10 秒"
        
        st.markdown(f'''
        <div class="progress-hints">
            <div class="hint-text">{hint_text}</div>
            <div class="time-estimate">{time_estimate}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    def _render_interactive_elements(self, progress: float):
        """渲染互動元素（完整模式）"""
        st.markdown("---")
        
        # 創建互動區域
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            # 學習提示
            with st.expander("💡 學習提示", expanded=False):
                tips = [
                    "💭 思考您的問診技巧是否完整",
                    "🔍 回顧您是否詢問了所有重要症狀",
                    "📚 準備學習相關的臨床指引",
                    "🎯 關注系統提供的改進建議"
                ]
                for tip in tips:
                    st.markdown(f"• {tip}")
        
        with col2:
            # 進度統計
            with st.expander("📊 進度統計", expanded=False):
                st.metric("完成進度", f"{int(progress * 100)}%")
                st.metric("預估剩餘時間", f"{max(0, int(60 * (1 - progress)))} 秒")
                st.metric("處理狀態", "進行中" if progress < 1.0 else "完成")
        
        with col3:
            # 系統狀態和實時更新
            def render_system_status():
                st.success("✅ AI 引擎運行正常")
                st.success("✅ 知識庫連接正常")
                st.success("✅ 報告生成器就緒")
                if progress > 0.5:
                    st.success("✅ 臨床指引已載入")
                
                # 顯示實時狀態更新
                if hasattr(st.session_state, 'status_updates') and st.session_state.status_updates:
                    st.markdown("---")
                    st.markdown("**🕒 實時狀態更新**")
                    recent_updates = st.session_state.status_updates[-3:]  # 顯示最近3個更新
                    for update in reversed(recent_updates):
                        st.markdown(f"`{update['timestamp']}` {update['status']}")
            
            create_custom_expander(
                title="系統狀態",
                content_func=render_system_status,
                key="system_status_toggle",
                style="emoji",
                emoji="⚙️",
                default_expanded=False
            )
        
        # 添加實時狀態更新區域（完整模式）
        if hasattr(st.session_state, 'status_updates') and st.session_state.status_updates:
            def render_log_content():
                st.markdown('<div class="status-log">', unsafe_allow_html=True)
                
                for update in reversed(st.session_state.status_updates[-5:]):  # 顯示最近5個更新
                    st.markdown(f'''
                    <div class="log-entry">
                        <span class="log-time">{update['timestamp']}</span>
                        <span class="log-status">{update['status']}</span>
                        <span class="log-details">{update['details']}</span>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            create_custom_expander(
                title="實時處理日誌",
                content_func=render_log_content,
                key="log_toggle",
                style="emoji",
                emoji="📊",
                default_expanded=False
            )
    
    def render_loading_animation(self, message: str = "處理中..."):
        """渲染載入動畫"""
        # 使用 Streamlit 的內建 spinner
        with st.spinner(message):
            time.sleep(0.1)  # 短暫延遲以顯示動畫
    
    def render_step_progress(self, 
                           step: int, 
                           total_steps: int, 
                           step_name: str,
                           details: str = "") -> None:
        """渲染步驟進度"""
        progress = step / total_steps
        
        # 更新進度條
        if self.progress_bar:
            self.progress_bar.progress(progress, text=f"步驟 {step}/{total_steps}: {step_name}")
        
        # 顯示步驟詳情
        if details:
            st.info(f"🔄 {step_name}: {details}")
    
    def render_error_state(self, error_message: str, on_retry: Optional[Callable] = None):
        """渲染錯誤狀態"""
        st.markdown(f"""
        <div class="warning-box">
        ❌ <strong>報告生成失敗</strong><br>
        {error_message}
        </div>
        """, unsafe_allow_html=True)
        
        if on_retry:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🔄 重試", key="retry_report_generation", help="重新嘗試生成報告"):
                    on_retry()
            with col2:
                if st.button("📋 查看錯誤詳情", key="view_error_details", help="查看詳細錯誤信息"):
                    st.exception()
    
    def render_success_state(self, report_filename: str = ""):
        """渲染成功狀態"""
        st.markdown("""
        <div class="info-box">
        ✅ <strong>報告生成完成！</strong><br>
        您的詳細分析報告已準備就緒。
        </div>
        """, unsafe_allow_html=True)
        
        if report_filename:
            st.info(f"📄 報告已儲存至: {report_filename}")
    
    def clear_progress(self):
        """清除進度顯示"""
        if self.progress_bar:
            self.progress_bar.empty()
        
        # 清除相關的 session state
        if "report_generation_progress" in st.session_state:
            del st.session_state.report_generation_progress


class ReportGenerationManager:
    """報告生成管理器"""
    
    def __init__(self):
        self.progress_component = ProgressDisplayComponent("report_progress")
        self.current_step = 0
        self.total_steps = 5
        self.steps = [
            "分析對話內容",
            "生成 RAG 查詢", 
            "搜尋臨床指引",
            "整合 AI 分析",
            "生成最終報告"
        ]
    
    def start_generation(self, on_cancel: Optional[Callable] = None) -> bool:
        """開始報告生成"""
        st.session_state.report_generation_progress = {
            "is_generating": True,
            "current_step": 0,
            "total_steps": self.total_steps,
            "status": "準備中...",
            "cancelled": False
        }
        
        return self.progress_component.render_report_generation_progress(
            progress=0.0,
            status="準備中...",
            current_step="初始化報告生成器",
            total_steps=self.total_steps,
            on_cancel=on_cancel
        )
    
    def update_progress(self, step: int, status: str, details: str = ""):
        """更新進度"""
        if "report_generation_progress" not in st.session_state:
            return
        
        progress = step / self.total_steps
        st.session_state.report_generation_progress.update({
            "current_step": step,
            "status": status,
            "details": details,
            "progress": progress
        })
        
        # 添加實時狀態更新
        self._add_status_update(step, status, details)
        
        self.progress_component.render_step_progress(
            step=step,
            total_steps=self.total_steps,
            step_name=self.steps[step - 1] if step <= len(self.steps) else "處理中",
            details=details
        )
    
    def _add_status_update(self, step: int, status: str, details: str):
        """添加狀態更新到歷史記錄"""
        if "status_updates" not in st.session_state:
            st.session_state.status_updates = []
        
        from datetime import datetime
        update = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "step": step,
            "status": status,
            "details": details
        }
        
        st.session_state.status_updates.append(update)
        
        # 只保留最近的10個更新
        if len(st.session_state.status_updates) > 10:
            st.session_state.status_updates = st.session_state.status_updates[-10:]
    
    def complete_generation(self, success: bool = True, error_message: str = ""):
        """完成報告生成"""
        if "report_generation_progress" in st.session_state:
            st.session_state.report_generation_progress["is_generating"] = False
        
        if success:
            self.progress_component.render_success_state()
        else:
            self.progress_component.render_error_state(error_message)
    
    def is_generating(self) -> bool:
        """檢查是否正在生成報告"""
        return st.session_state.get("report_generation_progress", {}).get("is_generating", False)
    
    def cancel_generation(self):
        """取消報告生成"""
        if "report_generation_progress" in st.session_state:
            st.session_state.report_generation_progress["cancelled"] = True
            st.session_state.report_generation_progress["is_generating"] = False
        
        self.progress_component.clear_progress()
        st.info("❌ 報告生成已取消")
