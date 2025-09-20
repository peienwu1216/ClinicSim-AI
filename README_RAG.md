# ClinicSim-AI RAG 系統使用指南

## 概述

本專案已整合 RAG (Retrieval-Augmented Generation) 功能，能夠在生成診後分析報告時提供基於臨床指引的專業建議。

## 架構設計

### 核心組件

1. **`build_index.py`** - 索引建立器
   - 一次性腳本，用於建立向量索引
   - 讀取 `documents/` 資料夾中的文件
   - 生成 `faiss_index/` 向量資料庫

2. **`rag_handler.py`** - RAG 處理器
   - 獨立的 RAG 系統模組
   - 提供搜尋功能
   - 在 `server.py` 啟動時自動載入

3. **`server.py`** - 後端伺服器
   - 整合 RAG 功能到報告生成流程
   - 支援雙平台 (Mac 開發 + AI PC Demo)

## 使用流程

### 步驟一：準備知識文件

1. 將臨床指引、OSCE 評分標準等文件放入 `documents/` 資料夾
2. 支援格式：PDF、TXT、MD

### 步驟二：建立向量索引

```bash
# 啟用虛擬環境
source venv/bin/activate  # Mac/Linux
# 或
venv\Scripts\activate     # Windows

# 安裝 RAG 相關依賴
pip install -r requirements.txt

# 建立索引
python build_index.py
```

### 步驟三：啟動系統

```bash
# 啟動後端
python server.py

# 啟動前端 (另一個終端)
streamlit run app.py
```

## 技術細節

### 使用的模型

- **Embedding 模型**: `nomic-ai/nomic-embed-text-v1.5`
  - 中英雙語支援
  - 開源且跨平台相容
  - 在 Mac 和 AI PC 上都能正常運作

### 索引建立過程

1. 文件載入：支援 PDF (PyMuPDF) 和文字檔
2. 文件切塊：800 字元/塊，100 字元重疊
3. 向量化：使用 HuggingFace Embeddings
4. 索引儲存：FAISS 向量資料庫

### RAG 搜尋流程

1. 接收查詢 (例如："為什麼 ECG 是急性胸痛的第一優先檢查？")
2. 向量相似度搜尋
3. 返回最相關的 3 個知識片段
4. 格式化為上下文注入到 LLM Prompt 中

## 跨平台相容性

### Mac 開發環境
- 使用 Ollama 本地模型
- 建立 `faiss_index/` 資料夾
- 將索引打包給 AI PC 使用

### AI PC Demo 環境
- 使用 Lemonade 服務
- 載入預先建立的 `faiss_index/`
- 無需重新建立索引

## 檔案結構

```
ClinicSim-AI/
├── documents/              # 知識文件存放處
│   └── acute_chest_pain_guidelines.txt
├── faiss_index/           # 向量索引 (不進版本控制)
├── build_index.py         # 索引建立腳本
├── rag_handler.py         # RAG 處理模組
├── server.py              # 後端伺服器 (已整合 RAG)
├── app.py                 # 前端界面
└── requirements.txt       # 依賴清單
```

## 注意事項

1. **索引建立**：只在開發環境中執行一次
2. **版本控制**：`faiss_index/` 資料夾不應被 Git 追蹤
3. **依賴安裝**：確保安裝所有 RAG 相關套件
4. **記憶體使用**：建立索引時可能需要較多記憶體

## 故障排除

### 常見問題

1. **找不到索引檔案**
   - 確認已執行 `python build_index.py`
   - 檢查 `faiss_index/` 資料夾是否存在

2. **模型下載失敗**
   - 確保網路連線正常
   - 可能需要較長時間下載模型

3. **記憶體不足**
   - 減少文件大小或數量
   - 調整 `chunk_size` 參數

### 日誌訊息

- `💡 [RAG] 正在載入 RAG 向量索引...` - 正常載入
- `✅ [RAG] RAG 索引載入成功。` - 載入完成
- `⚠️ 警告：找不到索引檔案` - 需要建立索引
- `❌ [RAG] RAG 索引載入失敗` - 載入錯誤

## 擴展功能

### 添加更多文件

1. 將新文件放入 `documents/` 資料夾
2. 重新執行 `python build_index.py`
3. 重啟伺服器

### 調整搜尋參數

在 `rag_handler.py` 中修改：
- `k=3`：返回的相關文件數量
- `chunk_size=800`：文件切塊大小
- `chunk_overlap=100`：重疊字元數

### 自定義查詢

在 `server.py` 的 `get_feedback_report` 函式中修改：
```python
student_weakness_query = "你的自定義查詢"
```
