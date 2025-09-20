"""
自定義 CSS 樣式
用於改善 UI 的視覺效果
"""

def get_custom_css():
    """返回自定義 CSS 樣式"""
    return """
    <style>
    /* 進度條樣式 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 50%, #4CAF50 100%);
        border-radius: 10px;
    }
    
    /* 進度容器樣式 */
    .progress-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
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
