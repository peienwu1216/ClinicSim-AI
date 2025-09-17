import json
import ollama
from flask import Flask, request, Response

# 初始化 Flask 應用程式
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 確保中文字符正常顯示

# --- Helper Functions ---
def load_case_data(case_id: str) -> dict:
    """根據 case_id 載入對應的教案 JSON 檔案"""
    try:
        # 修正檔案路徑以匹配我們的結構
        with open(f"cases/{case_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# --- API Endpoints ---

@app.route('/ask_patient', methods=['POST'])
def ask_patient():
    """處理與 AI 病人的對話"""
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

    # --- 更新的部分：讀取新的 JSON 結構 ---
    ai_instructions = case_data["ai_instructions"]
    patient_story = case_data["patient_story_data"]

    # 組合一個更精確的 System Prompt
    system_prompt = f"""
    You are a patient actor. Your persona and behavioral instructions are defined below.
    
    # AI PERSONA AND INSTRUCTIONS
    {json.dumps(ai_instructions, ensure_ascii=False)}

    # CASE DATA FOR YOUR REFERENCE (Only use this information when asked by the student)
    {json.dumps(patient_story, ensure_ascii=False)}

    The conversation history with the student is below. Based on all the information above, provide the next response as the patient.
    """
    
    messages = [{"role": "system", "content": system_prompt}] + history

    try:
        response = ollama.chat(model='llama3:8b', messages=messages)
        ai_reply = response['message']['content']
        success_response = json.dumps({"reply": ai_reply}, ensure_ascii=False)
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
    You are a professional OSCE evaluator from Taiwan, conducting a detailed and objective evaluation of a student's performance. Your entire output MUST be in Traditional Chinese (繁體中文).

    ### CONTEXT
    - The **'user'** in the conversation log is the **'student'** being evaluated.
    - The **'assistant'** in the conversation log is the **'simulated patient'**.

    ### CONVERSATION LOG
    ---
    {conversation_text}
    ---

    ### EVALUATION CHECKLIST
    ---
    {checklist_text}
    ---

    ### CRITICAL INSTRUCTIONS

    1.  **ANALYZE THE STUDENT'S ACTIONS**: Your entire evaluation must focus on the **student's ('user') performance**. Analyze the questions the student asked. **DO NOT** describe what the patient ('assistant') said, except as a result of the student's questioning.

    2.  **EVIDENCE-BASED JUSTIFICATION**: For each checklist point, you MUST provide a rating (✅, ⚠️, or ❌) AND a justification. The justification **MUST quote or accurately describe the student's specific question or action**. If the student did not ask, the justification is "學生未詢問此項目".

    3.  **STRICT RATING SYSTEM**:
        - ✅: The student's question directly and clearly addresses the checklist point.
        - ⚠️: The student's question is related but incomplete, imprecise, or they did not follow up on a key finding.
        - ❌: The student did not ask about this point at all.

    4.  **ROLE ADHERENCE**: Your role is to EVALUATE the student. DO NOT write any summary or plan as if you were the student.

    5.  **EXAMPLE OF CORRECT JUSTIFICATION**:
        - **CORRECT**: `- ✅ 疼痛位置 (Site): 學生透過提問『請問你哪裡痛？』成功問診。`
        - **INCORRECT**: `- ✅ 疼痛位置 (Site): 學生回答『我的胸口很痛』。`

    ### OUTPUT FORMAT
    Generate the report in Markdown format with the following structure:
    1.  Start with `### 診後分析報告`.
    2.  List each checklist item using the format: `- [RATING] [Checklist Point]: [Justification based on student's action]`.
    3.  End with a `### 總結與建議` section providing objective feedback on the student's performance.
    """

    try:
        response = ollama.chat(model='llama3:8b', messages=[{"role": "user", "content": analyst_prompt}])
        report = response['message']['content']
        success_response = json.dumps({"report_text": report}, ensure_ascii=False)
        return Response(success_response, mimetype='application/json', status=200)
    except Exception as e:
        error_response = json.dumps({"error": str(e)}, ensure_ascii=False)
        return Response(error_response, mimetype='application/json', status=500)

# --- 啟動伺服器 ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)