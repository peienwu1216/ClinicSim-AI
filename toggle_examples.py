"""
Toggle 按鈕解決方案示例
展示如何使用新的自定義 toggle 組件替代 Streamlit 的 st.expander
"""

import streamlit as st
from src.frontend.components.custom_toggle import create_custom_expander

def main():
    st.set_page_config(
        page_title="Toggle 解決方案示例",
        page_icon="🔄",
        layout="wide"
    )
    
    st.title("🔄 Toggle 按鈕解決方案示例")
    st.markdown("---")
    
    st.markdown("""
    ## 問題說明
    原本的 Streamlit `st.expander` 在某些環境下會將 toggle 圖標顯示為文字（如 "keyboard_double_arrow"），
    這會影響用戶體驗。我們提供了多種美觀的替代方案。
    """)
    
    st.markdown("---")
    
    # 示例 1: Emoji 樣式
    st.subheader("📁 示例 1: Emoji 樣式")
    
    def emoji_content():
        st.markdown("這是使用 Emoji 圖標的 toggle 內容。")
        st.info("📁 當收合時顯示資料夾圖標")
        st.info("📂 當展開時顯示開啟的資料夾圖標")
        st.code("create_custom_expander(title='檔案管理', content_func=content, key='emoji', style='emoji', emoji='📁')")
    
    create_custom_expander(
        title="檔案管理",
        content_func=emoji_content,
        key="emoji_example",
        style="emoji",
        emoji="📁",
        default_expanded=False
    )
    
    # 示例 2: Unicode 箭頭樣式
    st.subheader("▶️ 示例 2: Unicode 箭頭樣式")
    
    def unicode_content():
        st.markdown("這是使用 Unicode 箭頭的 toggle 內容。")
        st.info("▶ 當收合時顯示右箭頭")
        st.info("▼ 當展開時顯示下箭頭")
        st.code("create_custom_expander(title='設定選項', content_func=content, key='unicode', style='unicode')")
    
    create_custom_expander(
        title="設定選項",
        content_func=unicode_content,
        key="unicode_example",
        style="unicode",
        default_expanded=False
    )
    
    # 示例 3: 箭頭符號樣式
    st.subheader("🔸 示例 3: 箭頭符號樣式")
    
    def arrow_content():
        st.markdown("這是使用箭頭符號的 toggle 內容。")
        st.info("🔸 當收合時顯示菱形")
        st.info("🔽 當展開時顯示下箭頭")
        st.code("create_custom_expander(title='進階設定', content_func=content, key='arrows', style='arrows')")
    
    create_custom_expander(
        title="進階設定",
        content_func=arrow_content,
        key="arrow_example",
        style="arrows",
        default_expanded=False
    )
    
    # 示例 4: 加減號樣式
    st.subheader("➕ 示例 4: 加減號樣式")
    
    def plus_minus_content():
        st.markdown("這是使用加減號的 toggle 內容。")
        st.info("➕ 當收合時顯示加號")
        st.info("➖ 當展開時顯示減號")
        st.code("create_custom_expander(title='項目列表', content_func=content, key='plus_minus', style='plus_minus')")
    
    create_custom_expander(
        title="項目列表",
        content_func=plus_minus_content,
        key="plus_minus_example",
        style="plus_minus",
        default_expanded=False
    )
    
    # 示例 5: 自定義圖標對樣式
    st.subheader("👁️ 示例 5: 自定義圖標對樣式")
    
    def icon_content():
        st.markdown("這是使用自定義圖標對的 toggle 內容。")
        st.info("🙈 當收合時顯示閉眼猴子")
        st.info("👁️ 當展開時顯示眼睛")
        st.code("create_custom_expander(title='隱私設定', content_func=content, key='icons', style='icons', icon_pair=('👁️', '🙈'))")
    
    create_custom_expander(
        title="隱私設定",
        content_func=icon_content,
        key="icon_example",
        style="icons",
        icon_pair=("👁️", "🙈"),
        default_expanded=False
    )
    
    # 示例 6: 文字樣式
    st.subheader("📝 示例 6: 文字樣式")
    
    def text_content():
        st.markdown("這是使用文字的 toggle 內容。")
        st.info("[展開] 當收合時顯示")
        st.info("[收合] 當展開時顯示")
        st.code("create_custom_expander(title='詳細資訊', content_func=content, key='text', style='text')")
    
    create_custom_expander(
        title="詳細資訊",
        content_func=text_content,
        key="text_example",
        style="text",
        default_expanded=False
    )
    
    # 示例 7: 實際應用場景
    st.markdown("---")
    st.subheader("🏥 實際應用場景")
    
    # 醫療檢查項目
    def medical_orders_content():
        st.markdown("**檢查項目：**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("🩺 心電圖檢查", key="ecg_btn")
            st.button("💉 血液檢查", key="blood_btn")
            st.button("🔬 尿液檢查", key="urine_btn")
        
        with col2:
            st.button("📷 X光檢查", key="xray_btn")
            st.button("🧠 CT掃描", key="ct_btn")
            st.button("🔍 超音波檢查", key="ultrasound_btn")
    
    create_custom_expander(
        title="醫療檢查項目",
        content_func=medical_orders_content,
        key="medical_orders",
        style="arrows",
        default_expanded=False
    )
    
    # 報告摘要
    def report_summary_content():
        st.markdown("**報告摘要：**")
        
        st.metric("問診表現", "85分", "↑ 5分")
        st.metric("臨床決策", "78分", "↑ 3分")
        st.metric("知識應用", "92分", "↑ 8分")
        
        st.markdown("**改進建議：**")
        st.markdown("- 加強病史詢問的完整性")
        st.markdown("- 提高鑑別診斷的準確性")
        st.markdown("- 優化治療方案的選擇")
    
    create_custom_expander(
        title="學習報告摘要",
        content_func=report_summary_content,
        key="report_summary",
        style="emoji",
        emoji="📊",
        default_expanded=True  # 預設展開
    )
    
    # 使用說明
    st.markdown("---")
    st.subheader("📚 使用說明")
    
    st.markdown("""
    ### 如何在你的組件中使用新的 Toggle 方案：
    
    1. **導入組件**：
       ```python
       from .custom_toggle import create_custom_expander
       ```
    
    2. **替換 st.expander**：
       ```python
       # 原本的寫法
       with st.expander("標題", expanded=False):
           # 內容
       
       # 新的寫法
       def render_content():
           # 內容
       
       create_custom_expander(
           title="標題",
           content_func=render_content,
           key="unique_key",
           style="emoji",  # 選擇樣式
           emoji="📁",     # 可選參數
           default_expanded=False
       )
       ```
    
    3. **可用的樣式**：
       - `"emoji"`: Emoji 圖標樣式
       - `"unicode"`: Unicode 箭頭樣式
       - `"arrows"`: 箭頭符號樣式
       - `"plus_minus"`: 加減號樣式
       - `"icons"`: 自定義圖標對樣式
       - `"text"`: 文字樣式
    
    4. **優點**：
       - ✅ 解決圖標文字問題
       - ✅ 提供多種美觀樣式
       - ✅ 完全自定義外觀
       - ✅ 保持原有功能
       - ✅ 易於使用和維護
    """)
    
    st.markdown("---")
    st.success("🎉 現在你的專案中所有的 toggle 按鈕都會顯示美觀的圖標，而不是文字了！")

if __name__ == "__main__":
    main()
