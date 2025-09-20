# ClinicSim-AI 臨床技能教練系統

## 🎯 專案概述

ClinicSim-AI 是一個專為醫學生設計的 AI 臨床技能教練系統，提供模擬病人問診、即時評估和詳細分析報告功能。系統整合了 RAG (Retrieval-Augmented Generation) 技術，能夠基於臨床指引提供專業的學習建議。

### 核心功能
- 🤖 **AI 模擬病人**：基於案例的智能病人互動
- 📊 **即時評估**：問診過程中的覆蓋率統計
- 📚 **RAG 增強報告**：基於臨床指引的詳細分析
- 📝 **引註來源**：透明的知識來源顯示
- 🎨 **兩階段報告**：即時評估 + 詳細分析

## 🏗️ 系統架構

```
ClinicSim-AI/
├── app.py                    # Streamlit 前端界面
├── server.py                 # Flask 後端 API
├── rag_handler.py            # RAG 系統處理器
├── build_index.py            # RAG 索引建立腳本
├── documents/                # 臨床指引文件存放處
│   └── acute_chest_pain_guidelines.txt
├── cases/                    # 案例配置文件
│   └── case_chest_pain_acs_01.json
├── faiss_index/              # RAG 向量索引 (不進版本控制)
├── venv/                     # Python 虛擬環境
├── requirements.txt          # Python 依賴清單
└── README.md                # 本文件
```

## 🚀 快速開始

### 環境要求
- Python 3.8+
- 8GB+ RAM (用於 RAG 索引建立)
- 網路連線 (用於模型下載)

## 💻 本地開發環境設置

### 1. 克隆專案
```bash
git clone <repository-url>
cd ClinicSim-AI
```

### 2. 建立虛擬環境
```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 安裝依賴
```bash
pip install -r requirements.txt
```

### 4. 建立 RAG 索引
```bash
# 確保 documents/ 資料夾中有臨床指引文件
python build_index.py
```

### 5. 設定環境變數
建立 `.env` 檔案：
```env
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3:8b
```

### 6. 啟動 Ollama (如果使用本地模型)
```bash
# 安裝 Ollama
# 下載並安裝：https://ollama.ai/

# 下載模型
ollama pull llama3:8b

# 啟動 Ollama 服務
ollama serve
```

### 7. 啟動系統
```bash
# 終端 1：啟動後端
python server.py

# 終端 2：啟動前端
streamlit run app.py
```

### 8. 訪問系統
- 前端界面：http://localhost:8501
- 後端 API：http://localhost:5001

## 🖥️ Lemonade AMD AI PC 部署

### 1. 準備工作
在本地開發環境中完成以下步驟：

#### 建立 RAG 索引
```bash
# 在本地 Mac/Windows 環境中
python build_index.py
```

#### 打包索引檔案
```bash
# 將 faiss_index 資料夾打包
tar -czf faiss_index.tar.gz faiss_index/
# 或使用 zip
zip -r faiss_index.zip faiss_index/
```

### 2. 部署到 AMD AI PC

#### 上傳檔案
將以下檔案上傳到 AMD AI PC：
- 整個專案資料夾
- `faiss_index.tar.gz` 或 `faiss_index.zip`

#### 解壓縮索引
```bash
# 在 AMD AI PC 上
cd ClinicSim-AI
tar -xzf faiss_index.tar.gz
# 或
unzip faiss_index.zip
```

#### 安裝依賴
```bash
# 建立虛擬環境
python -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

### 3. Lemonade 環境設定

#### 環境變數設定
在 AMD AI PC 上建立 `.env` 檔案：
```env
# Lemonade 環境會自動設定這些變數
# 不需要手動設定 OLLAMA_HOST 和 OLLAMA_MODEL
```

#### 啟動系統
```bash
# 在 Lemonade 環境中
python server.py
```

### 4. 驗證部署
- 檢查 RAG 索引是否正常載入
- 測試 AI 病人回應功能
- 驗證詳細報告生成功能

## 🔧 開發指南

### 添加新的案例
1. 在 `cases/` 資料夾中建立新的 JSON 檔案
2. 參考 `case_chest_pain_acs_01.json` 的格式
3. 更新 `app.py` 中的 `CASE_ID` 變數

### 添加新的臨床指引
1. 將 PDF/TXT 檔案放入 `documents/` 資料夾
2. 重新執行 `python build_index.py`
3. 重啟系統

### 修改 RAG 查詢
編輯 `server.py` 中的 `rag_queries` 列表：
```python
rag_queries = [
    "你的查詢 1",
    "你的查詢 2",
    # ...
]
```

## 📚 功能說明

### 兩階段報告系統
1. **即時評估報告**：問診結束後立即生成
2. **詳細分析報告**：點擊按鈕後使用 LLM + RAG 生成

### RAG 系統
- **索引建立**：一次性建立向量索引
- **智能搜尋**：基於語義相似度的知識檢索
- **引註顯示**：透明的知識來源標示

### 引註功能
- **自動標記**：報告中的 `[引註 X]` 標記
- **視覺高亮**：藍色背景高亮顯示
- **詳細內容**：可展開查看完整指引

## 🐛 故障排除

### 常見問題

#### 1. RAG 索引載入失敗
```bash
# 重新建立索引
rm -rf faiss_index/
python build_index.py
```

#### 2. Ollama 連接失敗
```bash
# 檢查 Ollama 是否運行
ollama list
ollama serve
```

#### 3. 依賴安裝失敗
```bash
# 更新 pip
pip install --upgrade pip
# 重新安裝依賴
pip install -r requirements.txt --force-reinstall
```

#### 4. 記憶體不足
- 減少 `documents/` 中的文件數量
- 調整 `chunk_size` 參數
- 使用更小的 embedding 模型

### 日誌檢查
```bash
# 查看後端日誌
python server.py

# 查看前端日誌
streamlit run app.py --logger.level debug
```

## 🔒 安全注意事項

### 環境變數
- 不要將 `.env` 檔案提交到版本控制
- 敏感資訊使用環境變數管理

### 檔案權限
- `faiss_index/` 資料夾不應被版本控制
- 確保適當的檔案權限設定

## 📈 效能優化

### RAG 系統優化
- 調整 `chunk_size` 和 `chunk_overlap` 參數
- 使用更快的 embedding 模型
- 定期更新索引

### 系統監控
- 監控記憶體使用量
- 檢查 API 回應時間
- 追蹤錯誤率

## 🤝 團隊協作

### 開發流程
1. **功能開發**：在本地環境開發和測試
2. **索引建立**：在本地建立 RAG 索引
3. **索引傳遞**：將索引檔案傳給整合工程師
4. **部署測試**：在 AMD AI PC 上測試部署

### 版本控制
```bash
# 提交代碼變更
git add .
git commit -m "功能描述"
git push

# 不要提交以下檔案
# - faiss_index/
# - .env
# - __pycache__/
```

### 代碼規範
- 使用繁體中文註解
- 遵循 PEP 8 代碼風格
- 添加適當的錯誤處理

## 📞 支援與聯絡

### 技術支援
- 查看本 README 的故障排除部分
- 檢查專案中的其他文檔
- 聯繫專案維護者

### 功能建議
- 提交 Issue 描述需求
- 提供詳細的使用場景
- 包含預期的行為描述

## 📄 授權資訊

本專案使用 MIT 授權，詳見 LICENSE 檔案。

---

**最後更新**：2024年9月
**版本**：v1.0.0
**維護者**：ClinicSim-AI 開發團隊
