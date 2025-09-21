# 🔧 Notion 匯出問題修復方案

## 🎯 問題診斷

**原始錯誤**: `❌ 匯出請求失敗: HTTP 5000`

**根本原因**: 
1. Notion 服務嘗試解析空的報告檔案路徑
2. 前端錯誤處理不夠完善
3. 缺少對直接文字匯出的支援

## ✅ 修復內容

### 1. 修復 Notion 服務 (`src/services/notion_service.py`)

#### 新增功能：
- **`_parse_report_from_data()`**: 從 case_data 直接解析報告內容
- **`_parse_report_content()`**: 通用的報告內容解析方法
- **改進 `create_learning_record()`**: 支援檔案和直接文字兩種模式

#### 修復邏輯：
```python
def create_learning_record(self, report_path: str, case_data: Dict[str, Any]) -> Tuple[bool, str]:
    try:
        # 解析報告內容
        if report_path and report_path.strip():
            # 從檔案解析
            parsed_report = self._parse_report_file(report_path)
        else:
            # 從 case_data 直接解析
            parsed_report = self._parse_report_from_data(case_data)
        
        # 轉換為 Notion 格式
        notion_data = self._format_for_notion(parsed_report, case_data)
        # ... 其餘邏輯
```

### 2. 改善前端錯誤處理 (`src/frontend/components/report_display.py`)

#### 新增錯誤處理：
- **連接錯誤**: 無法連接到後端服務
- **超時錯誤**: 請求超時處理
- **500 錯誤**: 伺服器內部錯誤，包含 Notion 配置檢查提示
- **詳細調試信息**: 顯示報告檔案和案例 ID

#### 錯誤處理邏輯：
```python
try:
    response = requests.post(...)
    # 處理各種狀態碼
except requests.exceptions.ConnectionError:
    st.error("❌ 無法連接到後端服務")
    st.info("💡 請確保後端服務正在運行 (python main.py)")
except requests.exceptions.Timeout:
    st.error("❌ 請求超時，請稍後再試")
except Exception as e:
    st.error(f"❌ 匯出時發生錯誤: {str(e)}")
```

## 🧪 測試結果

### 測試命令：
```bash
python -c "import requests; response = requests.post('http://127.0.0.1:5001/notion/export_report', json={'report_text': 'Test report content', 'case_id': 'test_case', 'report_title': 'Test Report'}, timeout=30); print(f'Status: {response.status_code}'); print(f'Response: {response.text}')"
```

### 測試結果：
```
Status: 200
Response: {"message":"報告已成功匯出到 Notion","success":true}
```

## 🚀 使用方式

### 1. 確保後端運行
```bash
python main.py
```

### 2. 啟動前端
```bash
# 使用修復版前端
streamlit run src/frontend/app_fixed.py --server.port 8502

# 或使用原始前端
streamlit run src/frontend/app.py --server.port 8501
```

### 3. 測試 Notion 匯出
1. 完成問診對話
2. 生成學習報告
3. 點擊 "匯出到 Notion" 按鈕
4. 查看匯出結果

## 🔍 故障排除

### 如果仍然出現錯誤：

1. **檢查 Notion 配置**：
   - 確保已設定 `NOTION_API_KEY`
   - 確保已設定 `NOTION_DATABASE_ID`
   - 檢查 Notion 權限設定

2. **檢查後端服務**：
   ```bash
   curl http://127.0.0.1:5001/health
   ```

3. **檢查前端連接**：
   - 確認前端連接到正確的後端端口 (5001)
   - 檢查防火牆設定

4. **查看詳細錯誤**：
   - 前端會顯示詳細的調試信息
   - 後端日誌會記錄具體錯誤

## 📋 技術細節

### 修復的檔案：
- `src/services/notion_service.py` - 核心 Notion 服務修復
- `src/frontend/components/report_display.py` - 前端錯誤處理改善

### 新增方法：
- `_parse_report_from_data()` - 直接文字解析
- `_parse_report_content()` - 通用內容解析

### 改善功能：
- 支援直接文字匯出（不需要檔案）
- 更好的錯誤處理和用戶反饋
- 詳細的調試信息顯示

## ✅ 修復完成

Notion 匯出功能現已完全修復，支援：
- ✅ 直接文字匯出
- ✅ 檔案匯出
- ✅ 完善的錯誤處理
- ✅ 用戶友好的錯誤提示
- ✅ 詳細的調試信息

現在可以正常使用 Notion 匯出功能了！
