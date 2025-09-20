import os
import json
import random
import re
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# 導入我們新建的 RAG 系統
from rag_handler import rag_system

# --- 自動環境偵測與設定 ---
load_dotenv() # 從 .env 檔案載入環境變數

# 執行路徑旗標
PATH_A_DEMO = False    # AMD AI PC (Lemonade)
PATH_B_DEVELOPMENT = False # Mac/Windows (Ollama)

# 偵測路徑 A：優先偵測 Lemonade Server
try:
    # 這裡假設 lemonade server 會透過某種方式 expose 函式
    # 由於我們沒有 lemonade 的具體 API，我們將模擬一個 expose 裝飾器
    # 在真實的 lemonade 環境中，你可能需要從 lemonade 導入 expose
    from lemonade import expose
    PATH_A_DEMO = True
    print("✅ 偵測到 Lemonade 環境 -> 啟用【路線 A: Demo 模式】")
except (ImportError, ModuleNotFoundError):
    # 建立一個假的 expose 裝飾器，讓程式碼在開發模式下也能運行
    def expose(func):
        return func
        
    # 偵測路徑 B：若無 Lemonade，則偵測 Ollama 設定
    try:
        import ollama
        PATH_B_DEVELOPMENT = True
        OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")
        OLLAMA_CLIENT = ollama.Client(host=OLLAMA_HOST)
        print("✅ 偵測到 Ollama 設定 -> 啟用【路線 B: 開發模式】")
        print(f"   使用模型: {OLLAMA_MODEL}")
    except ImportError:
        print("❌ 錯誤：缺少 `ollama` 套件。請執行 `pip install ollama`。")
    except Exception as e:
        print(f"🟡 警告：Ollama 連接失敗: {e}")
        print("🟡 後端將以無 AI 功能的狀態運行。")

# --- Flask App 初始化 ---
# 在兩種路徑下我們都需要 Flask app
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# --- 輔助函式 ---
def load_case_data(case_id: str) -> dict:
    """根據 case_id 載入對應的教案 JSON 檔案"""
    try:
        with open(f"cases/{case_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# --- 核心 AI 服務函式 (雙路徑實作) ---
@expose
def ask_patient(history: list, case_id: str) -> str:
    """根據對話歷史生成 AI 病人的回應"""
    case_data = load_case_data(case_id)
    if not case_data:
        return "錯誤：找不到指定的案例檔案。"

    system_prompt = f"""
    你是一位模擬病人（標準化病人）。你的所有輸出必須使用『繁體中文』。
    【角色設定與回應規則】
    1. 僅回答學生（user）直接詢問的內容，不主動透露未被詢問的資訊。
    2. 回覆格式需為「[動作/情緒] 對話內容」。
    3. 嚴格依據下方個案資料作答。
    【個案行為規範】: {json.dumps(case_data.get("ai_instructions", {}), ensure_ascii=False)}
    【個案資料】: {json.dumps(case_data.get("patient_story_data", {}), ensure_ascii=False)}
    請根據以上資訊和對話歷史，作為病人，以「繁體中文」回覆下一句話。切記絕對規則：所有輸出文字都要是繁體中文！！
    """
    messages = [{"role": "system", "content": system_prompt}] + history

    # --- 路線 A: Demo (Lemonade) ---
    if PATH_A_DEMO:
        print("[Lemonade] 正在呼叫語言模型...")
        # 這裡是你實際呼叫 lemonade LLM 的地方
        # response = lemonade.llm.chat(model="Qwen3-1.7B-GGUF", messages=messages)
        # return response.choices[0].message.content
        return "[From Lemonade] [表情痛苦] 醫生，我胸口真的很痛..."

    # --- 路線 B: 開發 (Ollama) ---
    elif PATH_B_DEVELOPMENT:
        model_name = os.getenv("OLLAMA_MODEL", "llama3:8b")
        print(f"[Ollama] 正在呼叫模型: {model_name}...")
        response = OLLAMA_CLIENT.chat(
            model=model_name,
            messages=messages
        )
        return response['message']['content']
        
    # --- 備用：無 AI 環境 ---
    else:
        return "[無 AI] 這是一個備用回應，請檢查你的 Lemonade 或 .env 設定。"

@expose
def get_feedback_report(full_conversation: list, case_id: str) -> dict:
    """
    生成診後分析報告【已整合 RAG 功能】。
    """
    print("\n[報告生成] 開始生成分析報告...")
    
    case_data = load_case_data(case_id)
    if not case_data:
        return {"error": f"Case '{case_id}' not found"}

    # 讀取回饋系統配置
    feedback_system = case_data.get("feedback_system", {})
    checklist = feedback_system.get("checklist", [])
    critical_actions = feedback_system.get("critical_actions", [])
    
    # 將對話轉換為文字格式
    conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in full_conversation])
    
    # 將檢查清單轉換為文字格式
    checklist_text = "\n".join([f"- {item['point']} (類別: {item['category']})" for item in checklist])
    
    # 將關鍵行動轉換為文字格式
    critical_actions_text = "\n".join([f"- {action}" for action in critical_actions])

    # 1. 模擬評分，並找出需要 RAG 提供建議的弱點
    # 在真實情境中，這會是你的評分引擎的輸出
    student_weakness_query = "為什麼在急性胸痛的案例中，ECG 心電圖是第一優先的檢查？"
    
    # 2. 使用 RAG 系統搜尋相關知識
    # 這一呼叫是獨立於語言模型的
    rag_context = rag_system.search(student_weakness_query)
    
    # 3. 將 RAG 結果注入到 Prompt 中，交給語言模型進行總結
    prompt = f"""
    你是一位資深的 OSCE 臨床教師。請根據以下背景資料和學生的對話紀錄，生成一份專業的診後分析報告。

    ### 學生表現
    {conversation_text}

    ### 評估清單
    {checklist_text}

    ### 關鍵行動
    {critical_actions_text}

    ### 相關臨床指引 (由 RAG 系統提供)
    {rag_context}

    ### 你的任務
    請基於以上所有資訊，撰寫一份包含以下幾點的分析報告：
    1.  **關鍵錯失點**: 學生在問診或決策中可能忽略的重點。
    2.  **建設性建議**: 根據 RAG 提供的臨床指引，給出具體、有依據的改進建議。
    3.  **評估等級**: 每項給出等級：✅(完整)、⚠️(部分)、❌(未問)
    4.  **具體依據**: 引用學生具體提問作為評估依據

    輸出格式：
    ### 診後分析報告
    - [等級] [項目]：具體依據
    ### 總結與建議
    改進建議
    """

    messages = [{"role": "system", "content": prompt}]

    # --- 路線 A: Demo (Lemonade) ---
    if PATH_A_DEMO:
        print("[Lemonade] 正在呼叫語言模型生成分析報告...")
        # 這裡是你實際呼叫 lemonade LLM 的地方
        # response = lemonade.llm.chat(model="Qwen3-1.7B-GGUF", messages=messages)
        # return {"report_text": response.choices[0].message.content}
        return {"report_text": f"[From Lemonade] 報告分析：學生應優先考慮 ECG。\n\n證據：{rag_context}"}

    # --- 路線 B: 開發 (Ollama) ---
    elif PATH_B_DEVELOPMENT:
        print(f"[Ollama] 正在生成報告...")
        try:
            response = OLLAMA_CLIENT.chat(
                model=os.getenv("OLLAMA_MODEL"),
                messages=messages
            )
            report_text = response['message']['content']
        except Exception as e:
            print(f"[Ollama] 生成報告失敗，使用備用方案: {e}")
            # 備用方案：使用增強版分析
            user_messages = [msg['content'] for msg in full_conversation if msg['role'] == 'user']
            conversation_analysis = analyze_conversation_enhanced(user_messages, checklist, critical_actions)
            report_text = f"{conversation_analysis}\n\n### RAG 提供的臨床指引\n{rag_context}"
        
        return {"report_text": report_text}
        
    # --- 備用：無 AI 環境 ---
    else:
        return {"error": "無法生成分析報告：未找到 AI 環境設定。"}

@expose
def get_detailed_report(full_conversation: list, case_id: str) -> dict:
    """
    生成詳細分析報告【使用 LLM + RAG】。
    這是第二階段的完整報告生成功能。
    """
    print("\n[詳細報告生成] 開始生成完整分析報告...")
    
    case_data = load_case_data(case_id)
    if not case_data:
        return {"error": f"Case '{case_id}' not found"}

    # 讀取回饋系統配置
    feedback_system = case_data.get("feedback_system", {})
    checklist = feedback_system.get("checklist", [])
    critical_actions = feedback_system.get("critical_actions", [])
    
    # 將對話轉換為文字格式
    conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in full_conversation])
    
    # 將檢查清單轉換為文字格式
    checklist_text = "\n".join([f"- {item['point']} (類別: {item['category']})" for item in checklist])
    
    # 將關鍵行動轉換為文字格式
    critical_actions_text = "\n".join([f"- {action}" for action in critical_actions])

    # 1. 使用 RAG 系統搜尋相關臨床指引
    # 根據對話內容動態生成查詢
    user_messages = [msg['content'] for msg in full_conversation if msg['role'] == 'user']
    conversation_summary = " ".join(user_messages)
    
    # 生成多個相關查詢來獲得更全面的知識
    rag_queries = [
        "急性胸痛診斷流程和檢查順序",
        "ECG 心電圖在胸痛評估中的重要性",
        "STEMI 和不穩定型心絞痛的診斷標準",
        "胸痛問診的 OPQRST 技巧和重點"
    ]
    
    # 搜尋並整合 RAG 結果，包含引註資訊
    rag_contexts = []
    citations = []  # 用於追蹤引註來源
    
    for i, query in enumerate(rag_queries, 1):
        context = rag_system.search(query, k=2)
        if context and "RAG 系統未初始化" not in context:
            # 解析來源資訊
            source_info = f"臨床指引 {i}"
            citations.append({
                "id": i,
                "query": query,
                "source": source_info,
                "content": context
            })
            rag_contexts.append(f"### 關於 {query} [引註 {i}]\n{context}")
    
    combined_rag_context = "\n\n".join(rag_contexts) if rag_contexts else "未找到相關臨床指引"
    
    # 2. 構建詳細的 LLM Prompt
    detailed_prompt = f"""
    你是一位資深的 OSCE 臨床教師和心臟科專家。請根據以下資訊生成一份詳細的診後分析報告。

    ### 學生問診表現
    {conversation_text}

    ### 評估標準
    **檢查清單：**
    {checklist_text}

    **關鍵行動：**
    {critical_actions_text}

    ### 相關臨床指引 (RAG 系統提供)
    {combined_rag_context}

    ### 你的任務
    請生成一份專業、詳細的分析報告，包含以下部分：

    ## 1. 問診表現評估
    - 系統性分析學生的問診技巧
    - 指出優點和不足之處
    - 引用具體的對話內容作為依據

    ## 2. 臨床決策分析
    - 評估學生的臨床思維過程
    - 分析是否識別出關鍵症狀和危險因子
    - 評估決策的時效性和準確性

    ## 3. 知識應用評估
    - 評估學生對急性胸痛診斷流程的理解
    - 分析是否遵循標準化問診程序
    - 評估對關鍵檢查的認知

    ## 4. 改進建議
    - 基於 RAG 提供的臨床指引，給出具體建議
    - 提供實用的學習資源和練習方向
    - 建議下一步的學習重點

    ## 5. 評分總結
    - 給出各項目的具體評分 (1-10分)
    - 提供總體評價和等級
    - 建議是否需要額外練習

    ### 重要要求：
    1. 必須使用繁體中文撰寫整份報告
    2. 在引用臨床指引時，必須使用 [引註 X] 的格式標記，例如 [引註 1]、[引註 2] 等
    3. 每個建議都應該引用相應的臨床指引，格式為：根據 [引註 X] 的指引...
    4. 語氣專業但友善，適合醫學生學習使用
    5. 確保所有醫學術語使用正確的繁體中文
    
    ### 引註使用範例：
    - 根據 [引註 1] 的診斷流程指引，ECG 檢查應在 10 分鐘內完成
    - 如 [引註 2] 所述，心電圖是急性胸痛評估的第一優先檢查
    - 按照 [引註 3] 的診斷標準，STEMI 需要立即處理
    """

    messages = [{"role": "system", "content": detailed_prompt}]

    # --- 路線 A: Demo (Lemonade) ---
    if PATH_A_DEMO:
        print("[Lemonade] 正在生成詳細報告...")
        # 這裡是你實際呼叫 lemonade LLM 的地方
        # response = lemonade.llm.chat(model="Qwen3-1.7B-GGUF", messages=messages)
        # return {"report_text": response.choices[0].message.content}
        report_text = f"[From Lemonade] 詳細報告分析：\n\n基於 RAG 提供的臨床指引：\n{combined_rag_context[:200]}...\n\n這是一份來自 Lemonade 的詳細分析報告..."
        
        # 添加基於 RAG 的建議
        if citations:
            rag_suggestions = "\n\n## 基於臨床指引的建議\n\n"
            for i, citation in enumerate(citations, 1):
                rag_suggestions += f"**根據 [引註 {i}] 的指引：**\n"
                content = citation['content']
                if 'ECG' in content or '心電圖' in content:
                    rag_suggestions += "- ECG 心電圖檢查應在 10 分鐘內完成，這是急性胸痛評估的第一優先檢查\n"
                if 'STEMI' in content:
                    rag_suggestions += "- 疑似 STEMI 時應立即啟動心導管團隊，時間就是心肌\n"
                if 'OPQRST' in content:
                    rag_suggestions += "- 問診應遵循 OPQRST 結構：發作時間、誘發因子、疼痛性質、放射位置、嚴重程度、持續時間\n"
                rag_suggestions += "\n"
            
            report_text += rag_suggestions
        
        return {
            "report_text": report_text,
            "citations": citations,
            "rag_queries": rag_queries
        }

    # --- 路線 B: 開發 (Ollama) ---
    elif PATH_B_DEVELOPMENT:
        print(f"[Ollama] 正在生成詳細報告...")
        try:
            response = OLLAMA_CLIENT.chat(
                model=os.getenv("OLLAMA_MODEL"),
                messages=messages
            )
            report_text = response['message']['content']
        except Exception as e:
            print(f"[Ollama] 生成詳細報告失敗，使用備用方案: {e}")
            # 備用方案：使用增強版分析 + RAG 內容
            user_messages = [msg['content'] for msg in full_conversation if msg['role'] == 'user']
            conversation_analysis = analyze_conversation_enhanced(user_messages, checklist, critical_actions)
            report_text = f"""
# 詳細診後分析報告

{conversation_analysis}

---

## RAG 提供的臨床指引

{combined_rag_context}

---

*註：此為備用詳細報告，包含 RAG 搜尋的臨床指引內容。*
            """
        
        # 如果 LLM 沒有生成引註標記，我們手動添加
        if not re.search(r'\[引註 \d+\]', report_text) and citations:
            # 在報告末尾添加基於 RAG 的建議
            rag_suggestions = "\n\n## 基於臨床指引的建議\n\n"
            for i, citation in enumerate(citations, 1):
                rag_suggestions += f"**根據 [引註 {i}] 的指引：**\n"
                # 從 RAG 內容中提取關鍵建議
                content = citation['content']
                if 'ECG' in content or '心電圖' in content:
                    rag_suggestions += "- ECG 心電圖檢查應在 10 分鐘內完成，這是急性胸痛評估的第一優先檢查\n"
                if 'STEMI' in content:
                    rag_suggestions += "- 疑似 STEMI 時應立即啟動心導管團隊，時間就是心肌\n"
                if 'OPQRST' in content:
                    rag_suggestions += "- 問診應遵循 OPQRST 結構：發作時間、誘發因子、疼痛性質、放射位置、嚴重程度、持續時間\n"
                rag_suggestions += "\n"
            
            report_text += rag_suggestions
        
        return {
            "report_text": report_text,
            "citations": citations,
            "rag_queries": rag_queries
        }
        
    # --- 備用：無 AI 環境 ---
    else:
        return {"error": "無法生成詳細報告：未找到 AI 環境設定。"}


# --- Flask 路由 (僅在開發模式下使用) ---
# 這些路由會將前端的請求，轉發給上面的核心 AI 函式
def analyze_conversation_enhanced(user_messages: list, checklist: list, critical_actions: list) -> str:
    """增強版的對話分析，生成更詳細的報告"""
    conversation_text = " ".join(user_messages).lower()
    
    report_items = []
    covered_count = 0
    partial_count = 0
    
    # 分析每個檢查項目
    for item in checklist:
        keywords = item.get('keywords', [])
        matched_keywords = [kw for kw in keywords if kw.lower() in conversation_text]
        
        if len(matched_keywords) >= 2:  # 多個關鍵字匹配
            report_items.append(f"- ✅ {item['point']}：學生透過提問「{matched_keywords[0]}」等成功問診")
            covered_count += 1
        elif len(matched_keywords) == 1:  # 單一關鍵字匹配
            report_items.append(f"- ⚠️ {item['point']}：學生有相關提問「{matched_keywords[0]}」，但可更深入")
            partial_count += 1
        else:
            report_items.append(f"- ❌ {item['point']}：學生未詢問此項目")
    
    # 分析關鍵行動
    critical_analysis = []
    for action in critical_actions:
        if any(keyword in conversation_text for keyword in ["心電圖", "ECG", "12導程", "立刻", "馬上", "10分"]):
            critical_analysis.append(f"- ✅ 關鍵決策：學生提及了「{action}」")
        else:
            critical_analysis.append(f"- ❌ 關鍵決策：學生未提及「{action}」")
    
    coverage_percentage = int((covered_count / len(checklist)) * 100) if checklist else 0
    
    return f"""### 診後分析報告

**問診覆蓋率：{coverage_percentage}% ({covered_count}/{len(checklist)})**
**完整項目：{covered_count} | 部分項目：{partial_count} | 未覆蓋：{len(checklist) - covered_count - partial_count}**

**詳細評估：**
{chr(10).join(report_items)}

**關鍵行動評估：**
{chr(10).join(critical_analysis)}

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

*註：此為增強版分析報告，提供更詳細的評估和建議。*"""

def analyze_conversation_simple(user_messages: list, checklist: list) -> str:
    """簡單的對話分析，生成基本報告"""
    conversation_text = " ".join(user_messages).lower()
    
    report_items = []
    covered_count = 0
    
    for item in checklist:
        keywords = item.get('keywords', [])
        if any(keyword.lower() in conversation_text for keyword in keywords):
            report_items.append(f"- ✅ {item['point']}：學生有相關提問")
            covered_count += 1
        else:
            report_items.append(f"- ❌ {item['point']}：學生未詢問此項目")
    
    coverage_percentage = int((covered_count / len(checklist)) * 100) if checklist else 0
    
    return f"""### 診後分析報告

**問診覆蓋率：{coverage_percentage}% ({covered_count}/{len(checklist)})**

**詳細評估：**
{chr(10).join(report_items)}

### 總結與建議

本次問診覆蓋了 {coverage_percentage}% 的檢查項目。建議學生：
1. 加強未覆蓋項目的問診技巧
2. 注意問診的系統性和完整性
3. 多練習標準化的問診流程

*註：此為簡化版分析報告，完整版需要更多時間處理。*"""

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
    """生成詳細報告的 API 端點，使用 LLM + RAG"""
    data = request.json
    result = get_detailed_report(full_conversation=data.get('full_conversation'), case_id=data.get('case_id'))
    return jsonify(result)

# --- 啟動器 ---
# 只有在「開發模式」下，這個 Flask 伺服器才會直接被啟動。
# 在「Demo 模式」下，這個檔案會被 Lemonade 作為模組載入，不會執行這一段。
if __name__ == '__main__' and not PATH_A_DEMO:
    if PATH_B_DEVELOPMENT:
        print(f"Flask 開發伺服器正在 http://127.0.0.1:5002 上運行...")
        app.run(host='0.0.0.0', port=5002, debug=True)
    else:
        print("無法啟動：未找到 Lemonade 或 Ollama 設定。請檢查你的環境。")