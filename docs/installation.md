# 📦 安裝指南

> **詳細的安裝步驟** | 支援多平台和多環境部署

## 🖥️ 支援的環境

| 環境 | 狀態 | 推薦配置 |
|------|------|----------|
| **macOS** | ✅ 完全支援 | `requirements-dev.txt` |
| **Windows** | ✅ 完全支援 | `requirements-windows.txt` |
| **Linux** | ✅ 完全支援 | `requirements-dev.txt` |
| **Lemonade Server** | ✅ 比賽環境 | `requirements-lemonade.txt` |

## 🚀 快速安裝

### 自動安裝（推薦）

```bash
# 克隆專案
git clone https://github.com/your-username/ClinicSim-AI.git
cd ClinicSim-AI

# 自動檢測環境並安裝
python install.py
```

## 📋 手動安裝步驟

### 1. 環境準備

#### 檢查 Python 版本
```bash
python --version
# 應該顯示 Python 3.8 或更高版本
```

#### 更新 pip
```bash
python -m pip install --upgrade pip
```

### 2. 建立虛擬環境

```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. 安裝依賴

#### macOS/Linux 開發環境
```bash
pip install -r requirements-dev.txt
```

#### Windows 開發環境
```bash
pip install -r requirements-windows.txt
```

#### 生產環境
```bash
pip install -r requirements-production.txt
```

#### Lemonade 比賽環境
```bash
pip install -r requirements-lemonade.txt
```

### 4. 建立 RAG 索引

```bash
# 確保 documents/ 資料夾中有臨床指引文件
python build_index.py
```

### 5. 環境配置

創建 `.env` 檔案：

```env
# AI 服務配置
AI_PROVIDER=ollama
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3:8b

# 伺服器配置
HOST=0.0.0.0
PORT=5001
DEBUG=false

# RAG 配置
RAG_INDEX_PATH=faiss_index
EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5

# 案例配置
CASES_PATH=cases
```

## 🔧 環境特定配置

### macOS 安裝

```bash
# 使用 Homebrew 安裝 Python（可選）
brew install python

# 安裝依賴
pip install -r requirements-dev.txt

# 如果遇到權限問題
pip install --user -r requirements-dev.txt
```

### Windows 安裝

```bash
# 安裝 Windows 特殊依賴
pip install -r requirements-windows.txt

# 如果 FAISS 安裝失敗，使用替代方案
pip install chromadb
```

#### Windows 常見問題

**問題 1: FAISS 安裝失敗**
```bash
# 解決方案：使用 ChromaDB
pip install chromadb
# 然後修改代碼使用 ChromaDB 而不是 FAISS
```

**問題 2: 編譯錯誤**
```bash
# 安裝 Visual Studio Build Tools
# 或使用預編譯的 wheel
pip install --only-binary=all faiss-cpu
```

### Linux 安裝

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev python3-pip

# CentOS/RHEL
sudo yum install python3-devel python3-pip

# 安裝依賴
pip install -r requirements-dev.txt
```

## 🤖 AI 模型配置

### 使用 Ollama（本地模型）

```bash
# 1. 安裝 Ollama
# 訪問 https://ollama.ai/ 下載安裝

# 2. 下載模型
ollama pull llama3:8b

# 3. 啟動 Ollama 服務
ollama serve

# 4. 驗證安裝
ollama list
```

### 使用 Lemonade AI

```env
# 在 .env 中設定
AI_PROVIDER=lemonade
# Lemonade 環境會自動配置其他參數
```

## 🧪 驗證安裝

### 1. 檢查依賴
```bash
python -c "import flask, streamlit, langchain; print('✅ 核心依賴安裝成功')"
```

### 2. 測試 RAG 系統
```bash
python -c "from rag_handler import rag_system; print('✅ RAG 系統載入成功')"
```

### 3. 啟動測試
```bash
# 啟動後端
python main.py

# 在新終端啟動前端
streamlit run app_new.py
```

### 4. 訪問系統
- 前端：http://localhost:8501
- 後端：http://localhost:5001/health

## 🐛 故障排除

### 常見問題

#### 1. Python 版本不符
```bash
# 錯誤：Python 版本過低
# 解決：升級到 Python 3.8+
pyenv install 3.11.0  # 使用 pyenv
```

#### 2. 依賴安裝失敗
```bash
# 清理並重新安裝
pip cache purge
pip install --force-reinstall -r requirements-dev.txt
```

#### 3. RAG 索引建立失敗
```bash
# 檢查 documents/ 資料夾
ls documents/
# 應該包含 acute_chest_pain_guidelines.txt

# 重新建立索引
rm -rf faiss_index/
python build_index.py
```

#### 4. 記憶體不足
```bash
# 減少 chunk_size
# 編輯 build_index.py 中的參數
chunk_size = 500  # 預設 1000
```

#### 5. 端口被佔用
```bash
# 查看端口使用情況
lsof -i:5001  # macOS/Linux
netstat -ano | findstr :5001  # Windows

# 修改 .env 中的 PORT
PORT=5002
```

### 日誌檢查

```bash
# 後端日誌
python main.py --log-level debug

# 前端日誌
streamlit run app_new.py --logger.level debug
```

## 📊 系統監控

### 檢查系統狀態
```bash
# 記憶體使用
free -h  # Linux
vm_stat  # macOS

# 磁碟空間
df -h

# 網路連接
netstat -an | grep :5001
```

### 效能優化

#### 1. 減少記憶體使用
```python
# 在 .env 中調整
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

#### 2. 啟用快取
```python
# 在 settings.py 中
ENABLE_CACHE=true
CACHE_TTL=3600
```

## 🔒 安全配置

### 環境變數安全
```bash
# 不要將 .env 提交到版本控制
echo ".env" >> .gitignore

# 使用系統環境變數
export OLLAMA_HOST="http://127.0.0.1:11434"
```

### 檔案權限
```bash
# 設定適當的檔案權限
chmod 600 .env
chmod -R 755 faiss_index/
```

## 🚀 生產環境部署

### Docker 部署
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements-production.txt .
RUN pip install -r requirements-production.txt

COPY . .
EXPOSE 5001

CMD ["python", "main.py"]
```

### 使用 Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 main:app
```

## 📞 獲取幫助

如果遇到問題：

1. **查看日誌** - 檢查錯誤訊息
2. **檢查版本** - 確認 Python 和依賴版本
3. **重啟服務** - 重新啟動 Ollama 和應用程式
4. **查看文檔** - 參考其他文檔
5. **回報問題** - 創建 Issue 並提供詳細資訊

---

**安裝完成後，請查看 [快速開始指南](quick-start.md) 開始使用！** 🎉
