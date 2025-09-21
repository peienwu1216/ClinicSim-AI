"""
側邊欄組件
"""

import streamlit as st
from typing import Optional, Callable

from .base import BaseComponent
from .custom_toggle import create_custom_expander


class SidebarComponent(BaseComponent):
    """側邊欄組件"""
    
    def render(self, 
               coverage: int = 0,
               vital_signs: Optional[dict] = None,
               session_ended: bool = False,
               on_end_session: Optional[Callable] = None,
               on_generate_detailed_report: Optional[Callable] = None,
               detailed_report_available: bool = False,
               on_select_random_case: Optional[Callable] = None,
               current_case_id: Optional[str] = None,
               has_started: bool = False) -> None:
        """渲染側邊欄"""
        
        # 添加最簡單的 JavaScript 來確保佈局正確
        st.markdown("""
        <script>
        function fixLayout() {
            // 確保主內容區域有正確的邊距
            const mainContainer = document.querySelector('.main .block-container');
            if (mainContainer) {
                mainContainer.style.marginLeft = '350px';
                mainContainer.style.maxWidth = 'calc(100vw - 350px)';
            }
        }
        
        // 立即執行
        fixLayout();
        
        // 定期檢查
        setInterval(fixLayout, 500);
        </script>
        """, unsafe_allow_html=True)

        with st.sidebar:
            # 標題
            st.title("🧑‍⚕️ ClinicSim AI - 臨床診斷考試訓練系統")
            st.info("AI-powered Clinical Skills Training Platform for Medical Students OSCE MOCK EXAM")
            
            # 病例選擇
            self._render_case_selection(on_select_random_case, current_case_id, session_ended, has_started)
            
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
        st.subheader("📊 問診覆蓋率")
        # 確保覆蓋率在 0-100 範圍內，並轉換為 0-1 的小數
        normalized_coverage = max(0, min(100, coverage)) / 100
        st.progress(normalized_coverage, text=f"{coverage}%")
        st.caption("根據提問即時更新")
    
    def _render_vital_signs_monitor(self, vital_signs: Optional[dict]) -> None:
        """渲染生命體徵監視器"""
        st.subheader("💓 生命體徵")
        
        if vital_signs:
            # 使用兩欄佈局來顯示
            col1, col2 = st.columns(2)
            
            col1.metric("心率", f"{vital_signs.get('HR_bpm', 'N/A')} bpm", delta_color="inverse")
            col1.metric("血氧", f"{vital_signs.get('SpO2_room_air', 'N/A')}%", delta_color="inverse")
            col2.metric("血壓", f"{vital_signs.get('BP_mmHg', 'N/A')} mmHg", delta_color="inverse")
            col2.metric("呼吸", f"{vital_signs.get('RR_bpm', 'N/A')} /min", delta_color="inverse")
        else:
            st.info("待測量")
    
    def _render_control_buttons(self, 
                               session_ended: bool,
                               on_end_session: Optional[Callable],
                               on_generate_detailed_report: Optional[Callable],
                               detailed_report_available: bool) -> None:
        """渲染控制按鈕"""
        
        # 結束問診按鈕
        if on_end_session and st.button("📋 總結與計畫", disabled=session_ended):
            on_end_session()
        
        # 詳細報告按鈕（只在問診結束後顯示）
        if session_ended and on_generate_detailed_report:
            st.markdown("---")
            st.button(
                "🤖 完整報告", 
                disabled=detailed_report_available,
                help="生成包含臨床指引的詳細分析報告",
                on_click=on_generate_detailed_report
            )
    
    def _render_case_selection(self, 
                              on_select_random_case: Optional[Callable],
                              current_case_id: Optional[str],
                              session_ended: bool = False,
                              has_started: bool = False) -> None:
        """渲染病例選擇區域"""
        st.subheader("📋 病例")
        
        # 顯示當前病例信息
        if current_case_id:
            case_display_name = current_case_id.replace("_", " ").title()
            st.info(f"**當前病例**: {case_display_name}")
        
        # 隨機選擇病例按鈕
        self._render_random_case_button(
            on_select_random_case, 
            session_ended, 
            has_started
        )
    
    def _render_random_case_button(self, 
                                  on_select_random_case: Optional[Callable],
                                  session_ended: bool = False,
                                  has_started: bool = False) -> None:
        """渲染隨機選擇病例按鈕"""
        
        # 根據狀態決定按鈕文字和可用性
        if session_ended:
            button_text = "🎲 隨機選擇新病例"
            button_help = "選擇一個新的隨機病例開始練習"
            disabled = False
            caption = "開始新一輪練習"
        elif has_started:
            button_text = "🎲 隨機選擇病例"
            button_help = "問診進行中，無法切換病例"
            disabled = True
            caption = "⚠️ 問診進行中，無法切換"
        else:
            button_text = "🎲 隨機選擇病例"
            button_help = "隨機選擇一個病例進行練習"
            disabled = False
            caption = "選擇病例進行練習"
        
        # 創建按鈕容器，用於顯示載入狀態
        button_container = st.container()
        
        with button_container:
            if on_select_random_case and st.button(
                button_text, 
                use_container_width=True, 
                disabled=disabled,
                help=button_help
            ):
                # 顯示載入狀態
                with st.spinner("🎲 正在隨機選擇病例..."):
                    # 顯示過渡動畫
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # 模擬載入步驟
                    steps = [
                        "正在獲取可用病例列表...",
                        "正在隨機選擇病例...",
                        "正在載入病例資料...",
                        "正在初始化問診環境...",
                        "完成！"
                    ]
                    
                    for i, step in enumerate(steps):
                        progress_bar.progress((i + 1) / len(steps))
                        status_text.text(step)
                        st.session_state._case_loading_step = step
                        # 短暫延遲以顯示載入效果
                        import time
                        time.sleep(0.3)
                    
                    # 調用實際的隨機選擇函數
                    on_select_random_case()
                    
                    # 清除載入狀態
                    progress_bar.empty()
                    status_text.empty()
                    st.success("✅ 病例切換成功！")
        
        # 顯示說明文字
        st.caption(caption)
    
    def _render_osce_tips(self) -> None:
        """渲染 OSCE 技巧小抄"""
        def render_osce_content():
            st.markdown("""
            **開場建議：**
            > 「您好，在您同意下，為您快速了解胸痛細節，目標是盡快找到原因並幫您舒服一些。」
            
            **關鍵決策指令範例：**
            > 「您現在的症狀是我們非常重視的警訊，我會**立刻安排 12 導程心電圖（在 10 分內完成）**與抽血檢驗，同時持續監測您的生命徵象。」
            
            **結尾總結建議：**
            > 「總結一下，目前高度懷疑是心臟的問題。我們會先做檢查，如果症狀加重，請立刻告訴我們。」
            """)
        
        create_custom_expander(
            title="OSCE 技巧小抄",
            content_func=render_osce_content,
            key="osce_tips_toggle",
            style="emoji",
            emoji="💡",
            default_expanded=False
        )
