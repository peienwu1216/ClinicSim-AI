# 🍋 Lemonade Server API 設定指南

## 概述

ClinicSim-AI 現在使用 Lemonade Server 的 OpenAI 兼容 API 來獲得 NPU 加速，而不是在本地載入模型。這是最簡單且最穩定的方法。

## 前置需求

1. **Lemonade Server 正在運行**：確保 `http://localhost:8000` 上有 Lemonade Server
2. **Qwen-2.5-7B-Instruct-Hybrid 模型已載入**：在 Lemonade Server 中
3. **Python 環境**：只需要基本的 HTTP 請求庫

## 快速測試

### 1. 測試 Lemonade Server 連接

```bash
# 測試伺服器是否運行
curl http://localhost:8000/health

# 測試模型列表
curl http://localhost:8000/api/v1/models
```

### 2. 測試聊天 API

```bash
# PowerShell 測試
curl -X POST http://localhost:8000/api/v1/chat/completions `
  -H "Content-Type: application/json" `
  -d "{\"model\":\"Qwen-2.5-7B-Instruct-Hybrid\",\"messages\":[{\"role\":\"user\",\"content\":\"你好，說明一下Hybrid是怎麼跑的？\"}],\"stream\":false}"
```

### 3. 使用 Python 測試腳本

```bash
# 執行完整的 API 測試
python test_lemonade_server_api.py
```

## 環境設定

創建 `.env` 檔案：

```env
# AI 提供者設定
AI_PROVIDER=lemonade_npu

# Lemonade Server 設定
LEMONADE_BASE_URL=http://localhost:8000/api/v1
LEMONADE_NPU_MODEL=Qwen-2.5-7B-Instruct-Hybrid
LEMONADE_API_KEY=lemonade

# 基本設定
DEBUG=false
HOST=0.0.0.0
PORT=5001
DEFAULT_CASE_ID=case_chest_pain_acs_01
```

## 啟動應用程式

### 方法 1：使用批次檔 (Windows)

```bash
start_npu.bat
```

### 方法 2：使用 Python 腳本

```bash
python start_npu.py
```

### 方法 3：手動啟動

```bash
# 設定環境變數
set AI_PROVIDER=lemonade_npu
set LEMONADE_BASE_URL=http://localhost:8000/api/v1
set LEMONADE_NPU_MODEL=Qwen-2.5-7B-Instruct-Hybrid
set LEMONADE_API_KEY=lemonade

# 啟動後端
python main.py

# 在另一個終端啟動前端
streamlit run app.py
```

## 技術架構

### 新的架構流程

```
ClinicSim-AI Frontend (Streamlit)
    ↓ HTTP Request
ClinicSim-AI Backend (Flask)
    ↓ OpenAI Compatible API
Lemonade Server (localhost:8000)
    ↓ NPU Processing
AMD Ryzen AI NPU
    ↓ Response
Qwen-2.5-7B-Instruct-Hybrid Model
```

### API 端點

- **聊天完成**：`POST /api/v1/chat/completions`
- **模型列表**：`GET /api/v1/models`
- **健康檢查**：`GET /health`

### 請求格式

```json
{
  "model": "Qwen-2.5-7B-Instruct-Hybrid",
  "messages": [
    {
      "role": "user",
      "content": "患者主訴胸痛，請列出需要詢問的關鍵問題。"
    }
  ],
  "stream": false,
  "max_tokens": 200
}
```

## 優勢

### 1. 簡化部署
- **無需本地模型載入**：避免 dtype/device 問題
- **無需複雜依賴**：不需要 lemonade-sdk 的本地模型載入
- **更穩定的運行**：減少本地環境問題

### 2. 更好的效能
- **NPU 加速**：由 Lemonade Server 處理
- **模型優化**：Server 端已優化模型載入
- **資源管理**：Server 端統一管理資源

### 3. 更容易維護
- **集中管理**：模型更新在 Server 端
- **版本控制**：Server 端控制模型版本
- **監控調試**：統一的日誌和監控

## 故障排除

### 1. 連接問題

```bash
# 檢查 Lemonade Server 是否運行
curl http://localhost:8000/health

# 如果失敗，檢查：
# - Lemonade Server 是否啟動
# - 端口 8000 是否被佔用
# - 防火牆設定
```

### 2. 模型問題

```bash
# 檢查可用模型
curl http://localhost:8000/api/v1/models

# 確認 Qwen-2.5-7B-Instruct-Hybrid 在列表中
```

### 3. API 問題

```bash
# 測試基本 API 調用
python test_lemonade_server_api.py

# 檢查錯誤訊息和回應
```

## 效能監控

### 1. 回應時間
- **正常範圍**：1-5 秒
- **NPU 加速**：比 CPU 快 3-5 倍
- **網路延遲**：通常 < 100ms

### 2. 資源使用
- **記憶體**：由 Lemonade Server 管理
- **CPU**：ClinicSim-AI 只處理 HTTP 請求
- **NPU**：由 Lemonade Server 使用

## 下一步

1. **確保 Lemonade Server 運行**：`http://localhost:8000`
2. **測試 API 連接**：`python test_lemonade_server_api.py`
3. **啟動應用程式**：`python main.py`
4. **啟動前端**：`streamlit run app.py`

## 支援

如果遇到問題：
1. 檢查 Lemonade Server 狀態
2. 確認模型已載入
3. 測試 API 連接
4. 查看錯誤日誌

這種方法避免了所有本地模型載入的問題，讓您專注於使用 NPU 加速功能！🚀
