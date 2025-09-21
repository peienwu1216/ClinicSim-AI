# Notion UI 整合設計方案

## 概述

本專案已實現完整的 Notion UI 串接功能，讓用戶在報告生成後能夠無縫地管理學習記錄，包括匯出到 Notion、查看歷史記錄、學習統計分析等功能。

## 功能特色

### 🎯 核心功能
1. **智能報告匯出** - 自動提取評分數據並匯出到 Notion
2. **學習歷史管理** - 查看和管理所有學習記錄
3. **學習統計分析** - 提供詳細的學習進度分析
4. **批量操作** - 支持批量匯出和歷史記錄管理
5. **設定指南** - 內建 Notion 設定指導

### 🎨 用戶體驗
- **直觀的儀表板** - 清晰的數據展示和操作界面
- **智能狀態檢測** - 自動檢測 Notion 配置和連線狀態
- **響應式設計** - 適配不同螢幕尺寸
- **即時反饋** - 操作結果即時顯示

## 技術架構

### 前端組件
```
src/frontend/components/
├── notion_integration.py    # Notion 整合 UI 組件
├── report_display.py        # 報告顯示組件（已整合）
└── base.py                  # 基礎組件類
```

### 後端服務
```
src/services/
├── notion_service.py        # Notion API 服務
└── report_service.py        # 報告生成服務

src/api/routes.py            # API 路由端點
```

### API 端點
- `GET /notion/test_connection` - 測試 Notion 連線
- `POST /notion/export_report` - 匯出報告到 Notion
- `GET /notion/get_learning_history` - 獲取學習歷史
- `POST /notion/batch_export` - 批量匯出

## 使用流程

### 1. 報告生成後自動顯示
當用戶完成問診並生成報告後，系統會自動顯示 Notion 整合面板：

```python
# 在報告顯示組件中
def render(self, session_ended=False, report_data=None, ...):
    if session_ended:
        self._render_notion_integration(report_data)
```

### 2. 智能數據提取
系統會自動從報告中提取評分數據：

```python
def _prepare_report_data(self):
    return {
        'case_id': case_id,
        'case_type': '胸痛',
        'total_score': 85.5,
        'coverage': 78.0,
        'interview_score': 82.0,
        'decision_score': 88.0,
        'knowledge_score': 86.0,
        'report_content': detailed_report,
        'generated_at': datetime.now().isoformat()
    }
```

### 3. 多種匯出選項
用戶可以選擇不同的匯出方式：

- **匯出到 Notion** - 將完整報告匯出到 Notion 學習記錄
- **下載報告** - 下載為 Markdown 檔案
- **批量匯出** - 一次性匯出多個歷史記錄

## UI 組件設計

### NotionIntegrationComponent

#### 主要方法
- `render_notion_dashboard()` - 渲染主儀表板
- `_render_setup_guide()` - 顯示設定指南
- `_render_main_functions()` - 顯示主要功能
- `_render_history_section()` - 顯示歷史記錄
- `_render_learning_statistics()` - 顯示學習統計

#### 狀態管理
```python
# 檢查 Notion 狀態
notion_status = self._check_notion_status()

# 顯示相應的 UI
if not notion_status['configured']:
    self._render_setup_guide()
elif not notion_status['connected']:
    self._render_connection_error()
else:
    self._render_main_functions()
```

### 報告顯示組件整合

#### 數據準備
```python
def _prepare_report_data(self):
    # 從 session state 獲取數據
    case_id = st.session_state.get('case_id')
    feedback_report = st.session_state.get('feedback_report')
    detailed_report = st.session_state.get('detailed_report')
    
    # 提取評分信息
    total_score = self._extract_score_from_report(report_text, "總體評分")
    # ... 其他評分提取
    
    return report_data
```

#### 評分提取
```python
def _extract_score_from_report(self, report_text: str, score_type: str) -> float:
    patterns = {
        "總體評分": r"總體評分[：:]\s*(\d+(?:\.\d+)?)%",
        "問診覆蓋率": r"問診覆蓋率[：:]\s*(\d+(?:\.\d+)?)%",
        # ... 其他模式
    }
    # 使用正則表達式提取評分
```

## 設定指南

### 1. 創建 Notion Integration
1. 前往 [Notion Developers](https://www.notion.so/my-integrations)
2. 點擊 "New integration"
3. 填寫名稱和選擇工作區
4. 複製 "Internal Integration Token"

### 2. 創建學習記錄 Database
在 Notion 中創建 Database，包含以下欄位：

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| 案例標題 | Title | 學習案例的名稱 |
| 學習日期 | Date | 學習日期 |
| 案例類型 | Select | 胸痛、腹痛等 |
| 問診表現 | Number | 問診技巧評分 (0-100) |
| 臨床決策 | Number | 臨床決策評分 (0-100) |
| 知識應用 | Number | 知識應用評分 (0-100) |
| 總體評價 | Number | 總體評分 (0-100) |
| 複習狀態 | Select | 未複習、已複習、需加強 |
| 學習筆記 | Text | 個人學習筆記 |
| 報告內容 | Text | 完整報告內容 |

### 3. 設定環境變數
```bash
# Windows (PowerShell)
$env:NOTION_API_KEY="your_integration_token"
$env:NOTION_DATABASE_ID="your_database_id"

# Linux/Mac
export NOTION_API_KEY="your_integration_token"
export NOTION_DATABASE_ID="your_database_id"
```

## 學習統計功能

### 統計指標
- **總學習次數** - 累計學習次數
- **平均總體評分** - 所有學習的平均評分
- **平均問診表現** - 問診技巧平均評分
- **平均臨床決策** - 臨床決策平均評分

### 進度圖表
使用 Plotly 創建學習進度趨勢圖：

```python
import plotly.express as px

fig = px.line(df_chart, 
             x="學習次數", 
             y=["總體評分", "問診表現", "臨床決策"],
             title="學習進度趨勢")
```

## 錯誤處理

### 連線錯誤
```python
def _check_notion_status(self):
    try:
        response = requests.get(f"{self.api_base_url}/notion/test_connection")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return {'configured': False, 'connected': False, 'message': str(e)}
```

### 匯出錯誤
```python
def _handle_export_to_notion(self, report_data):
    try:
        with st.spinner("正在匯出到 Notion..."):
            response = requests.post(f"{self.api_base_url}/notion/export_report", ...)
            if response.status_code == 200:
                st.success("✅ 匯出成功")
            else:
                st.error(f"❌ 匯出失敗: {response.status_code}")
    except Exception as e:
        st.error(f"❌ 匯出時發生錯誤: {str(e)}")
```

## 測試驗證

### 運行測試
```bash
python test_notion_ui.py
```

### 測試內容
1. **Notion 服務測試** - 測試 API 連線和數據操作
2. **UI 組件測試** - 測試組件初始化和狀態檢查
3. **API 端點測試** - 測試所有相關 API 端點

### 預期結果
- ✅ Notion 服務: 測試通過
- ✅ Notion UI 組件: 測試通過  
- ✅ API 端點: 測試通過

## 未來改進

### 短期目標
1. **離線模式** - 支持離線查看歷史記錄
2. **數據同步** - 自動同步 Notion 數據變更
3. **自定義欄位** - 支持用戶自定義 Database 欄位

### 長期目標
1. **多平台支援** - 支持其他筆記應用整合
2. **AI 分析** - 基於學習數據的 AI 建議
3. **協作功能** - 支持多用戶協作學習

## 總結

Notion UI 整合功能提供了完整的學習記錄管理解決方案：

✅ **無縫整合** - 報告生成後自動顯示管理面板  
✅ **智能提取** - 自動提取評分和報告數據  
✅ **多種匯出** - 支持單個和批量匯出  
✅ **歷史管理** - 完整的學習歷史記錄管理  
✅ **統計分析** - 詳細的學習進度分析  
✅ **用戶友好** - 直觀的界面和操作流程  

這個整合方案不僅提升了用戶體驗，更為學習記錄管理提供了專業級的解決方案。
