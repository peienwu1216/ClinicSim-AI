"""
測試透明化 Toggle 修復效果
驗證 keyboard 文字是否變透明
"""

import streamlit as st
from src.frontend.components.transparent_toggle_fix import apply_transparent_toggle_fix_once

def main():
    st.set_page_config(
        page_title="透明化 Toggle 修復測試",
        page_icon="👻",
        layout="wide"
    )
    
    # 應用透明化修復
    apply_transparent_toggle_fix_once()
    
    st.title("👻 透明化 Toggle 修復測試")
    st.markdown("---")
    
    st.markdown("""
    ## 測試說明
    這個頁面用來測試透明化修復效果。如果修復成功，你不應該看到任何 "keyboard_arrow_down" 或類似的文字。
    即使文字存在，也會變透明讓你看不到。
    """)
    
    st.markdown("---")
    
    # 測試多個 expander
    st.subheader("🧪 測試多個 Expander")
    
    with st.expander("測試 Expander 1 - 應該看不到 keyboard 文字", expanded=False):
        st.markdown("**內容 1**")
        st.info("如果你看不到任何 keyboard 相關文字，修復就成功了！")
    
    with st.expander("測試 Expander 2 - 檢查圖標是否透明", expanded=False):
        st.markdown("**內容 2**")
        st.success("這個 expander 的圖標文字應該是透明的")
    
    with st.expander("測試 Expander 3 - 預設展開", expanded=True):
        st.markdown("**內容 3**")
        st.warning("這個 expander 預設展開，檢查圖標是否透明")
    
    # 測試不同的標題
    st.subheader("📝 測試不同標題")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("📊 數據分析", expanded=False):
            st.markdown("數據分析內容")
    
    with col2:
        with st.expander("⚙️ 系統設定", expanded=False):
            st.markdown("系統設定內容")
    
    # 測試長標題
    with st.expander("這是一個很長的標題用來測試 expander 的行為和圖標顯示", expanded=False):
        st.markdown("長標題測試內容")
    
    # 測試結果
    st.markdown("---")
    st.subheader("📊 測試結果檢查")
    
    st.markdown("""
    ### 檢查項目：
    - ✅ 是否還能看到 "keyboard_arrow_down" 文字？
    - ✅ 是否還能看到 "keyboard_double_arrow_down" 文字？
    - ✅ 是否還能看到其他 Material Icons 文字？
    - ✅ 所有 expander 是否正常展開/收合？
    - ✅ 標題文字是否正常顯示？
    
    ### 預期結果：
    - 所有 expander 都應該正常展開/收合
    - 不應該看到任何圖標文字（即使存在也是透明的）
    - 標題文字應該正常顯示
    - 功能完全正常
    """)
    
    # 互動測試
    st.markdown("---")
    st.subheader("🎮 互動測試")
    
    if st.button("重新載入頁面"):
        st.rerun()
    
    if st.button("清除 Session State"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # 顯示當前 session state
    if st.checkbox("顯示 Session State"):
        st.json(dict(st.session_state))
    
    # 技術說明
    st.markdown("---")
    st.subheader("🔧 技術說明")
    
    st.markdown("""
    ### 透明化修復原理：
    1. **CSS 透明化**: 使用 `opacity: 0` 和 `color: transparent` 讓文字變透明
    2. **JavaScript 動態處理**: 監控 DOM 變化，動態將新出現的文字變透明
    3. **多重保障**: CSS + JavaScript + 定期檢查，確保沒有遺漏
    4. **保留功能**: 只讓文字變透明，不影響 expander 的正常功能
    
    ### 優勢：
    - ✅ 文字完全透明，用戶看不到
    - ✅ 不影響 expander 的正常功能
    - ✅ 動態處理新出現的內容
    - ✅ 簡單有效的解決方案
    """)
    
    st.markdown("---")
    st.success("🎉 如果這個頁面運行正常且看不到任何 keyboard 文字，說明透明化修復成功！")

if __name__ == "__main__":
    main()
