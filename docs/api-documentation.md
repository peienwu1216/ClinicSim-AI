# 📚 API 文檔

> **完整的 API 參考** | 所有端點的詳細說明

## 🌐 API 概述

ClinicSim-AI 提供 RESTful API 接口，支援前端應用程式和第三方整合。

### 基礎資訊
- **Base URL**: `http://localhost:5001`
- **Content-Type**: `application/json`
- **認證**: 目前無需認證（未來版本將支援）

### 響應格式
所有 API 響應都使用 JSON 格式：

```json
{
    "success": true,
    "data": {...},
    "message": "操作成功"
}
```

錯誤響應：
```json
{
    "success": false,
    "error": "錯誤訊息",
    "code": "ERROR_CODE"
}
```

## 🔍 端點列表

### 1. 健康檢查

#### GET /health
檢查服務器健康狀態

**請求**
```http
GET /health
```

**響應**
```json
{
    "service": "ClinicSim-AI",
    "status": "healthy",
    "version": "2.0.0",
    "timestamp": "2024-09-20T09:00:00Z"
}
```

### 2. AI 病人對話

#### POST /ask_patient
與 AI 模擬病人進行對話

**請求**
```http
POST /ask_patient
Content-Type: application/json

{
    "history": [
        {"role": "user", "content": "你好，請問你哪裡不舒服？"},
        {"role": "assistant", "content": "我胸口很痛..."}
    ],
    "case_id": "case_chest_pain_acs_01"
}
```

**響應**
```json
{
    "reply": "[表情痛苦] 醫生，我胸口很痛，痛了一個小時了...",
    "coverage": 15,
    "vital_signs": {
        "blood_pressure": "140/90",
        "heart_rate": 95,
        "respiratory_rate": 22,
        "temperature": 37.2,
        "oxygen_saturation": 98
    }
}
```

**參數說明**
- `history`: 對話歷史列表
- `case_id`: 案例 ID

### 3. 報告生成

#### POST /get_feedback_report
生成即時評估報告

**請求**
```http
POST /get_feedback_report
Content-Type: application/json

{
    "full_conversation": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "我胸口很痛"}
    ],
    "case_id": "case_chest_pain_acs_01"
}
```

**響應**
```json
{
    "report_text": "### 診後分析報告\n\n- ✅ 問診開場：學生成功建立良好關係...",
    "coverage_percentage": 25,
    "key_points_covered": [
        "問診開場",
        "疼痛描述"
    ],
    "missing_points": [
        "既往史詢問",
        "用藥史詢問"
    ]
}
```

#### POST /get_detailed_report
生成詳細分析報告（使用 LLM + RAG）

**請求**
```http
POST /get_detailed_report
Content-Type: application/json

{
    "full_conversation": [...],
    "case_id": "case_chest_pain_acs_01"
}
```

**響應**
```json
{
    "report_text": "## 詳細診後分析報告\n\n### 問診表現評估...",
    "citations": [
        {
            "id": 1,
            "query": "急性胸痛診斷流程",
            "source": "臨床指引 1",
            "content": "急性胸痛是急診科最常見的主訴..."
        }
    ],
    "rag_queries": [
        "急性胸痛診斷流程和檢查順序",
        "ECG 心電圖在胸痛評估中的重要性"
    ],
    "scores": {
        "interview_skills": 7,
        "clinical_reasoning": 6,
        "knowledge_application": 8,
        "overall": 7
    }
}
```

### 4. 案例管理

#### GET /cases
獲取可用案例列表

**請求**
```http
GET /cases
```

**響應**
```json
{
    "cases": [
        {
            "id": "case_chest_pain_acs_01",
            "name": "急性胸痛案例",
            "description": "急性冠心症候群案例",
            "difficulty": "中等",
            "estimated_time": "15-20 分鐘"
        }
    ],
    "count": 1
}
```

#### GET /cases/{case_id}
獲取特定案例詳情

**請求**
```http
GET /cases/case_chest_pain_acs_01
```

**響應**
```json
{
    "id": "case_chest_pain_acs_01",
    "name": "急性胸痛案例",
    "patient_profile": {
        "age": 55,
        "gender": "男性",
        "chief_complaint": "胸痛"
    },
    "ai_instructions": {
        "personality": "焦慮、疼痛",
        "response_style": "簡短、痛苦"
    },
    "feedback_system": {
        "checklist": [...],
        "critical_actions": [...]
    }
}
```

### 5. RAG 系統

#### GET /rag/status
獲取 RAG 系統狀態

**請求**
```http
GET /rag/status
```

**響應**
```json
{
    "status": "initialized",
    "embedding_model": "nomic-ai/nomic-embed-text-v1.5",
    "index_path": "/path/to/faiss_index",
    "search_k": 3,
    "total_documents": 1,
    "last_updated": "2024-09-20T08:00:00Z"
}
```

## 🔧 錯誤處理

### HTTP 狀態碼

| 狀態碼 | 說明 | 範例 |
|--------|------|------|
| 200 | 成功 | 請求成功處理 |
| 400 | 請求錯誤 | 參數格式錯誤 |
| 404 | 資源不存在 | 案例 ID 不存在 |
| 500 | 服務器錯誤 | 內部錯誤 |

### 錯誤響應格式

```json
{
    "success": false,
    "error": "Case 'invalid_case' not found",
    "code": "CASE_NOT_FOUND",
    "details": {
        "case_id": "invalid_case",
        "available_cases": ["case_chest_pain_acs_01"]
    }
}
```

### 常見錯誤碼

| 錯誤碼 | 說明 | 解決方案 |
|--------|------|----------|
| `CASE_NOT_FOUND` | 案例不存在 | 檢查案例 ID |
| `INVALID_INPUT` | 輸入格式錯誤 | 檢查請求格式 |
| `AI_SERVICE_ERROR` | AI 服務錯誤 | 檢查 AI 服務狀態 |
| `RAG_SERVICE_ERROR` | RAG 服務錯誤 | 檢查 RAG 索引 |

## 📝 使用範例

### Python 客戶端

```python
import requests

# 基礎配置
BASE_URL = "http://localhost:5001"

# 健康檢查
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# 開始對話
conversation = []
response = requests.post(
    f"{BASE_URL}/ask_patient",
    json={
        "history": conversation,
        "case_id": "case_chest_pain_acs_01"
    }
)
data = response.json()

# 添加 AI 回應到對話
conversation.append({"role": "user", "content": "你好"})
conversation.append({"role": "assistant", "content": data["reply"]})

# 生成報告
response = requests.post(
    f"{BASE_URL}/get_detailed_report",
    json={
        "full_conversation": conversation,
        "case_id": "case_chest_pain_acs_01"
    }
)
report = response.json()
print(report["report_text"])
```

### JavaScript 客戶端

```javascript
const BASE_URL = 'http://localhost:5001';

// 健康檢查
async function checkHealth() {
    const response = await fetch(`${BASE_URL}/health`);
    return await response.json();
}

// 與 AI 病人對話
async function askPatient(history, caseId) {
    const response = await fetch(`${BASE_URL}/ask_patient`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            history: history,
            case_id: caseId
        })
    });
    return await response.json();
}

// 生成詳細報告
async function getDetailedReport(conversation, caseId) {
    const response = await fetch(`${BASE_URL}/get_detailed_report`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            full_conversation: conversation,
            case_id: caseId
        })
    });
    return await response.json();
}
```

### cURL 範例

```bash
# 健康檢查
curl -X GET http://localhost:5001/health

# 獲取案例列表
curl -X GET http://localhost:5001/cases

# 與 AI 病人對話
curl -X POST http://localhost:5001/ask_patient \
  -H "Content-Type: application/json" \
  -d '{
    "history": [{"role": "user", "content": "你好"}],
    "case_id": "case_chest_pain_acs_01"
  }'

# 生成詳細報告
curl -X POST http://localhost:5001/get_detailed_report \
  -H "Content-Type: application/json" \
  -d '{
    "full_conversation": [
      {"role": "user", "content": "你好"},
      {"role": "assistant", "content": "我胸口很痛"}
    ],
    "case_id": "case_chest_pain_acs_01"
  }'
```

## 🔒 安全考慮

### 輸入驗證
- 所有輸入都經過 Pydantic 驗證
- 防止 SQL 注入和 XSS 攻擊
- 路徑遍歷攻擊防護

### 速率限制
```python
# 未來版本將實作速率限制
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/ask_patient')
@limiter.limit("10 per minute")
def ask_patient():
    pass
```

### CORS 配置
```python
from flask_cors import CORS

CORS(app, origins=[
    "http://localhost:8501",  # Streamlit 前端
    "https://yourdomain.com"  # 生產環境
])
```

## 📊 監控和日誌

### 日誌格式
```json
{
    "timestamp": "2024-09-20T09:00:00Z",
    "level": "INFO",
    "service": "ClinicSim-AI",
    "endpoint": "/ask_patient",
    "method": "POST",
    "status_code": 200,
    "response_time": 1.23,
    "user_agent": "Mozilla/5.0...",
    "request_id": "req_123456"
}
```

### 指標收集
- API 響應時間
- 錯誤率
- 請求量
- 資源使用率

## 🚀 版本控制

### API 版本
- 當前版本：v2.0.0
- 向後兼容性：保持 v1.x 兼容
- 版本標頭：`API-Version: 2.0`

### 變更日誌
- v2.0.0：重構架構，新增詳細報告功能
- v1.1.0：新增 RAG 系統
- v1.0.0：初始版本

---

**需要更多幫助？查看 [開發者指南](developer-guide.md) 或 [故障排除](troubleshooting.md)** 🎉
