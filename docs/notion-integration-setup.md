# Notion API 整合設定指南

## 概述

ClinicSim-AI 現在支援將學習報告直接匯出到 Notion，作為個人學習記錄管理系統。這個功能可以幫助醫學學生和醫師建立完整的學習檔案。

## 功能特色

- 📊 **自動化報告匯出**: 一鍵將完整的學習報告匯出到 Notion
- 📝 **結構化學習記錄**: 包含評分、建議、引註等完整資訊
- 🔗 **無縫整合**: 與現有的報告生成系統完美整合
- 📱 **跨平台同步**: 在任何裝置上存取您的學習記錄

## 設定步驟

### 步驟 1: 創建 Notion Integration

1. 前往 [Notion Developers](https://www.notion.so/my-integrations)
2. 點擊 "New integration"
3. 填寫整合資訊：
   - **Name**: `ClinicSim-AI Integration`
   - **Logo**: 可選
   - **Associated workspace**: 選擇您的工作區
4. 點擊 "Submit" 創建整合
5. 複製 "Internal Integration Token" (以 `secret_` 開頭)

### 步驟 2: 創建學習記錄 Database

1. 在 Notion 中創建新的 Database
2. 設定以下欄位：

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| **案例標題** | Title | 案例名稱 |
| **學習日期** | Date | 問診日期 |
| **案例類型** | Select | 內科/外科/急診等 |
| **問診表現** | Number | 評分 (1-10) |
| **臨床決策** | Number | 評分 (1-10) |
| **知識應用** | Number | 評分 (1-10) |
| **總體評價** | Number | 總分 (1-10) |
| **複習狀態** | Select | 待複習/已複習/已掌握 |

3. 複製 Database ID (從 URL 中獲取，32 位字符)

### 步驟 3: 設定權限

1. 在 Database 頁面右上角點擊 "Share"
2. 點擊 "Add people, emails, groups, or integrations"
3. 搜尋並選擇您創建的 "ClinicSim-AI Integration"
4. 給予 "Can edit" 權限

### 步驟 4: 設定環境變數

在您的系統中設定以下環境變數：

```bash
# 設定 Notion API Key
export NOTION_API_KEY="ntn_your_integration_token_here"

# 設定 Notion Database ID
export NOTION_DATABASE_ID="your_32_character_database_id_here"
```

#### Windows (PowerShell)
```powershell
$env:NOTION_API_KEY="ntn_your_integration_token_here"
$env:NOTION_DATABASE_ID="your_32_character_database_id_here"
```

#### 永久設定 (.env 檔案)
在專案根目錄創建 `.env` 檔案：
```env
NOTION_API_KEY=ntn_your_integration_token_here
NOTION_DATABASE_ID=your_32_character_database_id_here
```

## 使用方法

### 1. 在 Streamlit 介面中使用

1. 完成問診並生成詳細報告
2. 在報告頁面底部找到 "📝 學習記錄管理" 區塊
3. 點擊 "📤 將學習報告輸出至 Notion" 按鈕
4. 系統會自動將報告匯出到您的 Notion Database

### 2. 檢查匯出狀態

- ✅ **成功**: 顯示成功訊息和 Notion 頁面連結
- ❌ **失敗**: 顯示錯誤訊息和解決建議
- ⚠️ **未配置**: 顯示設定指南

## 匯出的內容

每次匯出會創建一個新的 Notion 頁面，包含：

### 基本資訊
- 案例標題和類型
- 學習日期
- 各項評分

### 詳細內容
- 📊 學習表現摘要
- 🎯 改進建議
- 📋 完整學習報告
- 📚 引註來源

## 故障排除

### 常見問題

1. **"Notion API 未配置"**
   - 確認已設定環境變數
   - 檢查 API Key 和 Database ID 是否正確

2. **"Notion 連線失敗"**
   - 檢查網路連線
   - 確認 API Key 有效
   - 確認 Database ID 正確且有權限

3. **"報告檔案不存在"**
   - 確認已生成詳細報告
   - 檢查 report_history 目錄

### 測試整合

執行測試腳本驗證設定：

```bash
python test_notion_integration.py
```

## 安全注意事項

- 🔒 **保護您的 API Key**: 不要將 API Key 提交到版本控制系統
- 🔐 **限制權限**: 只給予整合必要的最小權限
- 📝 **定期更新**: 定期更新您的 API Key

## 進階功能

### 自定義 Database 結構

您可以根據需要調整 Database 欄位，但請確保包含基本的評分欄位。

### 批次匯出

目前支援單個報告匯出，批次匯出功能將在未來版本中提供。

## 技術細節

- **API 版本**: Notion API v1 (2022-06-28)
- **認證方式**: Bearer Token
- **請求限制**: 每分鐘 3 個請求
- **支援格式**: Rich Text, Number, Select, Date

## 支援與回報問題

如果您遇到任何問題，請：

1. 檢查本指南的故障排除部分
2. 執行測試腳本診斷問題
3. 在 GitHub 上回報問題，並附上錯誤訊息和日誌

---

**注意**: 此功能需要有效的 Notion 帳號和網路連線。某些組織的 Notion 可能限制第三方整合的使用。
