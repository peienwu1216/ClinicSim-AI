"""
測試終極 Toggle 修復
"""

import streamlit as st
from src.frontend.components.ultimate_toggle_fix import apply_ultimate_toggle_fix_once

def main():
    st.set_page_config(
        page_title="Toggle 修復測試",
        page_icon="🔧",
        layout="wide"
    )
    
    st.title("🔧 終極 Toggle 修復測試")
    
    # 應用修復
    apply_ultimate_toggle_fix_once()
    
    st.markdown("### 測試各種 Expander 組件")
    
    # 測試 1: 基本 expander
    with st.expander("📁 基本 Expander 測試", expanded=False):
        st.markdown("這是基本 expander 的內容")
        st.info("如果看不到 'keyboard_arrow_down' 文字，修復就成功了！")
    
    # 測試 2: 多個 expander
    with st.expander("📊 數據分析", expanded=False):
        st.markdown("數據分析內容")
        st.bar_chart([1, 2, 3, 4, 5])
    
    with st.expander("⚙️ 設定選項", expanded=False):
        st.markdown("設定選項內容")
        st.selectbox("選擇選項", ["選項1", "選項2", "選項3"])
    
    with st.expander("📋 詳細資訊", expanded=True):
        st.markdown("詳細資訊內容")
        st.code("print('Hello World')")
    
    # 測試 3: 動態 expander
    if st.button("🔄 創建動態 Expander"):
        with st.expander("🆕 動態 Expander", expanded=False):
            st.markdown("這是動態創建的 expander")
            st.success("動態 expander 創建成功！")
    
    # 測試 4: 嵌套 expander
    with st.expander("📂 嵌套 Expander 測試", expanded=False):
        st.markdown("外層 expander 內容")
        
        with st.expander("📁 內層 Expander 1", expanded=False):
            st.markdown("內層 expander 1 內容")
        
        with st.expander("📁 內層 Expander 2", expanded=False):
            st.markdown("內層 expander 2 內容")
    
    # 顯示修復狀態
    st.markdown("---")
    st.markdown("### 🔍 修復狀態檢查")
    
    if "ultimate_toggle_fix_applied" in st.session_state:
        st.success("✅ 終極 Toggle 修復已應用")
    else:
        st.error("❌ 終極 Toggle 修復未應用")
    
    # 顯示 JavaScript 檢查結果
    st.markdown("### 🧪 JavaScript 檢查")
    st.markdown("""
    <div id="check-result"></div>
    <script>
    setTimeout(function() {
        const expanders = document.querySelectorAll('[data-testid="stExpander"]');
        let hasKeyboardText = false;
        
        expanders.forEach(function(expander) {
            const header = expander.querySelector('.streamlit-expanderHeader');
            if (header) {
                const elements = header.querySelectorAll('*');
                elements.forEach(function(element) {
                    if (element.textContent && element.textContent.includes('keyboard')) {
                        hasKeyboardText = true;
                    }
                });
            }
        });
        
        const resultDiv = document.getElementById('check-result');
        if (hasKeyboardText) {
            resultDiv.innerHTML = '<div style="color: red; font-weight: bold;">❌ 仍然發現 keyboard 文字</div>';
        } else {
            resultDiv.innerHTML = '<div style="color: green; font-weight: bold;">✅ 沒有發現 keyboard 文字</div>';
        }
    }, 1000);
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
