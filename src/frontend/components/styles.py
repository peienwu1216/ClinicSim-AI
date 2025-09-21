"""
自定義 CSS 樣式
用於改善 UI 的視覺效果
"""

def get_custom_css():
    """返回自定義 CSS 樣式"""
    return """
    <style>
    /* --- 全局字體與顏色系統 --- */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Noto Sans TC', 'Inter', sans-serif;
    }
    
    /* 確保所有 Streamlit 組件使用正確的字體 */
    .stApp, .stApp * {
        font-family: 'Noto Sans TC', 'Inter', sans-serif !important;
    }
    
    /* 修復特殊符號顯示問題 */
    .stApp, .stApp * {
        text-rendering: optimizeLegibility !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }
    
    /* 強制覆蓋Streamlit默認樣式 */
    .stApp {
        background-color: #f8f9fa !important;
    }
    
    .main .block-container {
        background-color: transparent !important;
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 100% !important;
    }
    
    /* 移除所有可能的白色背景 */
    div[data-testid="stVerticalBlock"] {
        background-color: transparent !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        background-color: transparent !important;
    }
    
    /* 確保列容器沒有白色背景 */
    .stColumn {
        background-color: transparent !important;
        padding: 0 !important;
    }
    
    /* 移除列之間的間距和背景 */
    .stColumn > div {
        background-color: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* 強制移除所有列相關的白色背景 */
    div[data-testid="column"] {
        background-color: transparent !important;
        padding: 0 !important;
    }
    
    div[data-testid="column"] > div {
        background-color: transparent !important;
        padding: 0 !important;
    }
    
    /* 移除Streamlit默認的間距 */
    .stApp > div {
        padding-top: 0 !important;
    }
    
    /* 強制移除所有可能的白色背景 */
    .stApp > div > div {
        background-color: transparent !important;
    }
    
    .stApp > div > div > div {
        background-color: transparent !important;
    }
    
    /* 移除可能的空白容器 */
    .stApp > div > div > div > div {
        background-color: transparent !important;
    }
    
    /* 確保主容器沒有白色背景 */
    .main .block-container > div {
        background-color: transparent !important;
    }
    
    /* 移除可能的空白區域 */
    .stApp > div > div > div > div > div {
        background-color: transparent !important;
    }
    
    /* 針對Streamlit容器的強制透明背景 */
    .element-container {
        background-color: transparent !important;
    }
    
    .stMarkdown {
        background-color: transparent !important;
    }
    
    .stMarkdown > div {
        background-color: transparent !important;
    }
    
    /* 強制移除所有可能的白色背景容器 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: transparent !important;
    }
    
    [data-testid="stHorizontalBlock"] {
        background-color: transparent !important;
    }
    
    [data-testid="stHorizontalBlock"] > div {
        background-color: transparent !important;
    }
    
    /* 主色調系統 */
    :root {
        --primary-color: #2563eb; /* 專業藍 */
        --primary-light: #3b82f6;
        --primary-dark: #1d4ed8;
        --secondary-color: #f0f9ff; /* 淡藍背景 */
        --accent-color: #10b981; /* 成功綠 */
        --warning-color: #f59e0b; /* 警告橙 */
        --danger-color: #ef4444; /* 危險紅 */
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --text-muted: #9ca3af;
        --card-bg-color: #ffffff;
        --border-color: #e5e7eb;
        --border-light: #f3f4f6;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* --- 卡片式設計系統 --- */
    .clinical-card {
        background-color: var(--card-bg-color);
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    
    .clinical-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    .clinical-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 2px solid var(--border-light);
    }
    
    .clinical-card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
    }
    
    .clinical-card-subtitle {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin: 4px 0 0 0;
    }
    
    .clinical-icon {
        font-size: 1.5rem;
        color: var(--primary-color);
    }
    
    /* --- 按鈕系統 --- */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid var(--primary-color);
        background-color: var(--secondary-color);
        color: var(--primary-color);
        font-weight: 500;
        font-size: 0.875rem;
        padding: 8px 16px;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
    }
    
    .stButton > button:hover {
        background-color: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-sm);
    }
    
    /* 按鈕變體 */
    .btn-success {
        background-color: var(--accent-color) !important;
        border-color: var(--accent-color) !important;
        color: white !important;
    }
    
    .btn-warning {
        background-color: var(--warning-color) !important;
        border-color: var(--warning-color) !important;
        color: white !important;
    }
    
    .btn-danger {
        background-color: var(--danger-color) !important;
        border-color: var(--danger-color) !important;
        color: white !important;
    }
    
    /* --- 分頁系統 --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0 0;
        padding: 12px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding: 20px 0;
    }
    
    /* --- 修復 Expander 組件的 TOGGLE 符號顯示問題 --- */
    .streamlit-expanderHeader {
        font-family: 'Noto Sans TC', 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* 確保展開/摺疊符號正確顯示 */
    .streamlit-expanderHeader .streamlit-expanderHeaderButton {
        font-family: 'Noto Sans TC', 'Inter', sans-serif !important;
        font-size: 1rem !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    /* 修復展開符號 - 使用更兼容的符號 */
    .streamlit-expanderHeader .streamlit-expanderHeaderButton::before {
        content: "▼" !important;
        font-family: 'Noto Sans TC', 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        margin-right: 8px !important;
        transition: transform 0.3s ease !important;
        display: inline-block !important;
        width: 16px !important;
        height: 16px !important;
        line-height: 1 !important;
        text-align: center !important;
        vertical-align: middle !important;
    }
    
    /* 修復摺疊符號 - 使用更兼容的符號 */
    .streamlit-expanderHeader[aria-expanded="false"] .streamlit-expanderHeaderButton::before {
        content: "▶" !important;
        transform: rotate(0deg) !important;
    }
    
    .streamlit-expanderHeader[aria-expanded="true"] .streamlit-expanderHeaderButton::before {
        content: "▼" !important;
        transform: rotate(0deg) !important;
    }
    
    /* 
    ==============================================
    最簡單直接的佈局修復
    ==============================================
    */

    /* 強制主內容區域從側邊欄右側開始 */
    .main .block-container {
        margin-left: 350px !important;
        max-width: calc(100vw - 350px) !important;
    }
    
    /* 確保主內容區域本身也有正確的邊距 */
    .main {
        margin-left: 0 !important;
    }
    
    /* 聊天輸入框定位 */
    [data-testid="stChatInput"] {
        position: fixed !important;
        left: 350px !important;
        right: 25% !important;
        bottom: 0 !important;
    }
    
    /* 備用符號方案 - 如果Unicode符號無法顯示，使用ASCII符號 */
    @supports not (content: "▼") {
        .streamlit-expanderHeader .streamlit-expanderHeaderButton::before {
            content: "V" !important;
            font-weight: bold !important;
        }
        
        .streamlit-expanderHeader[aria-expanded="false"] .streamlit-expanderHeaderButton::before {
            content: ">" !important;
        }
        
        .streamlit-expanderHeader[aria-expanded="true"] .streamlit-expanderHeaderButton::before {
            content: "V" !important;
        }
    }
    
    /* 隱藏預設的符號 */
    .streamlit-expanderHeader .streamlit-expanderHeaderButton svg {
        display: none !important;
    }
    
    /* 美化 Expander 樣式 */
    .streamlit-expander {
        border: 1px solid #e9ecef !important;
        border-radius: 12px !important;
        margin: 12px 0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    }
    
    .streamlit-expanderHeader {
        background: #f8f9fa !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 12px 16px !important;
        border-bottom: 1px solid #e9ecef !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #e9ecef !important;
    }
    
    .streamlit-expanderContent {
        padding: 16px !important;
        background: #ffffff !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* --- 進度條樣式 --- */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent-color) 0%, #34d399 50%, var(--accent-color) 100%);
        border-radius: 12px;
    }
    
    /* 進度容器樣式 */
    .progress-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-md);
        margin: 16px 0;
    }
    
    /* 增強進度容器樣式 */
    .enhanced-progress-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 20px;
        padding: 24px;
        margin: 20px 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid #dee2e6;
        position: relative;
        overflow: hidden;
    }
    
    .enhanced-progress-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        animation: shimmer 2s infinite;
    }
    
    .enhanced-progress-container.full-mode {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .progress-header {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .progress-title {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        text-shadow: none;
    }
    
    .ai-icon {
        font-size: 2rem;
        animation: pulse 2s infinite;
    }
    
    .title-text {
        flex: 1;
    }
    
    .loading-dots {
        display: flex;
        gap: 4px;
    }
    
    .loading-dots span {
        width: 8px;
        height: 8px;
        background: #007bff;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .loading-dots span:nth-child(1) {
        animation-delay: -0.32s;
    }
    
    .loading-dots span:nth-child(2) {
        animation-delay: -0.16s;
    }
    
    .progress-wrapper {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
        border: 1px solid #dee2e6;
    }
    
    .progress-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .progress-percent {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
        text-shadow: none;
    }
    
    .progress-status {
        font-size: 1rem;
        color: #495057;
        font-weight: 500;
    }
    
    .current-step {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #f8f9fa;
        padding: 12px 16px;
        border-radius: 10px;
        margin: 12px 0;
        border: 1px solid #dee2e6;
    }
    
    .step-icon {
        font-size: 1.2rem;
        animation: rotate 2s linear infinite;
    }
    
    .step-text {
        color: #2c3e50;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    .progress-hints {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
        border: 1px solid #dee2e6;
    }
    
    .hint-text {
        color: #2c3e50;
        font-weight: 500;
        margin-bottom: 8px;
        font-size: 1rem;
    }
    
    .time-estimate {
        color: #6c757d;
        font-size: 0.9rem;
        font-style: italic;
    }
    
    /* 狀態指示器樣式 */
    .status-indicator {
        display: flex;
        align-items: center;
        padding: 10px;
        margin: 5px 0;
        border-radius: 8px;
        background: #f8f9fa;
        border-left: 4px solid #007bff;
    }
    
    .status-indicator.success {
        border-left-color: #28a745;
        background: #d4edda;
    }
    
    .status-indicator.warning {
        border-left-color: #ffc107;
        background: #fff3cd;
    }
    
    .status-indicator.error {
        border-left-color: #dc3545;
        background: #f8d7da;
    }
    
    /* 步驟列表樣式 */
    .step-list {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .step-item {
        display: flex;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .step-item:last-child {
        border-bottom: none;
    }
    
    .step-icon {
        margin-right: 10px;
        font-size: 18px;
    }
    
    .step-text {
        flex: 1;
        font-size: 14px;
    }
    
    /* 增強步驟列表樣式 */
    .enhanced-step-list {
        background: #f8f9fa;
        border-radius: 16px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid #dee2e6;
    }
    
    .enhanced-step-item {
        display: flex;
        align-items: center;
        padding: 16px 20px;
        margin: 12px 0;
        border-radius: 12px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: fadeInUp 0.5s ease-out;
    }
    
    .enhanced-step-item.completed {
        background: #d4edda;
        border-color: #c3e6cb;
    }
    
    .enhanced-step-item.active {
        background: #cce7ff;
        border-color: #99d6ff;
        box-shadow: 0 0 10px rgba(0, 123, 255, 0.2);
        animation: progressGlow 2s infinite;
    }
    
    .enhanced-step-item.pending {
        background: #ffffff;
        border-color: #dee2e6;
    }
    
    .step-icon-container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 16px;
        background: #ffffff;
        border: 1px solid #dee2e6;
    }
    
    .step-icon-container .step-icon {
        font-size: 1.2rem;
        margin: 0;
    }
    
    .step-icon.rotating {
        animation: rotate 2s linear infinite;
    }
    
    .step-content {
        flex: 1;
        margin-right: 16px;
    }
    
    .step-name {
        font-size: 1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 4px;
    }
    
    .step-description {
        font-size: 0.85rem;
        color: #6c757d;
        line-height: 1.4;
    }
    
    .step-status {
        font-size: 0.8rem;
        font-weight: 500;
        padding: 4px 12px;
        border-radius: 20px;
        background: #f8f9fa;
        color: #2c3e50;
        text-align: center;
        min-width: 60px;
        border: 1px solid #dee2e6;
    }
    
    .enhanced-step-item.completed .step-status {
        background: #d4edda;
        color: #155724;
        border-color: #c3e6cb;
    }
    
    .enhanced-step-item.active .step-status {
        background: #cce7ff;
        color: #004085;
        border-color: #99d6ff;
    }
    
    /* 狀態日誌樣式 */
    .status-log {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        max-height: 200px;
        overflow-y: auto;
        border: 1px solid #dee2e6;
    }
    
    .log-entry {
        display: flex;
        align-items: center;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 8px;
        background: #ffffff;
        border-left: 3px solid #007bff;
        animation: fadeInUp 0.3s ease-out;
        border: 1px solid #e9ecef;
    }
    
    .log-time {
        font-size: 0.75rem;
        color: #6c757d;
        font-family: monospace;
        margin-right: 12px;
        min-width: 60px;
    }
    
    .log-status {
        font-size: 0.85rem;
        color: #2c3e50;
        font-weight: 500;
        margin-right: 12px;
        flex: 1;
    }
    
    .log-details {
        font-size: 0.8rem;
        color: #495057;
        font-style: italic;
    }
    
    /* 載入動畫 */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 10px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 新增動畫效果 */
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes bounce {
        0%, 80%, 100% {
            transform: scale(0);
        }
        40% {
            transform: scale(1);
        }
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes progressGlow {
        0%, 100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
    }
    
    /* 按鈕樣式 */
    .stButton > button {
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* 取消按鈕樣式 */
    .cancel-button {
        background: #dc3545 !important;
        color: white !important;
    }
    
    .cancel-button:hover {
        background: #c82333 !important;
    }
    
    /* 成功按鈕樣式 */
    .success-button {
        background: #28a745 !important;
        color: white !important;
    }
    
    .success-button:hover {
        background: #218838 !important;
    }
    
    /* 提示框樣式 */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* 報告區域樣式 */
    .report-section {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }
    
    /* --- 聊天界面增強樣式 --- */
    .chat-container {
        min-height: 300px;
        height: calc(100vh - 200px);
        overflow-y: auto;
        padding: 4px 16px 96px 16px; /* 進一步減少頂部間距 */
        background: #ffffff;
        border-radius: 16px;
        margin: 0 0 4px 0; /* 移除頂部間距 */
        margin-left: 320px !important; /* 避免與側邊欄重疊 */
        margin-right: 25% !important; /* 為右側面板預留空間 */
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
        position: relative;
        z-index: 1;
        width: calc(75% - 320px) !important; /* 設定正確寬度 */
    }
    
    .chat-message {
        margin: 4px 0;
        padding: 12px 16px;
        border-radius: 20px;
        max-width: 75%;
        word-wrap: break-word;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        animation: slideInUp 0.4s ease-out;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .chat-message.user {
        background: #e3f2fd;
        color: #2c3e50;
        margin-left: auto;
        border-radius: 20px 20px 6px 20px;
        border-left: 3px solid #2196f3;
    }
    
    .chat-message.assistant {
        background: #f1f8e9;
        color: #2c3e50;
        margin-right: auto;
        border-radius: 20px 20px 20px 6px;
        border-left: 3px solid #4caf50;
    }
    
    /* 確保 Streamlit 聊天訊息正常顯示並美化 */
    [data-testid="stChatMessage"] {
        display: block !important;
        margin: 4px 0 !important;
        background: transparent !important;
        /* 移除強制定位，讓聊天訊息正常顯示 */
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
    }
    
    /* 修復聊天訊息頭像顯示 */
    [data-testid="stChatMessage"] [data-testid="stChatAvatar"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        background: #f0f0f0 !important;
        margin-right: 12px !important;
        flex-shrink: 0 !important;
    }
    
    /* 修復用戶頭像 */
    [data-testid="stChatMessage"] [data-testid="user"] [data-testid="stChatAvatar"] {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%) !important;
        color: #2196f3 !important;
    }
    
    /* 修復助手頭像 */
    [data-testid="stChatMessage"] [data-testid="assistant"] [data-testid="stChatAvatar"] {
        background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e8 100%) !important;
        color: #4caf50 !important;
    }
    
    /* 確保頭像圖標正常顯示 */
    [data-testid="stChatMessage"] [data-testid="stChatAvatar"] svg {
        width: 20px !important;
        height: 20px !important;
        fill: currentColor !important;
    }
    
    /* 美化聊天訊息容器 */
    [data-testid="stChatMessage"] > div {
        border-radius: 20px !important;
        padding: 14px 18px !important;
        margin: 4px 0 !important;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08) !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
        animation: slideInUp 0.4s ease-out !important;
        /* 移除寬度限制，讓訊息正常顯示 */
        max-width: 100% !important;
        word-wrap: break-word !important;
        display: flex !important;
        align-items: flex-start !important;
        gap: 12px !important;
    }
    
    /* 確保聊天訊息內容區域正確顯示 */
    [data-testid="stChatMessage"] > div > div:last-child {
        flex: 1 !important;
        min-width: 0 !important;
    }
    
    /* 美化用戶訊息 - 靠右顯示，藍色主題 */
    [data-testid="stChatMessage"] [data-testid="user"] {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%) !important;
        color: #1a237e !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        border-radius: 20px 20px 6px 20px !important;
        border-left: 3px solid #2196f3 !important;
        border-right: none !important;
        max-width: 75% !important;
    }
    
    /* 美化助手訊息 - 靠左顯示，綠色主題 */
    [data-testid="stChatMessage"] [data-testid="assistant"] {
        background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e8 100%) !important;
        color: #2e7d32 !important;
        margin-left: 0 !important;
        margin-right: auto !important;
        border-radius: 20px 20px 20px 6px !important;
        border-left: 3px solid #4caf50 !important;
        border-right: none !important;
        max-width: 75% !important;
    }
    
    /* 確保聊天訊息內容可見 */
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] span {
        font-size: 14px !important;
        line-height: 1.5 !important;
        margin: 0 !important;
    }
    
    /* 修復聊天訊息整體佈局 */
    [data-testid="stChatMessage"] {
        display: flex !important;
        align-items: flex-start !important;
        margin: 8px 0 !important;
        padding: 0 !important;
    }
    
    /* 確保聊天訊息容器正確對齊 */
    [data-testid="stChatMessage"] > div {
        display: flex !important;
        align-items: flex-start !important;
        width: 100% !important;
        gap: 12px !important;
    }
    
    /* 修復頭像容器 */
    [data-testid="stChatMessage"] [data-testid="stChatAvatar"] {
        order: 1 !important;
        flex-shrink: 0 !important;
    }
    
    /* 修復訊息內容容器 */
    [data-testid="stChatMessage"] > div > div:last-child {
        order: 2 !important;
        flex: 1 !important;
        min-width: 0 !important;
    }
    
    /* 用戶訊息內容顏色 */
    [data-testid="stChatMessage"] [data-testid="user"] p,
    [data-testid="stChatMessage"] [data-testid="user"] div,
    [data-testid="stChatMessage"] [data-testid="user"] span {
        color: #1a237e !important;
        font-weight: 500 !important;
    }
    
    /* AI訊息內容顏色 */
    [data-testid="stChatMessage"] [data-testid="assistant"] p,
    [data-testid="stChatMessage"] [data-testid="assistant"] div,
    [data-testid="stChatMessage"] [data-testid="assistant"] span {
        color: #2e7d32 !important;
        font-weight: 500 !important;
    }
    
    /* 確保聊天容器從標題位置開始 */
    .main .block-container {
        padding-top: 0 !important;
    }
    
    /* 強制修復所有聊天相關容器的定位 - 使用更廣泛的選擇器 */
    .main .block-container > div,
    .main .block-container > div > div,
    .main .block-container .stColumn,
    .main .block-container .stColumn > div,
    .main .block-container [data-testid="stVerticalBlock"],
    .main .block-container [data-testid="stVerticalBlock"] > div {
        /* 移除強制定位，讓容器正常顯示 */
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* 特別針對聊天訊息容器 */
    .main .block-container [data-testid="stChatMessage"],
    .main .block-container [data-testid="stChatMessage"] > div,
    .main .block-container [data-testid="stChatMessage"] > div > div {
        /* 移除強制定位，讓聊天訊息正常顯示 */
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* 強制修復聊天容器 */
    .main .block-container .chat-container,
    .main .block-container .chat-container > div {
        /* 移除強制定位，讓聊天容器正常顯示 */
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* 使用最高優先級強制修復 - 針對Streamlit的具體結構 */
    .stApp .main .block-container > div[data-testid="stVerticalBlock"],
    .stApp .main .block-container > div[data-testid="stVerticalBlock"] > div,
    .stApp .main .block-container > div[data-testid="stVerticalBlock"] > div > div,
    .stApp .main .block-container .stColumn,
    .stApp .main .block-container .stColumn > div,
    .stApp .main .block-container .stColumn > div > div {
        /* 移除強制定位，讓容器正常顯示 */
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* 特別針對聊天相關的Streamlit組件 */
    .stApp [data-testid="stChatMessage"],
    .stApp [data-testid="stChatMessage"] > div,
    .stApp [data-testid="stChatMessage"] > div > div,
    .stApp [data-testid="stChatMessage"] > div > div > div {
        /* 移除強制定位，讓聊天訊息正常顯示 */
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* 強制修復所有可能的聊天容器 */
    .stApp .main .block-container > div:has([data-testid="stChatMessage"]),
    .stApp .main .block-container > div:has(.chat-container),
    .stApp .main .block-container > div:has([data-testid="stChatInput"]) {
        /* 移除強制定位，讓聊天容器正常顯示 */
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* 正確修復 - 主內容區域在側邊欄右邊 */
    .main .block-container {
        margin-left: 320px !important;
        padding-left: 2rem !important;
        max-width: calc(100vw - 340px) !important;
        width: calc(100vw - 340px) !important;
        position: relative !important;
        left: 0 !important;
    }
    
    /* 確保聊天訊息在正確的容器內顯示 */
    .main .block-container [data-testid="stChatMessage"] {
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* 確保主內容區域不會被推到螢幕左邊 */
    .main {
        margin-left: 0 !important;
        padding-left: 0 !important;
        position: relative !important;
    }
    
    /* 確保主內容區域的父容器正確定位 */
    .main > div {
        margin-left: 320px !important;
        padding-left: 2rem !important;
        max-width: calc(100vw - 340px) !important;
        width: calc(100vw - 340px) !important;
    }
    
    /* 強制修復所有主內容區域的容器 */
    .main .block-container > div,
    .main .block-container > div > div,
    .main .block-container > div > div > div {
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* 特別修復Streamlit列系統 */
    .main .block-container .stColumn {
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* 修復第一列（聊天區域） */
    .main .block-container .stColumn:first-child {
        width: 75% !important;
        max-width: 75% !important;
        margin-right: 0 !important;
    }
    
    /* 修復第二列（右側面板） */
    .main .block-container .stColumn:last-child {
        width: 25% !important;
        max-width: 25% !important;
        margin-left: 0 !important;
    }
    
    /* 修復聊天訊息 - 確保正常顯示 */
    [data-testid="stChatMessage"],
    [data-testid="stChatMessage"] > div,
    [data-testid="stChatMessage"] > div > div {
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* 修復聊天輸入框 */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 320px !important; /* 避免與側邊欄重疊，側邊欄寬度320px */
        right: 25% !important; /* 為右側臨床Orders面板預留25%空間 */
        background: #ffffff !important;
        border-top: 1px solid #e0e0e0 !important;
        box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.06) !important;
        z-index: 20 !important;
        padding: 12px 20px !important;
        width: auto !important; /* 讓 left 和 right 決定寬度 */
        margin-left: 0 !important; /* 確保沒有額外的邊距 */
        margin-right: 0 !important; /* 確保沒有額外的邊距 */
    }
    
    /* 確保聊天輸入框內容可見 */
    [data-testid="stChatInput"] input {
        background: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        color: #2c3e50 !important;
    }
    
    [data-testid="stChatInput"] input:focus {
        border-color: #2196f3 !important;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2) !important;
    }
    
    .chat-message-timestamp {
        font-size: 0.75em;
        opacity: 0.8;
        margin-top: 4px;
    }
    
    /* 固定頭部樣式 */
    .fixed-header {
        position: sticky;
        top: 0;
        z-index: 100;
        background: #ffffff;
        color: #2c3e50;
        padding: 8px 20px;
        margin: 0 0 4px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        border-radius: 0 0 16px 16px;
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    }
    
    .fixed-header h1 {
        margin: 0;
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        line-height: 1.2;
    }
    
    .fixed-header p {
        margin: 2px 0 0 0;
        opacity: 0.7;
        font-size: 0.85rem;
        color: #6c757d;
        line-height: 1.2;
    }
    
    /* 移除重複的聊天輸入框樣式，統一使用上面的樣式 */
    
    .quick-action-button {
        background: #f8f9fa !important;
        color: #2c3e50 !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 12px !important;
        padding: 8px 12px !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    }
    
    .quick-action-button:hover {
        background: #e9ecef !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* 快速操作按鈕統一高度 - 強制統一 */
    .stButton > button[key="quick_vitals"],
    .stButton > button[key="quick_history"] {
        height: 50px !important;
        min-height: 50px !important;
        max-height: 50px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        padding: 12px 8px !important;
        margin-bottom: 6px !important;
        line-height: 1.0 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        box-sizing: border-box !important;
    }
    
    /* 確保按鈕容器也有統一高度 */
    .stButton[key="quick_vitals"],
    .stButton[key="quick_history"] {
        height: 50px !important;
        min-height: 50px !important;
        max-height: 50px !important;
        box-sizing: border-box !important;
    }
    
    /* 強制所有快速操作按鈕的父容器統一高度 */
    .stButton[key="quick_vitals"] *,
    .stButton[key="quick_history"] * {
        box-sizing: border-box !important;
    }
    
    /* 動畫效果 */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    /* 歡迎訊息樣式 */
    .welcome-message {
        text-align: center;
        padding: 20px;
        color: #6c757d;
        background: #f8f9fa;
        border-radius: 16px;
        margin: 8px 0;
        border: 1px solid #e9ecef;
    }
    
    .welcome-message h3 {
        color: #2c3e50;
        margin-bottom: 16px;
        font-weight: 600;
    }
    
    .welcome-message p {
        color: #6c757d;
        line-height: 1.6;
    }
    
    /* 響應式設計 */
    @media (max-width: 768px) {
        /* 移動設備：聊天輸入框佔滿整個寬度 */
        [data-testid="stChatInput"] {
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            padding: 8px 12px !important;
        }
        .progress-container {
            padding: 15px;
            margin: 5px 0;
        }
        
        .enhanced-progress-container {
            padding: 16px;
            margin: 12px 0;
        }
        
        .progress-title {
            font-size: 1.2rem;
            flex-direction: column;
            gap: 8px;
        }
        
        .ai-icon {
            font-size: 1.5rem;
        }
        
        .enhanced-step-item {
            padding: 12px 16px;
            margin: 8px 0;
        }
        
        .step-icon-container {
            width: 32px;
            height: 32px;
            margin-right: 12px;
        }
        
        .step-name {
            font-size: 0.9rem;
        }
        
        .step-description {
            font-size: 0.8rem;
        }
        
        .step-list {
            padding: 10px;
        }
        
        .report-section {
            padding: 15px;
            margin: 10px 0;
        }
        
        .chat-container {
            height: calc(100vh - 180px);
            padding: 12px 16px;
            margin: 4px 0;
            margin-left: 0 !important; /* 移動設備上不需要左邊距 */
            margin-right: 0 !important;
            width: 100% !important;
        }
        
        /* 移動設備上的聊天訊息 */
        [data-testid="stChatMessage"] {
            margin-left: 0 !important;
            margin-right: 0 !important;
            width: 100% !important;
        }
        
        .chat-message {
            max-width: 85%;
            padding: 12px 16px;
        }
        
        /* 移動設備上的訊息樣式調整 */
        [data-testid="stChatMessage"] > div {
            max-width: 90% !important;
            padding: 12px 16px !important;
        }
        
        /* 移動設備上的用戶訊息 */
        [data-testid="stChatMessage"] [data-testid="user"] > div,
        [data-testid="stChatMessage"] [data-testid="user"] {
            margin-left: auto !important;
            margin-right: 0 !important;
        }
        
        /* 移動設備上的AI訊息 */
        [data-testid="stChatMessage"] [data-testid="assistant"] > div,
        [data-testid="stChatMessage"] [data-testid="assistant"] {
            margin-left: 0 !important;
            margin-right: auto !important;
        }
        
        .fixed-header {
            padding: 10px 16px;
            margin: -16px -20px 4px -20px;
        }
        
        .fixed-header h1 {
            font-size: 1.4rem;
        }
        
        .chat-input-container {
            padding: 10px 12px;
        }
        
        .log-entry {
            flex-direction: column;
            align-items: flex-start;
            gap: 4px;
        }
        
        .log-time {
            min-width: auto;
            margin-right: 0;
        }
    }
    
    /* 中等螢幕優化 */
    @media (min-width: 769px) and (max-width: 1199px) {
        [data-testid="stChatInput"] {
            left: 320px !important; /* 與側邊欄寬度一致 */
            right: 25% !important;
            width: calc(75% - 320px) !important;
        }
        
        .main .block-container {
            margin-left: 320px !important;
            max-width: calc(100vw - 340px) !important;
        }
        
        .fixed-header {
            margin-left: 320px !important;
            width: calc(100vw - 340px) !important;
        }
    }
    
    /* 大螢幕優化 */
    @media (min-width: 1200px) {
        [data-testid="stChatInput"] {
            left: 320px !important;
            right: 25% !important;
            width: calc(75% - 320px) !important;
        }
        
        .main .block-container {
            margin-left: 320px !important;
            max-width: calc(100vw - 340px) !important;
        }
        
        .fixed-header {
            margin-left: 320px !important;
            width: calc(100vw - 340px) !important;
        }
        
        .chat-container {
            height: calc(100vh - 220px);
        }
        
        .chat-message {
            max-width: 70%;
        }
    }
    
    /* --- AI 思考中 UI 設計 --- */
    .ai-thinking-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 20px;
        margin: 16px 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: pulse 2s ease-in-out infinite;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .ai-thinking-header {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .ai-thinking-icon {
        margin-right: 10px;
        font-size: 1.3rem;
        animation: bounce 1.5s ease-in-out infinite;
    }
    
    .ai-thinking-dots {
        display: flex;
        align-items: center;
        margin-left: 10px;
    }
    
    .ai-thinking-dot {
        width: 8px;
        height: 8px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 50%;
        margin: 0 3px;
        animation: wave 1.4s ease-in-out infinite;
    }
    
    .ai-thinking-dot:nth-child(1) { animation-delay: 0s; }
    .ai-thinking-dot:nth-child(2) { animation-delay: 0.2s; }
    .ai-thinking-dot:nth-child(3) { animation-delay: 0.4s; }
    
    .ai-thinking-status {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 8px;
        font-style: italic;
    }
    
    /* 動畫效果 */
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.9; }
        50% { transform: scale(1.02); opacity: 1; }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-5px); }
        60% { transform: translateY(-3px); }
    }
    
    @keyframes wave {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-10px); opacity: 1; }
    }
    
    /* Streamlit Spinner 增強樣式 */
    .stSpinner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        font-weight: 600 !important;
        animation: pulse 2s ease-in-out infinite !important;
    }
    
    .stSpinner > div {
        background: rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    /* 確保 Spinner 可見 */
    [data-testid="stSpinner"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        font-weight: 600 !important;
        animation: pulse 2s ease-in-out infinite !important;
        z-index: 9999 !important;
        position: relative !important;
    }
    </style>
    """

def apply_custom_css():
    """應用自定義 CSS 樣式"""
    import streamlit as st
    st.markdown(get_custom_css(), unsafe_allow_html=True)
