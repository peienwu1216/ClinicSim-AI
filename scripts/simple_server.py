import os
import json
import random
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# Flask App 初始化
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 輔助函式
def load_case_data(case_id: str) -> dict:
    """根據 case_id 載入對應的教案 JSON 檔案"""
    try:
        with open(f"cases/{case_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def ask_patient(history: list, case_id: str) -> str:
    """根據對話歷史生成 AI 病人的回應"""
    case_data = load_case_data(case_id)
    if not case_data:
        return "錯誤：找不到指定的案例檔案。"

    # 模擬病人回應
    responses = [
        "[表情痛苦] 醫生，我胸口真的很痛...",
        "[呼吸急促] 疼痛已經持續了2個小時了",
        "[手按胸口] 感覺像有重物壓在胸口上",
        "[臉色蒼白] 有時候會痛到左手臂",
        "[焦慮] 醫生，這會不會是心臟病？",
        "[點頭] 是的，爬樓梯時會更痛",
        "[搖頭] 休息時疼痛會稍微好一點",
        "[擔憂] 我爸爸有心臟病史，我很擔心"
    ]
    
    return random.choice(responses)

def get_feedback_report(full_conversation: list, case_id: str) -> dict:
    """生成診後分析報告"""
    case_data = load_case_data(case_id)
    if not case_data:
        return {"error": f"Case '{case_id}' not found"}

    # 讀取回饋系統配置
    feedback_system = case_data.get("feedback_system", {})
    checklist = feedback_system.get("checklist", [])
    critical_actions = feedback_system.get("critical_actions", [])
    
    # 將對話轉換為文字格式
    conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in full_conversation])
    
    # 簡單的分析
    user_messages = [msg['content'] for msg in full_conversation if msg['role'] == 'user']
    conversation_text_lower = " ".join(user_messages).lower()
    
    # 計算覆蓋率
    covered_items = 0
    for item in checklist:
        keywords = item.get('keywords', [])
        if any(keyword.lower() in conversation_text_lower for keyword in keywords):
            covered_items += 1
    
    coverage_percentage = int((covered_items / len(checklist)) * 100) if checklist else 0
    
    # 生成報告
    report_text = f"""### 診後分析報告

**問診覆蓋率：{coverage_percentage}% ({covered_items}/{len(checklist)})**

**詳細評估：**
- ✅ 基本問診技巧：學生展現了良好的溝通能力
- ⚠️ 系統性問診：建議按照 OPQRST 結構進行問診
- ❌ 關鍵決策：需要加強臨床決策能力

**關鍵行動評估：**
- 建議立即安排 ECG 心電圖檢查
- 需要測量生命體徵
- 考慮心臟科會診

### 總結與建議

**優點：**
- 問診覆蓋率達 {coverage_percentage}%
- 學生展現了基本的問診技巧
- 能夠與病人建立良好的溝通

**改進建議：**
1. **系統性問診**：建議按照 OPQRST 結構進行問診
2. **深入探索**：對於已觸及的主題，可以進一步深入詢問
3. **關鍵決策**：加強臨床決策能力，及時提出關鍵檢查
4. **完整性**：注意問診的全面性，避免遺漏重要項目

**具體建議：**
- 多練習標準化問診流程
- 加強對關鍵症狀的識別能力
- 提升臨床決策的時效性
"""

    return {"report_text": report_text}

def calculate_coverage(history: list, case_id: str) -> int:
    """計算問診覆蓋率"""
    case_data = load_case_data(case_id)
    if not case_data:
        return 0
    
    feedback_system = case_data.get("feedback_system", {})
    checklist = feedback_system.get("checklist", [])
    
    if not checklist:
        return 0
    
    # 將對話歷史轉換為文字
    conversation_text = " ".join([msg['content'] for msg in history if msg['role'] == 'user'])
    conversation_text = conversation_text.lower()
    
    covered_items = 0
    total_items = len(checklist)
    
    for item in checklist:
        # 檢查關鍵字是否在對話中出現
        keywords = item.get('keywords', [])
        if any(keyword.lower() in conversation_text for keyword in keywords):
            covered_items += 1
    
    # 計算覆蓋率百分比
    coverage_percentage = int((covered_items / total_items) * 100) if total_items > 0 else 0
    return min(coverage_percentage, 100)  # 確保不超過 100%

# Flask 路由
@app.route('/ask_patient', methods=['POST'])
def ask_patient_route():
    data = request.json
    history = data.get('history', [])
    case_id = data.get('case_id')
    
    result = ask_patient(history=history, case_id=case_id)
    coverage = calculate_coverage(history, case_id)
    
    return jsonify({"reply": result, "coverage": coverage})

@app.route('/get_feedback_report', methods=['POST'])
def get_feedback_report_route():
    data = request.json
    result = get_feedback_report(full_conversation=data.get('full_conversation'), case_id=data.get('case_id'))
    return jsonify(result)

@app.route('/get_detailed_report', methods=['POST'])
def get_detailed_report_route():
    """生成詳細報告的 API 端點"""
    data = request.json
    result = get_feedback_report(full_conversation=data.get('full_conversation'), case_id=data.get('case_id'))
    return jsonify(result)

# 啟動器
if __name__ == '__main__':
    print("簡化版 Flask 開發伺服器正在 http://127.0.0.1:5002 上運行...")
    app.run(host='0.0.0.0', port=5002, debug=True)
