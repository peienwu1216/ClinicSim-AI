"""
ClinicSim-AI 統一版本 Streamlit 應用程式
整合所有功能：聊天、臨床Orders、報告生成等
"""

import streamlit as st
import requests
import json
import re
import os
from pathlib import Path

# --- 應用程式設定 ---
API_BASE_URL = "http://127.0.0.1:5001"
CASE_ID = "case_chest_pain_acs_01"

# --- 自定義CSS樣式 ---
def apply_custom_css():
    """應用自定義CSS樣式"""
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
        padding: 16px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }
    
    .clinical-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    
    .clinical-card-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 2px solid #f3f4f6;
    }
    
    .clinical-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
    }
    
    .clinical-icon {
        font-size: 1.3rem;
        color: var(--primary-color);
    }
    
    /* 按鈕系統 */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid var(--primary-color);
        background-color: var(--secondary-color);
        color: var(--primary-color);
        font-weight: 500;
        font-size: 0.8rem;
        padding: 6px 12px;
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
        gap: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 8px 16px;
        font-weight: 500;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding: 12px 0;
    }
    
    /* 側邊欄優化 */
    .stSidebar {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* 聊天訊息樣式 */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 8px;
    }
    
    /* 細長條狀高質感聊天輸入框 */
    .stChatInput {
        position: fixed !important;
        bottom: 60px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 70% !important;
        max-width: 600px !important;
        min-width: 400px !important;
        z-index: 1000 !important;
        border: 2px solid var(--primary-color) !important;
        border-radius: 30px !important;
        box-shadow: 
            0 8px 20px rgba(37, 99, 235, 0.15),
            0 2px 4px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        padding: 8px 16px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        height: 60px !important;
        display: flex !important;
        align-items: center !important;
    }
    
    .stChatInput:focus-within {
        border-color: var(--primary-light) !important;
        box-shadow: 
            0 0 0 3px rgba(37, 99, 235, 0.2),
            0 8px 20px rgba(37, 99, 235, 0.2),
            0 2px 4px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
        transform: translateX(-50%) translateY(-2px) !important;
    }
    
    /* 隱藏標籤 */
    .stChatInput label {
        display: none !important;
    }
    
    /* 細長條狀文字區域 */
    .stChatInput textarea {
        border: none !important;
        border-radius: 20px !important;
        padding: 8px 16px !important;
        font-size: 1rem !important;
        line-height: 1.4 !important;
        transition: all 0.3s ease !important;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        height: 40px !important;
        max-height: 40px !important;
        min-height: 40px !important;
        resize: none !important;
        flex: 1 !important;
        margin-right: 8px !important;
    }
    
    .stChatInput textarea:focus {
        background: rgba(255, 255, 255, 0.95) !important;
        outline: none !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stChatInput textarea::placeholder {
        color: #9ca3af !important;
        font-style: italic !important;
    }
    
    /* 細長條狀按鈕 */
    .stChatInput button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 8px 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 
            0 2px 6px rgba(37, 99, 235, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
        min-width: 60px !important;
        height: 40px !important;
    }
    
    .stChatInput button:hover {
        background: linear-gradient(135deg, var(--primary-light) 0%, #1d4ed8 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 
            0 4px 8px rgba(37, 99, 235, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }
    
    .stChatInput button:active {
        transform: translateY(0) !important;
        box-shadow: 
            0 1px 3px rgba(37, 99, 235, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* 添加質感光澤效果 */
    .stChatInput::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 50%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0.1) 100%);
        border-radius: 30px 30px 0 0;
        pointer-events: none;
    }
    
    /* 為固定輸入框留出空間 */
    .main .block-container {
        padding-bottom: 100px !important;
    }
    
    /* 響應式設計 */
    @media (max-width: 768px) {
        .stChatInput {
            width: 85% !important;
            min-width: 300px !important;
            height: 50px !important;
        }
        
        .stChatInput textarea {
            height: 32px !important;
            max-height: 32px !important;
            min-height: 32px !important;
        }
        
        .stChatInput button {
            height: 32px !important;
            padding: 6px 12px !important;
        }
    }
    
    /* 診斷流程面板樣式 */
    .diagnosis-flow-tab {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 8px;
    }
    
    .diagnosis-section {
        margin-bottom: 16px;
        padding: 8px;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 8px;
        border-left: 4px solid var(--primary-color);
    }
    
    .diagnosis-section h4 {
        color: var(--primary-color);
        margin: 0 0 8px 0;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* 按鈕分組樣式 */
    .button-group {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-bottom: 12px;
    }
    
    /* 優先級標示 */
    .priority-high {
        border-left: 4px solid #ef4444 !important;
        background: rgba(239, 68, 68, 0.1) !important;
    }
    
    .priority-medium {
        border-left: 4px solid #f59e0b !important;
        background: rgba(245, 158, 11, 0.1) !important;
    }
    
    .priority-low {
        border-left: 4px solid #10b981 !important;
        background: rgba(16, 185, 129, 0.1) !important;
    }
    /* 進度條樣式 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent-color) 0%, #34d399 50%, var(--accent-color) 100%);
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 工具函數 ---
def get_image_path(image_filename: str) -> str:
    """獲取圖片完整路徑"""
    if not image_filename:
        return None
    
    static_path = Path(__file__).parent / "static" / "samples" / image_filename
    if static_path.exists():
        return str(static_path)
    return None

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

def display_citation_modal(citation):
    """顯示引註的詳細內容"""
    with st.expander(f"📚 引註 {citation['id']}: {citation['query']}", expanded=False):
        st.markdown("**來源：** " + citation['source'])
        st.markdown("**查詢：** " + citation['query'])
        st.markdown("**內容：**")
        st.markdown(citation['content'])

def highlight_citations_in_text(text, citations):
    """在文字中高亮顯示引註標記"""
    if not citations:
        return text
    
    for citation in citations:
        citation_id = citation['id']
        pattern = f'\\[引註 {citation_id}\\]'
        replacement = f'<span style="background-color: #e1f5fe; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: #0277bd;">[引註 {citation_id}]</span>'
        text = re.sub(pattern, replacement, text)
    
    return text

# --- 處理函數 ---
def handle_order_action(action: str, image_path: str = None):
    """處理臨床檢測Orders"""
    if not action:
        return
    
    # 標記問診已開始
    st.session_state.has_started = True
    
    # 將使用者訊息加入歷史紀錄
    st.session_state.messages.append({"role": "user", "content": action})
    
    # 如果有圖片，顯示圖片
    if image_path:
        image_full_path = get_image_path(image_path)
        if image_full_path and os.path.exists(image_full_path):
            st.image(image_full_path, caption=f"{get_order_name_from_action(action)} 檢查結果", use_column_width=True)
    
    # 呼叫後端並處理回應
    with st.spinner("AI 病人正在處理您的臨床指令..."):
        try:
            payload = {"history": st.session_state.messages, "case_id": CASE_ID}
            response = requests.post(f"{API_BASE_URL}/ask_patient", json=payload)
            response.raise_for_status()
            
            response_data = response.json()
            ai_reply = response_data.get("reply")
            
            # 更新覆蓋率和生命體徵
            st.session_state.coverage = response_data.get("coverage", st.session_state.coverage)
            if "vital_signs" in response_data:
                st.session_state.vital_signs = response_data["vital_signs"]

            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.rerun()

        except requests.exceptions.RequestException as e:
            st.error(f"無法連接到後端服務，請確認伺服器正在運行。\n\n錯誤訊息：{e}")

def handle_user_input(prompt_text: str):
    """處理使用者輸入"""
    if not prompt_text:
        return

    # 標記問診已開始
    st.session_state.has_started = True

    # 將使用者訊息加入歷史紀錄
    st.session_state.messages.append({"role": "user", "content": prompt_text})

    # 呼叫後端並處理回應
    with st.spinner("AI 病人正在思考..."):
        try:
            payload = {"history": st.session_state.messages, "case_id": CASE_ID}
            response = requests.post(f"{API_BASE_URL}/ask_patient", json=payload)
            response.raise_for_status()
            
            response_data = response.json()
            ai_reply = response_data.get("reply")
            
            # 更新覆蓋率和生命體徵
            st.session_state.coverage = response_data.get("coverage", st.session_state.coverage)
            if "vital_signs" in response_data:
                st.session_state.vital_signs = response_data["vital_signs"]

            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.rerun()

        except requests.exceptions.RequestException as e:
            st.error(f"無法連接到後端服務，請確認伺服器正在運行。\n\n錯誤訊息：{e}")

def handle_end_session():
    """處理結束問診"""
    st.session_state.session_ended = True
    st.session_state.has_started = True
    
    with st.spinner("AI 評估官正在生成您的回饋報告..."):
        try:
            payload = {"full_conversation": st.session_state.messages, "case_id": CASE_ID}
            response = requests.post(f"{API_BASE_URL}/get_feedback_report", json=payload)
            response.raise_for_status()
            
            report_text = response.json().get("report_text")
            st.session_state.report = report_text
            st.rerun()

        except requests.exceptions.RequestException as e:
            st.error(f"無法生成報告，請確認後端服務是否正常。\n\n錯誤訊息：{e}")
            st.session_state.session_ended = False

def handle_generate_detailed_report():
    """處理生成詳細報告"""
    with st.spinner("AI 教師正在生成詳細分析報告（包含 RAG 臨床指引）..."):
        try:
            payload = {"full_conversation": st.session_state.messages, "case_id": CASE_ID}
            response = requests.post(f"{API_BASE_URL}/get_detailed_report", json=payload)
            response.raise_for_status()
            
            response_data = response.json()
            detailed_report_text = response_data.get("report_text")
            citations = response_data.get("citations", [])
            rag_queries = response_data.get("rag_queries", [])
            
            st.session_state.detailed_report = detailed_report_text
            st.session_state.citations = citations
            st.session_state.rag_queries = rag_queries
            st.rerun()

        except requests.exceptions.RequestException as e:
            st.error(f"無法生成詳細報告，請確認後端服務是否正常。\n\n錯誤訊息：{e}")

# --- Streamlit 頁面設定 ---
st.set_page_config(
    page_title="ClinicSim AI - 臨床技能教練", 
    page_icon="🧑‍⚕️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 應用自定義CSS
apply_custom_css()

# --- 初始化 Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "report" not in st.session_state:
    st.session_state.report = None
if "detailed_report" not in st.session_state:
    st.session_state.detailed_report = None
if "citations" not in st.session_state:
    st.session_state.citations = []
if "rag_queries" not in st.session_state:
    st.session_state.rag_queries = []
if "session_ended" not in st.session_state:
    st.session_state.session_ended = False
if "coverage" not in st.session_state:
    st.session_state.coverage = 0
if "vital_signs" not in st.session_state:
    st.session_state.vital_signs = None
if "has_started" not in st.session_state:
    st.session_state.has_started = False

# --- 側邊欄 Sidebar ---
with st.sidebar:
    st.title("🧑‍⚕️ ClinicSim AI")
    st.info("一個為醫學生設計的 AI 臨床技能教練。")
    
    # 問診覆蓋率
    st.subheader("📊 問診覆蓋率")
    st.progress(st.session_state.coverage, text=f"{st.session_state.coverage}%")
    st.caption("根據提問即時更新")
    
    # 生命體徵監視器
    st.subheader("💓 生命體徵")
    if st.session_state.vital_signs:
        col1, col2 = st.columns(2)
        vitals = st.session_state.vital_signs
        col1.metric("心率", f"{vitals.get('HR_bpm', 'N/A')} bpm", delta_color="inverse")
        col1.metric("血氧", f"{vitals.get('SpO2_room_air', 'N/A')}%", delta_color="inverse")
        col2.metric("血壓", f"{vitals.get('BP_mmHg', 'N/A')} mmHg", delta_color="inverse")
        col2.metric("呼吸", f"{vitals.get('RR_bpm', 'N/A')} /min", delta_color="inverse")
    else:
        st.info("待測量")

    st.markdown("---")
    
    # 控制按鈕
    end_session_button = st.button("📋 總結與計畫", disabled=st.session_state.session_ended, use_container_width=True)
    
    # 詳細報告按鈕（只在問診結束後顯示）
    if st.session_state.session_ended:
        st.markdown("---")
        detailed_report_button = st.button("🤖 完整報告", 
                                         disabled=st.session_state.detailed_report is not None,
                                         help="生成包含臨床指引的詳細分析報告",
                                         use_container_width=True)

# --- 主介面佈局 ---
# 創建主佈局：左側聊天，右側臨床Orders
col1, col2 = st.columns([3, 1])

with col1:
    st.title("模擬診間：急性胸痛")
    st.write("您現在正在與一位模擬病人進行問診。請開始您的提問。")

    # 顯示歷史對話紀錄
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 聊天輸入框 - 固定在底部中間位置
if prompt := st.chat_input("請開始問診...", disabled=st.session_state.session_ended):
    handle_user_input(prompt)

with col2:
    # 急性胸痛診斷流程面板
    st.markdown("""
    <div class="clinical-card">
        <div class="clinical-card-header">
            <span class="clinical-icon">🏥</span>
            <span class="clinical-card-title">急性胸痛診斷流程</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 創建診斷流程分頁
    tab_titles = [
        "🔍 初步評估",
        "⚡ 快速篩查", 
        "🖥️ 影像檢查",
        "💊 緊急處置"
    ]
    
    tabs = st.tabs(tab_titles)
    
    # 1. 初步臨床評估
    with tabs[0]:
        st.markdown("""
        <div class="diagnosis-section priority-high">
            <h4>📋 問診重點</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("**OPQRST**\n疼痛評估", use_container_width=True):
            handle_order_action("進行 OPQRST 疼痛評估：發作時間、誘發因子、疼痛性質、放射位置、嚴重程度、持續時間", None)
        
        if st.button("**伴隨症狀**\n呼吸困難/出汗", use_container_width=True):
            handle_order_action("詢問是否有呼吸困難、出汗、暈厥、噁心嘔吐等伴隨症狀", None)
        
        st.markdown("""
        <div class="diagnosis-section priority-high">
            <h4>🩺 身體檢查</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("**生命體徵**\n血壓/心率", use_container_width=True):
            handle_order_action("測量生命體徵：血壓、心率、呼吸、體溫、血氧飽和度", None)
        
        if st.button("**心肺聽診**\n心音/呼吸音", use_container_width=True):
            handle_order_action("進行心肺聽診，檢查心音、呼吸音、心包摩擦音", None)
        
        if st.button("**胸壁檢查**\n壓痛/觸診", use_container_width=True):
            handle_order_action("檢查胸壁是否有壓痛、腫脹、皮膚變化", None)
    
    # 2. 快速篩查（關鍵檢查）
    with tabs[1]:
        st.markdown("""
        <div class="diagnosis-section priority-high">
            <h4>⚡ 第一優先檢查</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("**12導程ECG**\n心電圖", use_container_width=True):
            handle_order_action("立即安排12導程心電圖檢查，判讀ST段變化、T波倒置、Q波形成", "ecg_sample.png")
        
        if st.button("**Troponin I**\n心肌酵素", use_container_width=True):
            handle_order_action("抽血檢驗高敏感性Troponin I，並安排3-6小時後複檢觀察動態變化", None)
        
        st.markdown("""
        <div class="diagnosis-section priority-medium">
            <h4>🩸 實驗室檢查</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("**CBC/DC**\n血球計數", use_container_width=True):
            handle_order_action("檢驗CBC/DC，確認是否有貧血、感染、血小板異常", None)
        
        if st.button("**D-Dimer**\n血栓篩檢", use_container_width=True):
            handle_order_action("檢驗D-Dimer，協助排除肺栓塞", None)
        
        if st.button("**電解質**\nNa/K/Cl", use_container_width=True):
            handle_order_action("檢驗電解質，評估心臟功能", None)
    
    # 3. 輔助影像檢查
    with tabs[2]:
        st.markdown("""
        <div class="diagnosis-section priority-medium">
            <h4>🖥️ 影像學檢查</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("**Chest X-ray**\n胸部X光", use_container_width=True):
            handle_order_action("安排胸部X光檢查，偵測氣胸、肺炎、心臟擴大、主動脈剝離徵象", "chest_xray_sample.png")
        
        if st.button("**CT Angio**\n血管攝影", use_container_width=True):
            handle_order_action("安排CT血管攝影，評估主動脈剝離、肺栓塞", None)
        
        if st.button("**Echo**\n心臟超音波", use_container_width=True):
            handle_order_action("安排心臟超音波檢查，評估心臟功能、瓣膜、心包膜", None)
        
        st.markdown("""
        <div class="diagnosis-section priority-low">
            <h4>🔬 特殊檢查</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("**Stress Test**\n運動心電圖", use_container_width=True, disabled=True):
            pass
        st.caption("🔒 穩定後安排")
    
    # 4. 緊急處置
    with tabs[3]:
        st.markdown("""
        <div class="diagnosis-section priority-high">
            <h4>🚨 緊急處置</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("**O₂ 氧氣**\n維持血氧", use_container_width=True):
            handle_order_action("給予氧氣治療，維持血氧飽和度 > 94%", None)
        
        if st.button("**Aspirin**\n阿斯匹靈", use_container_width=True):
            handle_order_action("給予 Aspirin 160-325mg 口嚼，預防血栓形成", None)
        
        if st.button("**NTG**\n硝化甘油", use_container_width=True):
            handle_order_action("給予 Nitroglycerin 0.4mg 舌下含服，緩解心絞痛", None)
        
        if st.button("**Morphine**\n嗎啡", use_container_width=True):
            handle_order_action("若疼痛嚴重且NTG無效，給予 Morphine 2-4mg IV", None)
        
        st.markdown("""
        <div class="diagnosis-section priority-medium">
            <h4>📞 會診</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("**心臟科**\n緊急會診", use_container_width=True):
            handle_order_action("緊急會診心臟科，評估是否需要心導管介入", None)
        
        if st.button("**胸腔科**\n會診", use_container_width=True):
            handle_order_action("會診胸腔科，評估肺部疾病", None)

# --- 處理按鈕事件 ---
# 處理結束問診按鈕
if end_session_button and not st.session_state.session_ended:
    handle_end_session()

# 處理詳細報告生成按鈕
if st.session_state.session_ended and 'detailed_report_button' in locals() and detailed_report_button and not st.session_state.detailed_report:
    handle_generate_detailed_report()

# --- 顯示報告區域 ---
if st.session_state.session_ended:
    st.info("本次問診已結束。")
    
    # 顯示即時報告（第一階段）
    if st.session_state.report:
        st.markdown("---")
        st.subheader("📊 即時評估報告")
        st.markdown(st.session_state.report)
    
    # 顯示詳細報告（第二階段）
    if st.session_state.detailed_report:
        st.markdown("---")
        st.subheader("🤖 完整分析報告 (LLM + RAG)")
        st.info("此報告由 AI 教師基於臨床指引生成，包含詳細的學習建議。")
        
        # 顯示報告內容，包含引註高亮
        highlighted_report = highlight_citations_in_text(st.session_state.detailed_report, st.session_state.citations)
        st.markdown(highlighted_report, unsafe_allow_html=True)
        
        # 顯示引註資訊
        if st.session_state.citations:
            st.markdown("---")
            st.subheader("📚 引註來源")
            st.info("以下為報告中引用的臨床指引來源，點擊可查看詳細內容。")
            
            # 顯示所有引註
            for citation in st.session_state.citations:
                display_citation_modal(citation)
            
            # 顯示 RAG 查詢摘要
            if st.session_state.rag_queries:
                with st.expander("🔍 RAG 查詢摘要", expanded=False):
                    st.markdown("**本次報告基於以下查詢獲取臨床指引：**")
                    for i, query in enumerate(st.session_state.rag_queries, 1):
                        st.markdown(f"{i}. {query}")
        
    elif st.session_state.session_ended:
        st.markdown("---")
        st.info("💡 點擊左側「完整報告」按鈕，獲取包含 RAG 臨床指引的詳細分析。")

# --- 頁腳資訊 ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 0.8rem;'>
    <p>🧑‍⚕️ ClinicSim AI - 臨床技能教練 | 統一版本</p>
    <p>請確保後端伺服器正在運行 (python main.py)</p>
</div>
""", unsafe_allow_html=True)