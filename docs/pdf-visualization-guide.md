# PDF 視覺化功能使用指南

## 概述

本功能為 ClinicSim-AI 專案新增了強大的 PDF 視覺化能力，能夠：

1. **精確來源追蹤**：在 RAG 搜尋時記錄每個知識片段的原始檔案和頁碼
2. **視覺化附錄**：自動從原始 PDF 中截取相關段落並高亮顯示
3. **提升可信度**：讓評審能夠直接看到 AI 引用的原始文件內容

## 功能特色

### 1. 強化引註系統
- 每個引註現在包含：
  - 原始檔案名稱
  - 精確頁碼
  - 相關性分數
  - 完整的來源路徑

### 2. PDF 截圖生成
- 自動從原始 PDF 中截取指定頁面
- 高亮顯示相關文字段落
- 快取機制避免重複處理
- 高解析度輸出 (200 DPI)

### 3. 前端視覺化展示
- 在報告附錄中顯示 PDF 截圖
- 清晰的來源資訊標示
- 檔案大小和處理狀態顯示

## 技術實現

### 核心組件

1. **Citation 模型升級** (`src/models/report.py`)
   ```python
   class Citation(BaseModel):
       id: int
       query: str
       source: str
       content: str
       page_number: Optional[int] = None  # 新增頁碼欄位
       metadata: Optional[Dict[str, Any]] = None
   ```

2. **PDF 視覺化工具** (`src/utils/pdf_visualizer.py`)
   - `create_source_snippet()`: 根據引註產生 PDF 截圖
   - `create_page_snippet()`: 產生指定頁面截圖
   - `get_page_text()`: 獲取頁面文字內容
   - `find_text_in_page()`: 搜尋頁面中的文字

3. **RAG 服務升級** (`src/services/rag_service.py`)
   - `search_with_citations()`: 回傳帶有完整來源資訊的引註
   - 自動提取頁碼和檔案資訊
   - 美化檔名顯示

4. **前端顯示組件** (`src/frontend/components/report_display.py`)
   - `_render_citation_with_visualization()`: 渲染帶有 PDF 截圖的引註
   - 自動產生和顯示 PDF 截圖
   - 錯誤處理和狀態顯示

### 工作流程

1. **索引建立階段** (`build_index.py`)
   - PyMuPDFLoader 自動提取頁碼資訊
   - 確保每個文檔片段都有正確的來源標記

2. **RAG 搜尋階段**
   - 使用 `search_with_citations()` 方法
   - 自動提取最相關的結果和來源資訊
   - 建立完整的引註物件

3. **報告生成階段**
   - 在報告中嵌入引註資訊
   - 準備視覺化所需的資料

4. **前端展示階段**
   - 根據引註資訊產生 PDF 截圖
   - 在附錄中展示視覺化結果

## 使用方法

### 1. 重新建立索引

由於新增了頁碼資訊，需要重新建立 FAISS 索引：

```bash
python build_index.py
```

### 2. 啟動應用程式

正常啟動應用程式，新功能會自動啟用：

```bash
python main.py
```

### 3. 查看視覺化效果

1. 完成一次問診對話
2. 生成詳細報告
3. 滾動到報告底部的「附錄：引註來源視覺化」部分
4. 點擊展開每個引註，查看 PDF 截圖

## 配置選項

### 快取設定

PDF 截圖會快取在 `static/snippets/` 目錄中，可以透過以下方式管理：

```python
from src.utils.pdf_visualizer import pdf_visualizer

# 清理 7 天前的快取檔案
pdf_visualizer.cleanup_cache(max_age_days=7)
```

### 圖片品質設定

在 `src/utils/pdf_visualizer.py` 中調整 DPI 設定：

```python
# 將整頁渲染成一張圖片
pix = page.get_pixmap(dpi=200)  # 可調整為 150, 300 等
```

## 故障排除

### 常見問題

1. **PDF 截圖無法產生**
   - 檢查原始 PDF 檔案是否存在
   - 確認頁碼是否正確
   - 查看控制台錯誤訊息

2. **快取目錄權限問題**
   - 確保 `static/snippets/` 目錄可寫入
   - 檢查檔案系統權限

3. **記憶體使用過高**
   - 調整 DPI 設定降低圖片解析度
   - 定期清理快取檔案

### 除錯模式

啟用詳細日誌輸出：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 效能優化

### 快取策略
- 使用 MD5 雜湊避免重複處理
- 自動清理過期快取檔案
- 並行處理多個引註

### 記憶體管理
- 及時關閉 PDF 文件
- 限制同時處理的檔案數量
- 使用適當的圖片壓縮

## 未來擴展

### 可能的改進
1. **多頁面截圖**：支援跨頁面的內容截圖
2. **文字搜尋高亮**：更精確的文字定位和高亮
3. **批次處理**：一次處理多個引註
4. **雲端儲存**：將截圖上傳到雲端服務

### API 擴展
- 提供 REST API 端點
- 支援外部系統整合
- 增加更多視覺化選項

## 總結

PDF 視覺化功能大幅提升了 ClinicSim-AI 專案的可信度和專業性。透過精確的來源追蹤和視覺化展示，評審能夠直接驗證 AI 系統的知識來源，這將是專案的一大亮點。

這個功能不僅技術上可行，而且實現相對簡單，主要依賴於現有的 PyMuPDF 函式庫和 Streamlit 的圖片顯示能力。建議在評審前充分測試，確保所有 PDF 檔案都能正常處理。
