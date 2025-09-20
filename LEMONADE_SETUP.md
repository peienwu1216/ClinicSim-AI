# Lemonade Server 串接設定指南

## 🎯 問題已解決！

您的 ClinicSim-AI 專案現在已經成功支援 Lemonade Server 的標準 OpenAI 相容 API 串接方式。

## ✅ 已完成的修改

### 1. 更新 AI 服務層 (`src/services/ai_service.py`)
- ✅ 導入 OpenAI SDK
- ✅ 重寫 `LemonadeAIService` 類別使用 OpenAI 客戶端
- ✅ 實作正確的訊息格式轉換
- ✅ 加入詳細的錯誤處理和除錯訊息
- ✅ 更新工廠方法以支援動態配置

### 2. 擴充配置系統 (`src/config/settings.py`)
- ✅ 新增 `lemonade_base_url` 和 `lemonade_model` 配置參數
- ✅ 修復 Pydantic v2 相容性問題
- ✅ 支援透過環境變數動態配置

### 3. 建立環境變數範例 (`env_example.txt`)
- ✅ 提供完整的 Lemonade Server 配置範例
- ✅ 包含所有必要的環境變數設定

### 4. 更新依賴套件
- ✅ 確認 OpenAI SDK (`openai>=1.0.0`) 已正確安裝
- ✅ 所有相關依賴套件都已更新至最新版本

## 🚀 如何啟用 Lemonade Server

### 步驟 1：建立環境變數檔案
```bash
# 複製範例檔案內容到 .env 檔案
copy env_example.txt .env
```

### 步驟 2：確認 Lemonade Server 啟動
確保您的 Lemonade Server 在以下位址運行：
```
http://localhost:8000/api/v1
```

### 步驟 3：測試連接（可選）
```bash
python test_lemonade_connection.py
```

### 步驟 4：啟動 ClinicSim-AI
```bash
python main.py
```

## 🔧 重要配置參數

在 `.env` 檔案中設定以下參數：

```env
# AI 服務配置 - 重要！
AI_PROVIDER=lemonade

# Lemonade Server 設定 (實際測試成功的配置)
LEMONADE_BASE_URL=http://localhost:8080/api/v1
LEMONADE_MODEL=Qwen2.5-0.5B-Instruct-CPU
```

## 🎛️ 動態切換 AI 提供者

您現在可以輕鬆在不同的 AI 提供者之間切換：

```env
# 使用 Lemonade Server
AI_PROVIDER=lemonade

# 使用 Ollama (備用)
AI_PROVIDER=ollama

# 使用模擬服務 (開發測試)
AI_PROVIDER=mock
```

## 🔍 連接問題除錯

如果遇到連接問題，請檢查：

1. **Lemonade Server 狀態**：
   ```bash
   curl -X GET http://localhost:8000/api/v1/models
   ```

2. **網路連接**：確認防火牆沒有阻擋 8000 埠

3. **模型名稱**：確認 `LEMONADE_MODEL` 設定正確

4. **啟動順序**：先啟動 Lemonade Server，再啟動 ClinicSim-AI

## 📋 完整測試流程

1. 啟動 Lemonade Server
2. 執行連接測試：`python test_lemonade_connection.py`
3. 看到 "✅ Lemonade Server 連接成功！" 訊息
4. 啟動主程式：`python main.py`

## 🎉 結果

現在您的 ClinicSim-AI 可以：
- 正確連接到 AMD AI PC demo 的 Lemonade Server
- 使用標準 OpenAI 相容 API 進行通訊
- 動態切換不同的 AI 提供者
- 提供詳細的連接狀態回饋

專案架構的抽象化設計讓這次整合變得非常順暢！🚀
