import streamlit as st
import requests
import json

# --- 應用程式設定 ---
API_BASE_URL = "http://127.0.0.1:5001"
CASE_ID = "case_chest_pain_acs_01" # 使用我們更新後的 case_id

# --- Streamlit 頁面設定 ---
st.set_page_config(page_title="ClinicSim AI - 臨床技能教練", page_icon="🧑‍⚕️", layout="wide")

# --- 初始化 Session State ---
# 'session_state' 是 Streamlit 用來在每次互動間保存變數的方法
if "messages" not in st.session_state:
    st.session_state.messages = []
if "report" not in st.session_state:
    st.session_state.report = None
if "session_ended" not in st.session_state:
    st.session_state.session_ended = False
if "coverage" not in st.session_state:
    st.session_state.coverage = 0
# --- ✨ 新增的 Session State ✨ ---
if "vital_signs" not in st.session_state:
    st.session_state.vital_signs = None

# --- 側邊欄 Sidebar ---
with st.sidebar:
    st.title("🧑‍⚕️ ClinicSim AI")
    st.info("一個為醫學生設計的 AI 臨床技能教練。")
    
    # --- ✨ 新增的儀表板 ✨ ---
    st.subheader("問診覆蓋率 (Checklist Coverage)")
    if "coverage" not in st.session_state:
        st.session_state.coverage = 0
    st.progress(st.session_state.coverage, text=f"{st.session_state.coverage}%")
    st.caption("此儀表板會根據你的提問即時更新。")
    
    # --- ✨ 新增的生命體徵監視器 ✨ ---
    st.subheader("生命體徵監視器")
    if st.session_state.vital_signs:
        # 使用兩欄佈局來顯示
        col1, col2 = st.columns(2)
        vitals = st.session_state.vital_signs
        col1.metric("心率 (HR)", f"{vitals.get('HR_bpm', 'N/A')} bpm", delta_color="inverse")
        col1.metric("血氧 (SpO2)", f"{vitals.get('SpO2_room_air', 'N/A')}", delta_color="inverse")
        col2.metric("血壓 (BP)", f"{vitals.get('BP_mmHg', 'N/A')} mmHg", delta_color="inverse")
        col2.metric("呼吸 (RR)", f"{vitals.get('RR_bpm', 'N/A')} /min", delta_color="inverse")
    else:
        st.info("待測量")

    st.markdown("---")
    st.session_state.end_session_button = st.button("進入總結與計畫", disabled=st.session_state.session_ended)


# --- 主介面 ---
st.title("模擬診間：急性胸痛")
st.write("您現在正在與一位模擬病人進行問診。請開始您的提問。")

# --- ✨ 新增的指令按鈕 ✨ ---
with st.container():
    # 使用 popover 創建一個指令選單
    with st.popover("常用指令"):
        st.markdown("點擊下方按鈕，快速執行臨床操作：")
        measure_vitals_clicked = st.button("測量生命徵象", use_container_width=True)

# 顯示歷史對話紀錄
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ✨ 邏輯改造：將 API 呼叫封裝成函式 ✨ ---
def handle_user_input(prompt_text: str):
    """處理使用者輸入（來自聊天框或按鈕），並與後端互動"""
    if not prompt_text:
        return

    # 1. 將使用者訊息加入歷史紀錄並顯示
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
        st.markdown(prompt_text)

    # 2. 呼叫後端並處理回應
    with st.chat_message("assistant"):
        with st.spinner("AI 病人正在思考..."):
            try:
                payload = {"history": st.session_state.messages, "case_id": CASE_ID}
                response = requests.post(f"{API_BASE_URL}/ask_patient", json=payload)
                response.raise_for_status()
                
                response_data = response.json()
                ai_reply = response_data.get("reply")
                
                # 更新覆蓋率
                st.session_state.coverage = response_data.get("coverage", st.session_state.coverage)
                
                # ✨ 新增：更新生命體徵 ✨
                if "vital_signs" in response_data:
                    st.session_state.vital_signs = response_data["vital_signs"]

                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                # 我們需要 st.rerun() 來強制刷新側邊欄
                st.rerun()

            except requests.exceptions.RequestException as e:
                st.error(f"無法連接到後端服務，請確認 mock_server.py 正在運行。\n\n錯誤訊息：{e}")


# --- 處理各類使用者輸入 ---

# 1. 處理指令按鈕點擊
if measure_vitals_clicked:
    handle_user_input("/測量生命徵象")

# 2. 處理聊天框輸入
if prompt := st.chat_input("請開始問診...", disabled=st.session_state.session_ended):
    handle_user_input(prompt)


# 處理結束問診按鈕與顯示報告的邏輯
if st.session_state.end_session_button and not st.session_state.session_ended:
    st.session_state.session_ended = True
    with st.spinner("AI 評估官正在生成您的回饋報告..."):
        try:
            payload = {"full_conversation": st.session_state.messages, "case_id": CASE_ID}
            response = requests.post(f"{API_BASE_URL}/get_feedback_report", json=payload)
            response.raise_for_status()
            
            report_text = response.json().get("report_text")
            st.session_state.report = report_text
            st.rerun() # 重新整理頁面以顯示報告

        except requests.exceptions.RequestException as e:
            st.error(f"無法生成報告，請確認後端服務是否正常。\n\n錯誤訊息：{e}")
            st.session_state.session_ended = False # 讓使用者可以重試

# ... in app.py, inside "with st.sidebar:" ...
with st.expander("💡 OSCE 技巧小抄"):
    st.markdown("""
    **開場建議：**
    > 「您好，我是 OOO 醫學生。在您同意下，為您快速了解胸痛細節，目標是盡快找到原因並幫您舒服一些。」
    
    **關鍵決策指令範例：**
    > 「您現在的症狀是我們非常重視的警訊，我會**立刻安排 12 導程心電圖（在 10 分內完成）**與抽血檢驗，同時持續監測您的生命徵象。」
    
    **結尾總結建議：**
    > 「總結一下，目前高度懷疑是心臟的問題。我們會先做檢查，如果症狀加重，請立刻告訴我們。」
    """)
# ...

# 如果問診已結束，顯示報告
if st.session_state.session_ended:
    st.info("本次問診已結束。")
    if st.session_state.report:
        st.markdown("---")
        st.markdown(st.session_state.report)