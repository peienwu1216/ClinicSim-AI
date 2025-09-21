# Toggle 按鈕解決方案

## 問題描述

在 Streamlit 應用中，`st.expander` 組件的 toggle 按鈕在某些環境下會顯示為文字（如 "keyboard_double_arrow"）而不是圖標，這嚴重影響了用戶體驗。

## 解決方案

我們創建了一個自定義的 Toggle 組件，提供多種美觀的替代方案來替代 `st.expander`。

### 新增文件

1. **`src/frontend/components/custom_toggle.py`** - 自定義 Toggle 組件
2. **`toggle_examples.py`** - 使用示例和展示
3. **`TOGGLE_SOLUTION.md`** - 本說明文件

### 已更新的文件

1. **`src/frontend/components/clinical_orders_simplified.py`** - 更新次要檢查項目的 toggle
2. **`src/frontend/components/report_display.py`** - 更新 RAG 查詢和 Notion 設定的 toggle
3. **`src/frontend/components/progress_display.py`** - 更新系統狀態和日誌的 toggle

## 使用方法

### 基本用法

```python
from .custom_toggle import create_custom_expander

def render_content():
    st.markdown("這是 toggle 的內容")

create_custom_expander(
    title="標題",
    content_func=render_content,
    key="unique_key",
    style="emoji",
    emoji="📁",
    default_expanded=False
)
```

### 可用的樣式

1. **Emoji 樣式** (`style="emoji"`)
   - 使用 Emoji 圖標（如 📁/📂）
   - 適合：檔案管理、資料夾結構

2. **Unicode 箭頭樣式** (`style="unicode"`)
   - 使用 Unicode 箭頭（▶/▼）
   - 適合：導航、選單

3. **箭頭符號樣式** (`style="arrows"`)
   - 使用箭頭符號（🔸/🔽）
   - 適合：設定選項、進階功能

4. **加減號樣式** (`style="plus_minus"`)
   - 使用加減號（➕/➖）
   - 適合：項目列表、計數器

5. **自定義圖標對樣式** (`style="icons"`)
   - 使用自定義圖標對
   - 適合：特殊功能（如 👁️/🙈 用於隱私設定）

6. **文字樣式** (`style="text"`)
   - 使用文字標示（[展開]/[收合]）
   - 適合：簡單介面、無圖標需求

## 參數說明

- `title`: 按鈕標題文字
- `content_func`: 內容渲染函數
- `key`: 唯一的 session state key
- `style`: 樣式類型
- `default_expanded`: 預設是否展開
- `emoji`: Emoji 樣式使用的圖標（僅 emoji 樣式）
- `icon_pair`: 自定義圖標對（僅 icons 樣式）
- `expand_text`: 展開文字（僅 text 樣式）
- `collapse_text`: 收合文字（僅 text 樣式）

## 優勢

✅ **解決圖標文字問題** - 完全避免 Streamlit expander 的圖標顯示問題  
✅ **多種美觀樣式** - 提供 6 種不同的視覺風格  
✅ **完全自定義** - 可以自定義圖標、顏色、動畫效果  
✅ **保持原有功能** - 完全兼容原有的展開/收合功能  
✅ **易於使用** - 簡單的 API，一行代碼即可替換  
✅ **性能優化** - 使用 CSS 動畫，流暢的用戶體驗  

## 實際應用

### 醫療檢查項目
```python
create_custom_expander(
    title="其他檢查與治療",
    content_func=render_secondary_content,
    key="secondary_orders_toggle",
    style="arrows",
    default_expanded=False
)
```

### 報告摘要
```python
create_custom_expander(
    title="RAG 查詢摘要",
    content_func=render_rag_content,
    key="rag_queries_toggle",
    style="emoji",
    emoji="🔍",
    default_expanded=False
)
```

### 系統設定
```python
create_custom_expander(
    title="如何設定 Notion 整合",
    content_func=render_notion_setup,
    key="notion_setup_toggle",
    style="emoji",
    emoji="🔧",
    default_expanded=False
)
```

## 測試

運行示例文件來查看所有樣式效果：

```bash
streamlit run toggle_examples.py
```

## 遷移指南

### 從 st.expander 遷移

**原本的寫法：**
```python
with st.expander("標題", expanded=False):
    st.markdown("內容")
    st.button("按鈕")
```

**新的寫法：**
```python
def render_content():
    st.markdown("內容")
    st.button("按鈕")

create_custom_expander(
    title="標題",
    content_func=render_content,
    key="unique_key",
    style="emoji",
    emoji="📁",
    default_expanded=False
)
```

### 注意事項

1. **Key 唯一性**: 確保每個 toggle 使用唯一的 key
2. **函數定義**: 內容必須包裝在函數中
3. **樣式選擇**: 根據使用場景選擇合適的樣式
4. **預設狀態**: 根據用戶體驗需求設定 default_expanded

## 未來擴展

這個解決方案可以進一步擴展：

- 添加更多動畫效果
- 支援自定義 CSS 類別
- 添加鍵盤快捷鍵支援
- 支援多級嵌套 toggle
- 添加主題切換功能

## 最新更新

### 透明化修復方案

為了徹底解決所有可能的 `keyboard_arrow_down` 文字問題，我們新增了：

1. **`transparent_toggle_fix.py`** - 透明化修復組件
   - 使用 CSS 讓所有圖標文字變透明（`opacity: 0`, `color: transparent`）
   - JavaScript 動態處理新出現的文字，讓它們變透明
   - 持續監控 DOM 變化，定期檢查
   - 保留 expander 的正常功能，只讓文字變透明

2. **`test_transparent_fix.py`** - 透明化測試頁面
   - 驗證透明化修復效果
   - 測試各種 expander 使用情況
   - 確認文字變透明但功能正常

### 全域修復方案（備用）

1. **`global_toggle_fix.py`** - 全域修復組件
   - 強力的 CSS 規則隱藏所有圖標文字
   - JavaScript 動態移除新出現的圖標文字
   - 持續監控 DOM 變化

2. **`test_toggle_fix.py`** - 測試頁面
   - 驗證修復效果
   - 測試各種 expander 使用情況

### 使用方法

在主應用中自動應用透明化修復：

```python
from src.frontend.components.transparent_toggle_fix import apply_transparent_toggle_fix_once

def main():
    # 應用透明化修復
    apply_transparent_toggle_fix_once()
    # ... 其他代碼
```

### 測試修復效果

運行透明化測試頁面：

```bash
streamlit run test_transparent_fix.py
```

或運行原始測試頁面：

```bash
streamlit run test_toggle_fix.py
```

## 總結

通過這個完整的解決方案（自定義 Toggle 組件 + 透明化修復），我們：

1. ✅ **完全解決**了 Streamlit expander 的圖標文字問題
2. ✅ **提供多種美觀**的 toggle 樣式選擇
3. ✅ **保持原有功能**不變
4. ✅ **透明化修復**讓文字變透明，用戶看不到
5. ✅ **動態處理**新出現的內容
6. ✅ **易於使用和維護**
7. ✅ **包含測試工具**驗證效果

### 透明化修復的優勢：
- **簡單有效**: 讓文字變透明，不需要複雜的隱藏邏輯
- **功能完整**: 不影響 expander 的正常展開/收合功能
- **動態處理**: 自動處理新出現的內容
- **多重保障**: CSS + JavaScript + 定期檢查
- **用戶友好**: 用戶完全看不到問題文字

所有原本使用 `st.expander` 的地方都已經更新為使用新的自定義組件，同時透明化修復確保即使有遺漏的 expander 也不會顯示圖標文字。
