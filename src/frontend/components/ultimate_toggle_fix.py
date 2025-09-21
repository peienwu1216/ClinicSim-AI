"""
終極 Toggle 修復組件
使用最強力的方法來隱藏 keyboard_arrow_down 文字
"""

import streamlit as st


def apply_ultimate_toggle_fix():
    """應用終極 toggle 修復"""
    
    st.markdown("""
    <style>
    /* 終極修復：隱藏所有可能的 keyboard 文字 */
    
    /* 1. 隱藏所有包含特定文字的元素 */
    [data-testid="stExpander"] .streamlit-expanderHeader * {
        font-family: 'Noto Sans TC', 'Inter', sans-serif !important;
    }
    
    /* 2. 強制隱藏所有 Material Icons 相關元素 */
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="material-icons"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="MuiIcon"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="material-symbols"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="expanderToggle"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="arrow"],
    [data-testid="stExpander"] .streamlit-expanderHeader *[class*="icon"],
    [data-testid="stExpander"] .streamlit-expanderHeader svg,
    [data-testid="stExpander"] .streamlit-expanderHeader .stExpanderToggleIcon,
    [data-testid="stExpander"] .streamlit-expanderHeader .streamlit-expanderToggle {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        z-index: -1 !important;
    }
    
    /* 3. 隱藏所有非第一個子元素（保留標題文字） */
    [data-testid="stExpander"] .streamlit-expanderHeader > *:not(:first-child) {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        z-index: -1 !important;
    }
    
    /* 4. 確保標題文字正常顯示 */
    [data-testid="stExpander"] .streamlit-expanderHeader > p:first-child,
    [data-testid="stExpander"] .streamlit-expanderHeader > div:first-child,
    [data-testid="stExpander"] .streamlit-expanderHeader > span:first-child {
        display: block !important;
        visibility: visible !important;
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
        position: static !important;
        left: auto !important;
        top: auto !important;
        z-index: auto !important;
    }
    
    /* 5. 隱藏所有可能的按鈕圖標 */
    [data-testid="stExpander"] button *[class*="icon"],
    [data-testid="stExpander"] button *[class*="arrow"],
    [data-testid="stExpander"] button *[class*="toggle"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        z-index: -1 !important;
    }
    
    /* 6. 隱藏所有包含特定文字的文本內容 */
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
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        z-index: -1 !important;
    }
    
    /* 7. 強制隱藏所有可能的圖標文字 */
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
        z-index: -1 !important;
    }
    
    /* 8. 確保 expander 標題只顯示文字 */
    [data-testid="stExpander"] .streamlit-expanderHeader {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        overflow: hidden !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 添加強力的 JavaScript 來移除所有圖標文字
    st.markdown("""
    <script>
    // 終極修復函數
    function ultimateToggleFix() {
        console.log('🔧 執行終極 Toggle 修復...');
        
        // 要移除的文字列表
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
            'chevron',
            'double_arrow',
            'toggle'
        ];
        
        // 查找所有 expander 元素
        const expanders = document.querySelectorAll('[data-testid="stExpander"]');
        console.log(`🔍 找到 ${expanders.length} 個 expander`);
        
        expanders.forEach(function(expander, index) {
            const header = expander.querySelector('.streamlit-expanderHeader');
            if (header) {
                console.log(`🔧 修復 expander ${index + 1}`);
                
                // 移除所有包含特定文字的元素
                textToRemove.forEach(function(text) {
                    const elements = header.querySelectorAll('*');
                    elements.forEach(function(element) {
                        if (element.textContent && element.textContent.includes(text)) {
                            console.log(`🗑️ 移除包含 "${text}" 的元素:`, element);
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
                
                // 移除所有非第一個子元素
                const children = Array.from(header.children);
                children.forEach(function(child, childIndex) {
                    if (childIndex > 0) { // 保留第一個元素（通常是標題文字）
                        console.log(`🗑️ 移除非第一個子元素 ${childIndex}:`, child);
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
                        console.log(`🗑️ 移除圖標元素:`, icon);
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
        
        console.log('✅ 終極 Toggle 修復完成');
    }
    
    // 等待頁面加載完成
    setTimeout(function() {
        ultimateToggleFix();
    }, 100);
    
    // 持續監控並修復新出現的圖標文字
    const observer = new MutationObserver(function(mutations) {
        let shouldFix = false;
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        if (node.matches && node.matches('[data-testid="stExpander"]')) {
                            shouldFix = true;
                        } else if (node.querySelectorAll) {
                            const expanders = node.querySelectorAll('[data-testid="stExpander"]');
                            if (expanders.length > 0) {
                                shouldFix = true;
                            }
                        }
                    }
                });
            }
        });
        
        if (shouldFix) {
            console.log('🔄 檢測到新的 expander，重新執行修復...');
            setTimeout(ultimateToggleFix, 50);
        }
    });
    
    // 開始監控 DOM 變化
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // 定期檢查（保險措施）
    setInterval(function() {
        const expanders = document.querySelectorAll('[data-testid="stExpander"]');
        let needsFix = false;
        
        expanders.forEach(function(expander) {
            const header = expander.querySelector('.streamlit-expanderHeader');
            if (header) {
                const elements = header.querySelectorAll('*');
                elements.forEach(function(element) {
                    if (element.textContent && element.textContent.includes('keyboard')) {
                        needsFix = true;
                    }
                });
            }
        });
        
        if (needsFix) {
            console.log('🔄 定期檢查發現需要修復的元素，重新執行修復...');
            ultimateToggleFix();
        }
    }, 2000);
    </script>
    """, unsafe_allow_html=True)


def apply_ultimate_toggle_fix_once():
    """只應用一次的終極 toggle 修復"""
    if "ultimate_toggle_fix_applied" not in st.session_state:
        apply_ultimate_toggle_fix()
        st.session_state.ultimate_toggle_fix_applied = True
        st.success("🔧 已應用終極 Toggle 修復")
