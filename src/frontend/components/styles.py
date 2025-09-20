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
    
    /* 響應式設計 */
    @media (max-width: 768px) {
        .progress-container {
            padding: 15px;
            margin: 5px 0;
        }
        
        .step-list {
            padding: 10px;
        }
        
        .report-section {
            padding: 15px;
            margin: 10px 0;
        }
    }
    </style>
    """

def apply_custom_css():
    """應用自定義 CSS 樣式"""
    import streamlit as st
    st.markdown(get_custom_css(), unsafe_allow_html=True)
