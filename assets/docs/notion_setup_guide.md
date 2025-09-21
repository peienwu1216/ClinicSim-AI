# 🔧 Notion 串接修復指南

## 🚨 問題診斷

您的 Notion 串接業務沒有正常執行的原因是：

1. **環境變數未設定** - `NOTION_API_KEY` 和 `NOTION_DATABASE_ID` 為空
2. **配置文件缺失** - 沒有 `.env` 文件
3. **依賴套件** - 需要確認 `notion-client` 是否已安裝

## 🛠️ 解決步驟

### 步驟 1: 安裝 Notion 依賴

```bash
pip install notion-client
```

### 步驟 2: 創建 Notion Integration

1. 前往 [Notion Developers](https://www.notion.so/my-integrations)
2. 點擊 "New integration"
3. 填寫整合資訊：
   - **Name**: `ClinicSim-AI Integration`
   - **Associated workspace**: 選擇您的工作區
4. 點擊 "Submit" 創建整合
5. 複製 "Internal Integration Token" (以 `secret_` 開頭)

### 步驟 3: 創建 Notion Database

1. 在 Notion 中創建新的 Database
2. 設定以下欄位：

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| **Name** | Title | 案例名稱 |
| **學習日期** | Date | 問診日期 |
| **案例類型** | Select | 內科/外科/急診等 |
| **問診表現** | Number | 評分 (1-10) |
| **臨床決策** | Number | 評分 (1-10) |
| **知識應用** | Number | 評分 (1-10) |
| **總體評價** | Number | 總分 (1-10) |
| **複習狀態** | Select | 待複習/已複習/已掌握 |

3. 複製 Database ID (從 URL 中獲取，32 位字符)

### 步驟 4: 設定權限

1. 在 Database 頁面右上角點擊 "Share"
2. 點擊 "Add people, emails, groups, or integrations"
3. 搜尋並選擇您創建的 "ClinicSim-AI Integration"
4. 給予 "Can edit" 權限

### 步驟 5: 設定環境變數

#### Windows PowerShell:
```powershell
$env:NOTION_API_KEY="secret_your_integration_token_here"
$env:NOTION_DATABASE_ID="your_32_character_database_id_here"
$env:NOTION_ENABLED="true"
```

#### 永久設定 (編輯 .env 文件):
```env
NOTION_ENABLED=true
NOTION_API_KEY=secret_your_integration_token_here
NOTION_DATABASE_ID=your_32_character_database_id_here
```

### 步驟 6: 測試整合

運行測試腳本：

```bash
python examples/notion_sync_example.py
```

## 🔍 驗證步驟

1. **檢查環境變數**：
   ```bash
   echo $env:NOTION_API_KEY
   echo $env:NOTION_DATABASE_ID
   ```

2. **測試連接**：
   - 啟動應用程式
   - 生成一個測試報告
   - 檢查是否成功同步到 Notion

3. **查看日誌**：
   - 應該看到 "✅ Notion 客戶端初始化成功"
   - 報告生成時應該看到同步成功的訊息

## 🚨 常見問題

### 問題 1: "Notion API 未配置"
**解決方案**: 確認環境變數已正確設定

### 問題 2: "Notion 連線失敗"
**解決方案**: 
- 檢查 API Key 是否有效
- 確認 Database ID 正確
- 確認整合有適當權限

### 問題 3: "找不到頁面"
**解決方案**: 
- 確認 Database ID 格式正確 (32 位字符)
- 確認整合已添加到 Database

## 📞 需要幫助？

如果按照以上步驟仍有問題，請提供：
1. 錯誤訊息截圖
2. 環境變數設定狀況
3. Notion Integration 設定截圖

---
**注意**: 確保您的 Notion API Key 以 `secret_` 開頭，Database ID 為 32 位字符。
