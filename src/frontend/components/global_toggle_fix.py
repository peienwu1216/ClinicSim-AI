"""
全域 Toggle 修復組件
徹底解決 Streamlit expander 圖標文字問題
"""

import streamlit as st


def apply_global_toggle_fix():
    """應用全域 toggle 修復 CSS 和 JavaScript"""
    
    st.markdown("""
    <style>
    /* 全域隱藏所有 Streamlit expander 的圖標文字 */
    
    /* 隱藏所有 expander 相關的圖標文字 */
    [data-testid="stExpander"] .streamlit-expanderHeader * {
        font-family: 'Noto Sans TC', 'Inter', sans-serif !important;
    }
    
    /* 強制隱藏所有包含 Material Icons 文字的元素 */
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="material-icons"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="MuiIcon"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="material-symbols"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* 隱藏所有可能的展開圖標元素 */
    [data-testid="stExpander"] .streamlit-expanderHeader [class*="expanderToggle"],
    [data-testid="stExpander"] .streamlit-expanderHeader [class*="arrow"],
    [data-testid="stExpander"] .streamlit-expanderHeader [class*="icon"],
    [data-testid="stExpander"] .streamlit-expanderHeader svg,
    [data-testid="stExpander"] .streamlit-expanderHeader .stExpanderToggleIcon,
    [data-testid="stExpander"] .streamlit-expanderHeader .streamlit-expanderToggle {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* 隱藏所有包含特定文字的文本節點 */
    [data-testid="stExpander"] .streamlit-expanderHeader {
        position: relative !important;
    }
    
    [data-testid="stExpander"] .streamlit-expanderHeader::after {
        content: "" !important;
        display: none !important;
    }
    
    /* 隱藏 expander 標題中的所有子元素，只保留第一個文本節點 */
    [data-testid="stExpander"] .streamlit-expanderHeader > *:not(:first-child) {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* 強制隱藏所有可能的圖標容器 */
    [data-testid="stExpander"] .streamlit-expanderHeader .stIcon,
    [data-testid="stExpander"] .streamlit-expanderHeader .icon,
    [data-testid="stExpander"] .streamlit-expanderHeader .toggle-icon,
    [data-testid="stExpander"] .streamlit-expanderHeader .expander-icon {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* 隱藏所有可能的按鈕圖標 */
    [data-testid="stExpander"] button *[class*="icon"],
    [data-testid="stExpander"] button *[class*="arrow"],
    [data-testid="stExpander"] button *[class*="toggle"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* 確保 expander 標題只顯示文字 */
    [data-testid="stExpander"] .streamlit-expanderHeader {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        overflow: hidden !important;
    }
    
    [data-testid="stExpander"] .streamlit-expanderHeader > p:first-child {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* 隱藏所有其他可能的元素 */
    [data-testid="stExpander"] .streamlit-expanderHeader > *:not(p:first-child) {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
    }
    
    /* 強制隱藏所有可能的圖標文字 */
    [data-testid="stExpander"] *[aria-label*="keyboard"],
    [data-testid="stExpander"] *[aria-label*="arrow"],
    [data-testid="stExpander"] *[title*="keyboard"],
    [data-testid="stExpander"] *[title*="arrow"],
    [data-testid="stExpander"] *[alt*="keyboard"],
    [data-testid="stExpander"] *[alt*="arrow"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* 隱藏所有包含特定文字的文本內容 */
    [data-testid="stExpander"] * {
        text-rendering: optimizeLegibility !important;
    }
    
    /* 讓所有包含 keyboard 文字的元素變透明 */
    [data-testid="stExpander"] .streamlit-expanderHeader *:contains("keyboard"),
    [data-testid="stExpander"] .streamlit-expanderHeader *:contains("arrow"),
    [data-testid="stExpander"] .streamlit-expanderHeader *:contains("expand"),
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
    
    /* 強制讓所有可能的圖標文字變透明 */
    [data-testid="stExpander"] .streamlit-expanderHeader span,
    [data-testid="stExpander"] .streamlit-expanderHeader div,
    [data-testid="stExpander"] .streamlit-expanderHeader p,
    [data-testid="stExpander"] .streamlit-expanderHeader i,
    [data-testid="stExpander"] .streamlit-expanderHeader em {
        font-size: inherit !important;
    }
    
    /* 隱藏所有非標題文字的元素 */
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
    
    /* 最後的保險：隱藏所有可能的圖標元素 */
    [data-testid="stExpander"] .streamlit-expanderHeader span:not(:first-child),
    [data-testid="stExpander"] .streamlit-expanderHeader div:not(:first-child),
    [data-testid="stExpander"] .streamlit-expanderHeader i,
    [data-testid="stExpander"] .streamlit-expanderHeader em,
    [data-testid="stExpander"] .streamlit-expanderHeader strong:not(:first-child) {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 添加強力的 JavaScript 來移除所有圖標文字
    st.markdown("""
    <script>
    // 等待頁面加載完成
    setTimeout(function() {
        // 移除所有包含特定文字的元素
        const textToRemove = [
            'keyboard_arrow_down',
            'keyboard_arrow_up', 
            'keyboard_double_arrow_down',
            'keyboard_double_arrow_up',
            'keyboard_arrow_right',
            'keyboard_arrow_left',
            'expand_more',
            'expand_less',
            'chevron_down',
            'chevron_up',
            'arrow_drop_down',
            'arrow_drop_up',
            'keyboard',
            'arrow',
            'expand',
            'chevron'
        ];
        
        // 查找所有 expander 元素
        const expanders = document.querySelectorAll('[data-testid="stExpander"]');
        
        expanders.forEach(function(expander) {
            const header = expander.querySelector('.streamlit-expanderHeader');
            if (header) {
                // 移除所有包含特定文字的元素
                textToRemove.forEach(function(text) {
                    const elements = header.querySelectorAll('*');
                    elements.forEach(function(element) {
                        if (element.textContent && element.textContent.includes(text)) {
                            element.style.display = 'none';
                            element.style.visibility = 'hidden';
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
                            element.style.position = 'absolute';
                            element.style.left = '-9999px';
                            element.style.top = '-9999px';
                            element.style.zIndex = '-1';
                        }
                    });
                });
                
                // 移除所有非文字的子元素
                const children = Array.from(header.children);
                children.forEach(function(child, index) {
                    if (index > 0) { // 保留第一個元素（通常是標題文字）
                        child.style.display = 'none';
                        child.style.visibility = 'hidden';
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
                        child.style.position = 'absolute';
                        child.style.left = '-9999px';
                        child.style.top = '-9999px';
                        child.style.zIndex = '-1';
                    }
                });
                
                // 移除所有包含圖標類別的元素
                const iconSelectors = [
                    '[class*="material-icons"]',
                    '[class*="MuiIcon"]',
                    '[class*="material-symbols"]',
                    '[class*="expanderToggle"]',
                    '[class*="arrow"]',
                    '[class*="icon"]',
                    'svg',
                    '.stExpanderToggleIcon',
                    '.streamlit-expanderToggle'
                ];
                
                iconSelectors.forEach(function(selector) {
                    const iconElements = header.querySelectorAll(selector);
                    iconElements.forEach(function(icon) {
                        icon.style.display = 'none';
                        icon.style.visibility = 'hidden';
                        icon.style.opacity = '0';
                        icon.style.color = 'transparent';
                        icon.style.background = 'transparent';
                        icon.style.border = 'none';
                        icon.style.outline = 'none';
                        icon.style.textShadow = 'none';
                        icon.style.fontSize = '0';
                        icon.style.lineHeight = '0';
                        icon.style.padding = '0';
                        icon.style.margin = '0';
                        icon.style.width = '0';
                        icon.style.height = '0';
                        icon.style.overflow = 'hidden';
                        icon.style.position = 'absolute';
                        icon.style.left = '-9999px';
                        icon.style.top = '-9999px';
                        icon.style.zIndex = '-1';
                    });
                });
            }
        });
        
        // 持續監控並移除新出現的圖標文字
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) { // Element node
                            const expanders = node.querySelectorAll ? node.querySelectorAll('[data-testid="stExpander"]') : [];
                            if (expanders.length === 0 && node.matches && node.matches('[data-testid="stExpander"]')) {
                                expanders.push(node);
                            }
                            
                            expanders.forEach(function(expander) {
                                const header = expander.querySelector('.streamlit-expanderHeader');
                                if (header) {
                                    textToRemove.forEach(function(text) {
                                        const elements = header.querySelectorAll('*');
                                        elements.forEach(function(element) {
                                            if (element.textContent && element.textContent.includes(text)) {
                                                element.style.display = 'none';
                                                element.style.visibility = 'hidden';
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
                                                element.style.position = 'absolute';
                                                element.style.left = '-9999px';
                                                element.style.top = '-9999px';
                                                element.style.zIndex = '-1';
                                            }
                                        });
                                    });
                                }
                            });
                        }
                    });
                }
            });
        });
        
        // 開始監控 DOM 變化
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
    }, 100);
    </script>
    """, unsafe_allow_html=True)


def apply_global_toggle_fix_once():
    """只應用一次的全域 toggle 修復（避免重複應用）"""
    if "global_toggle_fix_applied" not in st.session_state:
        apply_global_toggle_fix()
        st.session_state.global_toggle_fix_applied = True
