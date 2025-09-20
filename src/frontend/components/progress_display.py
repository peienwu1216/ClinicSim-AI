"""
進度顯示組件
用於顯示報告生成過程中的進度和狀態
"""

import streamlit as st
import time
from typing import Optional, Callable, Dict, Any
from .base import BaseComponent
from .styles import apply_custom_css


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
        # 使用簡潔的樣式
        st.markdown('<div class="progress-container" style="margin-top: 20px; padding: 15px;">', unsafe_allow_html=True)
        
        # 標題和進度條
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown("**🤖 AI 教師正在生成詳細分析報告...**")
            self.progress_bar = st.progress(progress, text=f"{int(progress * 100)}%")
            st.caption(f"📋 {status}")
        
        with col2:
            if on_cancel:
                if st.button("❌ 取消", key="cancel_report_generation_compact", help="取消報告生成"):
                    st.markdown('</div>', unsafe_allow_html=True)
                    return True
        
        # 簡化的步驟顯示
        if current_step:
            st.info(f"🔄 {current_step}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    
    def _render_full_progress(self, progress: float, status: str, current_step: str, total_steps: int, on_cancel: Optional[Callable] = None) -> bool:
        """渲染完整模式進度（適合在報告區域顯示）"""
        # 使用自定義樣式的容器
        st.markdown('<div class="progress-container">', unsafe_allow_html=True)
        
        # 標題
        st.markdown("### 🤖 AI 教師正在生成詳細分析報告")
        st.markdown("---")
        
        # 進度條
        self.progress_bar = st.progress(progress, text=f"{int(progress * 100)}%")
        
        # 狀態信息
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'<div class="status-indicator"><strong>狀態：</strong> {status}</div>', unsafe_allow_html=True)
            if current_step:
                st.markdown(f'<div class="status-indicator"><strong>當前步驟：</strong> {current_step}</div>', unsafe_allow_html=True)
        
        with col2:
            if on_cancel:
                if st.button("❌ 取消", key="cancel_report_generation", help="取消報告生成"):
                    st.markdown('</div>', unsafe_allow_html=True)
                    return True
        
        # 詳細進度信息
        self._render_detailed_progress(progress, current_step, total_steps)
        
        # 提示信息
        self._render_progress_tips()
        
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    
    def _render_detailed_progress(self, progress: float, current_step: str, total_steps: int):
        """渲染詳細進度信息"""
        with st.expander("📋 處理詳情", expanded=True):
            st.markdown('<div class="step-list">', unsafe_allow_html=True)
            
            steps = [
                "分析對話內容",
                "生成 RAG 查詢",
                "搜尋臨床指引",
                "整合 AI 分析",
                "生成最終報告"
            ]
            
            for i, step in enumerate(steps, 1):
                if i <= int(progress * total_steps):
                    st.markdown(f'<div class="step-item"><span class="step-icon">✅</span><span class="step-text">{step}</span></div>', unsafe_allow_html=True)
                elif i == int(progress * total_steps) + 1:
                    st.markdown(f'<div class="step-item"><span class="step-icon">🔄</span><span class="step-text">{step} (進行中...)</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="step-item"><span class="step-icon">⏳</span><span class="step-text">{step}</span></div>', unsafe_allow_html=True)
            
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
            "status": status
        })
        
        self.progress_component.render_step_progress(
            step=step,
            total_steps=self.total_steps,
            step_name=self.steps[step - 1] if step <= len(self.steps) else "處理中",
            details=details
        )
    
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
