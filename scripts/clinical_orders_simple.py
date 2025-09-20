"""
簡化版臨床檢測Orders組件
可直接在舊版本app.py中使用
"""

import streamlit as st
import os
from pathlib import Path
from typing import Optional, Callable


def render_clinical_orders(on_order_action: Optional[Callable[[str, Optional[str]], None]] = None):
    """渲染臨床檢測Orders面板"""
    
    # 應用自定義CSS
    st.markdown("""
    <style>
    /* --- 全局字體與顏色系統 --- */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Noto Sans TC', 'Inter', sans-serif;
    }
    
    /* 主色調系統 */
    :root {
        --primary-color: #2563eb;
        --primary-light: #3b82f6;
        --secondary-color: #f0f9ff;
        --accent-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --card-bg-color: #ffffff;
        --border-color: #e5e7eb;
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* 卡片式設計 */
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
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    
    .clinical-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 2px solid #f3f4f6;
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
    
    /* 按鈕系統 */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid var(--primary-color);
        background-color: var(--secondary-color);
        color: var(--primary-color);
        font-weight: 500;
        font-size: 0.875rem;
        padding: 8px 16px;
        transition: all 0.3s ease;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    .stButton > button:hover {
        background-color: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transform: translateY(-1px);
    }
    
    /* 分頁系統 */
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
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 使用自定義CSS卡片
    st.markdown("""
    <div class="clinical-card">
        <div class="clinical-card-header">
            <span class="clinical-icon">📋</span>
            <div>
                <h3 class="clinical-card-title">臨床決策 (Clinical Orders)</h3>
                <p class="clinical-card-subtitle">點擊下方按鈕執行臨床檢測與處置</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 創建分頁
    tab_titles = [
        "⚕️ 床邊檢查 (Bedside)",
        "🩸 實驗室檢驗 (Labs)",
        "🖥️ 影像學 (Imaging)",
        "💊 藥物處方 (Meds)"
    ]
    
    tabs = st.tabs(tab_titles)
    
    # 床邊檢查
    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("**12-Lead ECG**\n\n12導程心電圖", use_container_width=True):
                if on_order_action:
                    on_order_action("我現在要為病人安排12導程心電圖檢查", "ecg_sample.png")
        with col2:
            if st.button("**POCUS**\n\n床邊超音波", use_container_width=True, disabled=True):
                pass
            st.caption("🔒 此功能即將推出")
    
    # 實驗室檢驗
    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("**Cardiac Enzymes**\n\n心肌酵素 (Troponin I)", use_container_width=True):
                if on_order_action:
                    on_order_action("幫病人抽血，檢驗 Cardiac Troponin I", None)
            if st.button("**CBC/DC**\n\n全血球計數", use_container_width=True):
                if on_order_action:
                    on_order_action("檢驗 CBC/DC，確認是否有貧血或感染", None)
        with col2:
            if st.button("**Coagulation**\n\n凝血功能 (PT/aPTT)", use_container_width=True):
                if on_order_action:
                    on_order_action("檢驗 PT/aPTT，評估凝血功能", None)
            if st.button("**Electrolytes**\n\n電解質與腎功能", use_container_width=True):
                if on_order_action:
                    on_order_action("檢驗電解質與腎功能 (Na, K, Cl, BUN, Cr)", None)
    
    # 影像學檢查
    with tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("**Chest X-ray**\n\n胸部X光", use_container_width=True):
                if on_order_action:
                    on_order_action("安排 Portable Chest X-ray，確認是否有氣胸或主動脈剝離等問題", "chest_xray_sample.png")
        with col2:
            if st.button("**CT Angiography**\n\n電腦斷層血管攝影", use_container_width=True, disabled=True):
                pass
            st.caption("🔒 此功能即將推出")
    
    # 藥物處方
    with tabs[3]:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("**Oxygen**\n\n氧氣治療", use_container_width=True):
                if on_order_action:
                    on_order_action("給予病人氧氣，維持血氧濃度 > 94%", None)
        with col2:
            if st.button("**Aspirin**\n\n阿斯匹靈", use_container_width=True):
                if on_order_action:
                    on_order_action("給予 Aspirin 160-325mg 口嚼", None)
        with col3:
            if st.button("**Nitroglycerin**\n\n硝化甘油 (NTG)", use_container_width=True):
                if on_order_action:
                    on_order_action("給予 Nitroglycerin (NTG) 0.4mg 舌下含服", None)
        with col4:
            if st.button("**Morphine**\n\n嗎啡", use_container_width=True):
                if on_order_action:
                    on_order_action("若 NTG 無法緩解胸痛，給予 Morphine 2-4mg IV", None)


def get_image_path(image_filename: str) -> Optional[str]:
    """獲取圖片完整路徑"""
    if not image_filename:
        return None
    
    # 檢查static/samples目錄
    static_path = Path(__file__).parent / "static" / "samples" / image_filename
    if static_path.exists():
        return str(static_path)
    
    return None


def display_order_result(order_action: str, result_text: str, image_path: Optional[str] = None) -> None:
    """顯示Order執行結果"""
    if image_path:
        image_full_path = get_image_path(image_path)
        if image_full_path and os.path.exists(image_full_path):
            # 顯示圖片
            st.image(image_full_path, caption=f"{get_order_name_from_action(order_action)} 檢查結果", use_column_width=True)
    
    # 顯示結果文字
    st.markdown(f"**[系統訊息]** {result_text}")


def get_order_name_from_action(action: str) -> str:
    """從action文字中提取Order名稱"""
    if "心電圖" in action or "ECG" in action:
        return "12導程心電圖"
    elif "X光" in action or "X-ray" in action:
        return "胸部X光"
    elif "抽血" in action or "檢驗" in action:
        return "實驗室檢驗"
    else:
        return "臨床檢測"
