import json
import os
import requests
#import ollama
from flask import Flask, request, Response
from call_AI import call_ai

# 初始化 Flask 應用程式
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 確保中文字符正常顯示

# --- LLM Config ---
# 透過環境變數切換：
#   LLM_PROVIDER: 'ollama' (預設) 或 'openai_compat'（如 Lemonade 提供 OpenAI 相容 API）
#   LLM_BASE_URL: 當使用 openai_compat 時的基底網址，例如 http://localhost:11434 或 http://localhost:8000
#   LLM_API_KEY:  若需要授權時的金鑰（可選）
#   LLM_MODEL:    模型名稱，例如 'llama3:8b' 或 'qwen2.5:7b'
LLM_PROVIDER = "openai_compat"
LLM_BASE_URL = 'http://localhost:8000'
LLM_API_KEY = 'lemonade'
LLM_MODEL = 'Qwen3-1.7B-GGUF'

# --- Helper Functions ---
def load_case_data(case_id: str) -> dict:
    """根據 case_id 載入對應的教案 JSON 檔案"""
    try:
        # 修正檔案路徑以匹配我們的結構
        with open(f"cases/{case_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# --- ✨ 新增的 Helper Function ✨ ---
def calculate_coverage(history: list, checklist: list) -> int:
    """計算問診覆蓋率"""
    if not history or not checklist:
        return 0
    student_dialogue = " ".join([msg.get("content", "") for msg in history if msg.get("role") == "user"])    
    covered_count = 0
    for item in checklist:
        keywords = item.get("keywords", []) if isinstance(item, dict) else []
        if any((kw in student_dialogue) for kw in keywords):
            covered_count += 1
    percentage = int((covered_count / len(checklist)) * 100) if len(checklist) > 0 else 0
    return percentage

# --- API Endpoints ---

@app.route('/', methods=['POST', 'GET'])
def home():
    return "<br>ClinicSim-AI Mock Server is running.</br>"

@app.route('/ask_patient', methods=['POST'])
def ask_patient():
    print("ask_patient")
    """處理與 AI 病人的對話，並回傳即時覆蓋率"""
    data = request.get_json()
    if not data or "history" not in data or "case_id" not in data:
        error_response = json.dumps({"error": "Invalid request body"}, ensure_ascii=False)
        return Response(error_response, mimetype='application/json', status=400)

    history = data["history"]
    case_id = data["case_id"]

    case_data = load_case_data(case_id)
    if not case_data:
        error_response = json.dumps({"error": f"Case '{case_id}' not found"}, ensure_ascii=False)
        return Response(error_response, mimetype='application/json', status=404)

    # --- ✨ 新增：攔截特殊指令 ✨ ---
    last_user_message = history[-1]["content"].strip() if history and history[-1]["role"] == "user" else ""

    checklist = case_data.get("feedback_system", {}).get("checklist", [])
    coverage_percentage = calculate_coverage(history, checklist)

    # 如果是測量生命體徵的指令
    if last_user_message == "/測量生命徵象":
        vital_signs = case_data.get("patient_story_data", {}).get("vital_signs", {})
        
        # 格式化一個簡單的文字回覆
        vitals_text = ", ".join([f"{key.replace('_', ' ')}: {value}" for key, value in vital_signs.items()])
        reply_message = f"[操作完成] 生命體徵測量結果如下：{vitals_text}"
        
        success_response = json.dumps({
            "reply": reply_message,
            "coverage": coverage_percentage,
            "vital_signs": vital_signs  # 將結構化數據一併回傳
        }, ensure_ascii=False)
        
        return Response(success_response, mimetype='application/json', status=200)

    # --- ✨ 原有邏輯微調 ✨ ---
    # (如果不是特殊指令，則照常呼叫 LLM)
    ai_instructions = case_data["ai_instructions"]
    patient_story = case_data["patient_story_data"]

    system_prompt = f"""
    你是一位模擬病人（標準化病人）。從現在起，你的所有輸出必須使用『繁體中文』，嚴禁使用任何英文單字、片語或縮寫（包含括號或標點中的英文）。必要之專有名詞請以繁體中文全形描述。

    【角色設定與回應規則】
    1. 僅回答學生（user）直接詢問的內容，不主動透露未被詢問的資訊。
    2. 回覆格式需為「[動作/情緒] 對話內容」，動作與情緒以中括號標示，且必須用繁體中文描述。
    3. 嚴格依據下方個案資料作答；除非學生詢問，否則不要主動提供。

    【個案行為規範（AI INSTRUCTIONS）】
    {json.dumps(ai_instructions, ensure_ascii=False)}

    【個案資料（僅於被問及時使用）】
    {json.dumps(patient_story, ensure_ascii=False)}

    請根據以上資訊，作為病人，以繁體中文回覆下一句話。
    """

    messages = str(system_prompt) + str(history)

    try:
        print(messages)
        ai_reply = call_ai(messages)
        success_response = json.dumps({
            "reply": ai_reply,
            "coverage": coverage_percentage
        }, ensure_ascii=False)
        return Response(success_response, mimetype='application/json', status=200)
    except Exception as e:
        error_response = json.dumps({"error": str(e)}, ensure_ascii=False)
        return Response(error_response, mimetype='application/json', status=500)


@app.route('/get_feedback_report', methods=['POST'])
def get_feedback_report():
    """生成診後分析報告"""
    data = request.get_json()
    if not data or "full_conversation" not in data or "case_id" not in data:
        error_response = json.dumps({"error": "Invalid request body"}, ensure_ascii=False)
        return Response(error_response, mimetype='application/json', status=400)
        
    full_conversation = data["full_conversation"]
    case_id = data["case_id"]

    case_data = load_case_data(case_id)
    if not case_data:
        error_response = json.dumps({"error": f"Case '{case_id}' not found"}, ensure_ascii=False)
        return Response(error_response, mimetype='application/json', status=404)
    
    # --- 更新的部分：讀取新的 JSON 結構 ---
    feedback_system = case_data["feedback_system"]
    checklist = feedback_system["checklist"]
    
    conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in full_conversation])
    checklist_text = "\n".join([f"- {item['point']} (Category: {item['category']})" for item in checklist])

    # ... 在 get_feedback_report 函式中 ...
    analyst_prompt = f"""
    你是一位台灣的 OSCE 專業評估者，請以嚴謹且客觀的方式評估學生的表現。你的整份輸出必須使用『繁體中文』，嚴禁輸出任何英文單字、片語或縮寫（包含括號或標點中的英文）。若來源對話出現英文或縮寫，請以繁體中文完整轉述。

    ### 背景說明
    - 對話紀錄中的 'user' 代表受評的『學生』。
    - 對話紀錄中的 'assistant' 代表『模擬病人』。

    ### 對話紀錄
    ---
    {conversation_text}
    ---

    ### 評估清單（Checklist）
    ---
    {checklist_text}
    ---

    ### 核心評估規範

    1.  僅分析學生（user）的問診與行為。除非作為學生提問後的結果，否則不要描述病人的自述。

    2.  逐項清單給出等級（✅、⚠️、❌）與依據。依據需引用或準確描述學生的具體提問或行為；若未詢問，請填寫「學生未詢問此項目」。

    3.  嚴格評分標準：
        - ✅：學生的提問直接且清楚地覆蓋該清單項目。
        - ⚠️：學生有相關提問但不完整／不精確，或未追問關鍵細節。
        - ❌：學生完全未涉及該項目。

    4.  評估者角色：僅進行評估，請勿以學生口吻撰寫計畫。

    5.  正確示例：
        - 正確：- ✅ 疼痛位置 (Site)：學生透過提問「請問你哪裡痛？」成功問診。
        - 錯誤：- ✅ 疼痛位置 (Site)：學生回答「我的胸口很痛」。

    ### 輸出格式（Markdown）
    1.  以「### 診後分析報告」作為開頭。
    2.  依序列出各清單項目，格式為：`- [等級] [項目名稱]：基於學生行為之具體依據`。
    3.  以「### 總結與建議」作結，提供客觀可行的改進建議。
    """

    try:
        report = call_ai(analyst_prompt)
        success_response = json.dumps({"report_text": report}, ensure_ascii=False)
        return Response(success_response, mimetype='application/json', status=200)
    except Exception as e:
        error_response = json.dumps({"error": str(e)}, ensure_ascii=False)
        return Response(error_response, mimetype='application/json', status=500)

# --- 啟動伺服器 ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)