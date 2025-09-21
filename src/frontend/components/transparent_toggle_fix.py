"""
透明化 Toggle 修復組件
專門將 keyboard 文字變透明，讓用戶看不到
"""

import streamlit as st


def apply_transparent_toggle_fix():
    """應用透明化 toggle 修復"""
    
    st.markdown("""
    <style>
    /* 讓所有 expander 中的 keyboard 文字變透明 */
    [data-testid="stExpander"] .streamlit-expanderHeader * {
        /* 如果元素包含 keyboard 相關文字，讓它變透明 */
    }
    
    /* 強制隱藏所有包含 keyboard 文字的元素 */
    [data-testid="stExpander"] .streamlit-expanderHeader *:contains("keyboard") {
        opacity: 0 !important;
        color: transparent !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        text-shadow: none !important;
        font-size: 0 !important;
        line-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        visibility: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        z-index: -1 !important;
    }
    
    /* 隱藏所有包含 arrow 文字的元素 */
    [data-testid="stExpander"] .streamlit-expanderHeader *:contains("arrow") {
        opacity: 0 !important;
        color: transparent !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        text-shadow: none !important;
        font-size: 0 !important;
        line-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        visibility: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        z-index: -1 !important;
    }
    
    /* 隱藏所有包含 expand 文字的元素 */
    [data-testid="stExpander"] .streamlit-expanderHeader *:contains("expand") {
        opacity: 0 !important;
        color: transparent !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        text-shadow: none !important;
        font-size: 0 !important;
        line-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        visibility: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        z-index: -1 !important;
    }
    
    /* 隱藏所有包含 chevron 文字的元素 */
    [data-testid="stExpander"] .streamlit-expanderHeader *:contains("chevron") {
        opacity: 0 !important;
        color: transparent !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        text-shadow: none !important;
        font-size: 0 !important;
        line-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        visibility: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        z-index: -1 !important;
    }
    
    /* 隱藏所有可能的圖標類別 */
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="material-icons"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="MuiIcon"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="material-symbols"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="expanderToggle"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="arrow"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="icon"],
    [data-testid="stExpander"] .streamlit-expanderHeader svg,
    [data-testid="stExpander"] .streamlit-expanderHeader .stExpanderToggleIcon,
    [data-testid="stExpander"] .streamlit-expanderHeader .streamlit-expanderToggle {
        opacity: 0 !important;
        color: transparent !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        text-shadow: none !important;
        font-size: 0 !important;
        line-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        visibility: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        z-index: -1 !important;
    }
    
    /* 隱藏所有非第一個子元素（保留標題文字） */
    [data-testid="stExpander"] .streamlit-expanderHeader > *:not(:first-child) {
        opacity: 0 !important;
        color: transparent !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        text-shadow: none !important;
        font-size: 0 !important;
        line-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        visibility: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        z-index: -1 !important;
    }
    
    /* 確保標題文字正常顯示 */
    [data-testid="stExpander"] .streamlit-expanderHeader > p:first-child,
    [data-testid="stExpander"] .streamlit-expanderHeader > div:first-child,
    [data-testid="stExpander"] .streamlit-expanderHeader > span:first-child {
        opacity: 1 !important;
        color: inherit !important;
        background: transparent !important;
        font-size: inherit !important;
        line-height: inherit !important;
        padding: inherit !important;
        margin: inherit !important;
        width: auto !important;
        height: auto !important;
        overflow: visible !important;
        visibility: visible !important;
        position: static !important;
        left: auto !important;
        top: auto !important;
        z-index: auto !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 添加 JavaScript 來動態移除文字
    st.markdown("""
    <script>
    function makeTextTransparent() {
        // 查找所有 expander
        const expanders = document.querySelectorAll('[data-testid="stExpander"]');
        
        expanders.forEach(function(expander) {
            const header = expander.querySelector('.streamlit-expanderHeader');
            if (header) {
                // 查找所有包含特定文字的元素
                const textPatterns = ['keyboard', 'arrow', 'expand', 'chevron'];
                
                textPatterns.forEach(function(pattern) {
                    const elements = header.querySelectorAll('*');
                    elements.forEach(function(element) {
                        if (element.textContent && element.textContent.includes(pattern)) {
                            // 讓文字變透明
                            element.style.opacity = '0';
                            element.style.color = 'transparent';
                            element.style.background = 'transparent';
                            element.style.border = 'none';
                            element.style.outline = 'none';
                            element.style.textShadow = 'none';
                            element.style.fontSize = '0';
                            element.style.lineHeight = '0';
                            element.style.padding = '0';
                            element.style.margin = '0';
                            element.style.width = '0';
                            element.style.height = '0';
                            element.style.overflow = 'hidden';
                            element.style.visibility = 'hidden';
                            element.style.position = 'absolute';
                            element.style.left = '-9999px';
                            element.style.top = '-9999px';
                            element.style.zIndex = '-1';
                        }
                    });
                });
                
                // 隱藏所有非第一個子元素
                const children = Array.from(header.children);
                children.forEach(function(child, index) {
                    if (index > 0) {
                        child.style.opacity = '0';
                        child.style.color = 'transparent';
                        child.style.background = 'transparent';
                        child.style.border = 'none';
                        child.style.outline = 'none';
                        child.style.textShadow = 'none';
                        child.style.fontSize = '0';
                        child.style.lineHeight = '0';
                        child.style.padding = '0';
                        child.style.margin = '0';
                        child.style.width = '0';
                        child.style.height = '0';
                        child.style.overflow = 'hidden';
                        child.style.visibility = 'hidden';
                        child.style.position = 'absolute';
                        child.style.left = '-9999px';
                        child.style.top = '-9999px';
                        child.style.zIndex = '-1';
                    }
                });
            }
        });
    }
    
    // 頁面加載後執行
    setTimeout(makeTextTransparent, 100);
    
    // 監控 DOM 變化
    const observer = new MutationObserver(function(mutations) {
        let shouldUpdate = false;
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        if (node.matches && node.matches('[data-testid="stExpander"]')) {
                            shouldUpdate = true;
                        } else if (node.querySelectorAll) {
                            const expanders = node.querySelectorAll('[data-testid="stExpander"]');
                            if (expanders.length > 0) {
                                shouldUpdate = true;
                            }
                        }
                    }
                });
            }
        });
        
        if (shouldUpdate) {
            setTimeout(makeTextTransparent, 50);
        }
    });
    
    // 開始監控
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // 定期檢查（保險措施）
    setInterval(makeTextTransparent, 1000);
    </script>
    """, unsafe_allow_html=True)


def apply_transparent_toggle_fix_once():
    """只應用一次的透明化 toggle 修復"""
    if "transparent_toggle_fix_applied" not in st.session_state:
        apply_transparent_toggle_fix()
        st.session_state.transparent_toggle_fix_applied = True
