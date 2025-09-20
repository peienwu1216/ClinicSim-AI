# Notion 整合設定指南

## 概述

ClinicSim-AI 現在支援將生成的報告自動同步到 Notion，讓您可以集中管理所有的診後分析報告。

## 功能特色

- 🚀 **自動同步**：報告生成後自動同步到 Notion
- 📝 **Markdown 轉換**：將 Markdown 格式的報告轉換為 Notion blocks
- 🏗️ **模組化設計**：獨立的 Notion 服務，易於維護
- ⚙️ **配置管理**：支援環境變數配置
- 🔄 **手動同步**：支援手動同步現有報告

## 設定步驟

### 1. 安裝依賴

```bash
pip install notion-client
```

### 2. 設定環境變數

在 `.env` 檔案中添加以下設定：

```env
# Notion 整合設定
NOTION_ENABLED=true
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_database_id_here
NOTION_PARENT_PAGE_ID=your_parent_page_id_here
```

### 3. 取得 Notion API Key

1. 前往 [Notion Developers](https://www.notion.so/my-integrations)
2. 點擊 "New integration"
3. 填寫整合名稱和選擇工作區
4. 複製 "Internal Integration Token" 作為 `NOTION_API_KEY`

### 4. 設定 Notion 資料庫或頁面

#### 選項 A：使用資料庫
1. 在 Notion 中創建一個資料庫
2. 確保資料庫有 "title" 屬性
3. 將整合添加到資料庫（在資料庫頁面右上角點擊 "..." → "Add connections"）
4. 複製資料庫 ID 作為 `NOTION_DATABASE_ID`

#### 選項 B：使用父頁面
1. 在 Notion 中創建一個頁面作為父頁面
2. 將整合添加到頁面（在頁面右上角點擊 "..." → "Add connections"）
3. 複製頁面 ID 作為 `NOTION_PARENT_PAGE_ID`

### 5. 取得頁面/資料庫 ID

Notion 的頁面 ID 格式為：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

可以從 Notion 頁面 URL 中取得：
- URL: `https://www.notion.so/workspace/Page-Title-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- ID: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

## 使用方法

### 自動同步

當 `NOTION_ENABLED=true` 時，每次生成報告都會自動同步到 Notion：

```python
# 生成報告時會自動同步
report = report_service.generate_detailed_report(conversation)
```

### 手動同步現有報告

```python
# 同步現有報告檔案
page_id = report_service.sync_existing_report_to_notion(
    file_path="report_history/case_chest_pain_acs_01_detailed_20250920_133300.md",
    page_title="自定義標題"
)
```

### API 端點

```bash
# 同步報告到 Notion
curl -X POST http://localhost:5001/sync_report_to_notion \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "report_history/case_chest_pain_acs_01_detailed_20250920_133300.md",
    "page_title": "自定義標題"
  }'
```

## 支援的 Markdown 格式

- **標題**：`# 一級標題`, `## 二級標題`, `### 三級標題`
- **無序列表**：`- 項目` 或 `* 項目`
- **有序列表**：`1. 項目`, `2. 項目`
- **段落文字**：一般文字內容
- **程式碼區塊**：``` 包圍的內容

## 故障排除

### 常見問題

1. **"Notion 客戶端未初始化"**
   - 檢查 `NOTION_API_KEY` 是否正確設定
   - 確認 API Key 有效且有適當權限

2. **"找不到頁面"**
   - 檢查 `NOTION_DATABASE_ID` 或 `NOTION_PARENT_PAGE_ID` 是否正確
   - 確認整合已添加到對應的資料庫或頁面

3. **"權限不足"**
   - 確認整合有創建頁面的權限
   - 檢查整合是否已正確添加到工作區

### 除錯模式

設定 `DEBUG=true` 可以啟用詳細的除錯資訊：

```env
DEBUG=true
NOTION_ENABLED=true
```

## 架構說明

```
src/services/notion_service.py     # Notion 整合服務
src/api/routes.py                  # API 端點
src/config/settings.py             # 配置管理
src/services/report_service.py     # 報告服務整合
```

## 開發者注意事項

- Notion API 有速率限制，請避免頻繁調用
- 每次最多可添加 100 個 blocks
- 建議在生產環境中啟用錯誤處理和重試機制
