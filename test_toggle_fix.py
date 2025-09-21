"""
測試 Toggle 修復效果
驗證所有 keyboard_arrow_down 文字是否已被隱藏
"""

import streamlit as st
from src.frontend.components.global_toggle_fix import apply_global_toggle_fix_once
from src.frontend.components.custom_toggle import create_custom_expander

def main():
    st.set_page_config(
        page_title="Toggle 修復測試",
        page_icon="🔧",
        layout="wide"
    )
    
    # 應用全域修復
    apply_global_toggle_fix_once()
    
    st.title("🔧 Toggle 修復測試")
    st.markdown("---")
    
    st.markdown("""
    ## 測試說明
    這個頁面用來測試 toggle 按鈕修復效果。如果修復成功，你不應該看到任何 "keyboard_arrow_down" 或類似的文字。
    """)
    
    st.markdown("---")
    
    # 測試 1: 原始的 st.expander（應該被修復）
    st.subheader("🧪 測試 1: 原始 st.expander")
    st.markdown("如果修復成功，下面的 expander 應該沒有圖標文字：")
    
    with st.expander("原始 Streamlit Expander 測試", expanded=False):
        st.markdown("這是原始的 `st.expander` 內容。")
        st.info("如果你看不到任何 'keyboard_arrow_down' 文字，修復就成功了！")
        st.code("with st.expander('標題', expanded=False):\n    # 內容")
    
    # 測試 2: 自定義 toggle
    st.subheader("🎨 測試 2: 自定義 Toggle")
    st.markdown("這是我們的自定義 toggle 組件：")
    
    def custom_content():
        st.markdown("這是自定義 toggle 的內容。")
        st.success("這個 toggle 使用美觀的圖標，不會有文字問題！")
        st.code("create_custom_expander(title='標題', content_func=content, key='key', style='emoji')")
    
    create_custom_expander(
        title="自定義 Toggle 測試",
        content_func=custom_content,
        key="custom_toggle_test",
        style="emoji",
        emoji="🎨",
        default_expanded=False
    )
    
    # 測試 3: 多個 expander
    st.subheader("📚 測試 3: 多個 Expander")
    st.markdown("測試多個 expander 的修復效果：")
    
    with st.expander("測試 Expander 1", expanded=False):
        st.markdown("**內容 1**")
        st.info("第一個 expander")
    
    with st.expander("測試 Expander 2", expanded=False):
        st.markdown("**內容 2**")
        st.success("第二個 expander")
    
    with st.expander("測試 Expander 3", expanded=True):
        st.markdown("**內容 3**")
        st.warning("第三個 expander（預設展開）")
    
    # 測試 4: 混合使用
    st.subheader("🔄 測試 4: 混合使用")
    st.markdown("原始 expander 和自定義 toggle 混合使用：")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**原始 expander:**")
        with st.expander("原始", expanded=False):
            st.markdown("原始內容")
    
    with col2:
        st.markdown("**自定義 toggle:**")
        def mixed_content():
            st.markdown("自定義內容")
        
        create_custom_expander(
            title="自定義",
            content_func=mixed_content,
            key="mixed_toggle_test",
            style="arrows",
            default_expanded=False
        )
    
    # 測試結果
    st.markdown("---")
    st.subheader("📊 測試結果")
    
    st.markdown("""
    ### 檢查項目：
    - ✅ 是否還有 "keyboard_arrow_down" 文字？
    - ✅ 是否還有 "keyboard_double_arrow_down" 文字？
    - ✅ 是否還有其他 Material Icons 文字？
    - ✅ 原始 expander 是否正常運作？
    - ✅ 自定義 toggle 是否美觀？
    
    ### 預期結果：
    - 所有 expander 都應該正常展開/收合
    - 不應該看到任何圖標文字
    - 自定義 toggle 應該顯示美觀的圖標
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
    
    st.markdown("---")
    st.success("🎉 如果這個頁面運行正常且沒有圖標文字，說明修復成功！")

if __name__ == "__main__":
    main()
