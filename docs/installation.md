# 📦 安裝指南

本指南將協助您在不同環境中安裝和配置 ClinicSim-AI。

## 🎯 安裝選項

### 選項一：基本安裝 (推薦)
適用於大多數用戶，包含所有核心功能。

```bash
pip install -r requirements.txt
```

### 選項二：開發環境安裝
適用於開發者，包含測試工具和開發依賴。

```bash
pip install -r requirements-dev.txt
```

## 📋 依賴文件說明

| 文件 | 用途 | 包含內容 |
|------|------|----------|
| `requirements.txt` | 主要依賴 | 核心功能、AI服務、RAG系統 |
| `requirements-dev.txt` | 開發依賴 | 測試框架、代碼檢查工具、Jupyter |
| `requirements-base.txt` | 基礎依賴 | Web框架、數據處理、基礎工具 |

## 🔧 環境配置

### 1. 創建虛擬環境 (推薦)

```bash
# 創建虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

### 2. 配置環境變數

創建 `.env` 文件：

```bash
# AI 模型配置
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3:8b
OPENAI_API_KEY=your_openai_api_key_here

# 應用程式配置
HOST=127.0.0.1
PORT=5001
DEBUG=false

# RAG 配置
RAG_MODEL_NAME=nomic-ai/nomic-embed-text-v1.5
RAG_CHUNK_SIZE=800
RAG_CHUNK_OVERLAP=100
RAG_SEARCH_K=3
```

## 🍋 Lemonade Server 配置

如果您使用 Lemonade Server，請參考 [Lemonade Server 配置指南](lemonade-setup.md)。

### 環境變數配置

```bash
# Lemonade Server 配置
LEMONADE_HOST=http://127.0.0.1:11434
LEMONADE_MODEL=llama3:8b
LEMONADE_GPU_LAYERS=35
LEMONADE_CONTEXT_LENGTH=4096
```

## 🖥️ 平台特定安裝

### Windows

```bash
# 基本安裝
pip install -r requirements.txt

# 如果遇到 FAISS 問題，開發環境包含替代方案
pip install -r requirements-dev.txt
```

### macOS

```bash
# 基本安裝
pip install -r requirements.txt

# 如果需要 M1/M2 優化
pip install --upgrade torch torchvision torchaudio
```

### Linux

```bash
# 基本安裝
pip install -r requirements.txt

# 系統依賴 (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-dev python3-pip
```

## 🐳 Docker 安裝

### 使用 Docker Compose

```bash
# 克隆專案
git clone https://github.com/your-username/ClinicSim-AI.git
cd ClinicSim-AI

# 啟動服務
docker-compose up -d
```

### 手動 Docker 構建

```bash
# 構建映像
docker build -t clinic-sim-ai .

# 運行容器
docker run -p 8501:8501 -p 5001:5001 clinic-sim-ai
```

## 🔍 驗證安裝

### 1. 檢查依賴

```bash
# 檢查主要依賴
python -c "import streamlit, flask, langchain; print('✅ 主要依賴安裝成功')"

# 檢查 AI 服務
python -c "import ollama, openai; print('✅ AI 服務依賴安裝成功')"

# 檢查 RAG 系統
python -c "import faiss, sentence_transformers; print('✅ RAG 系統依賴安裝成功')"
```

### 2. 運行測試

```bash
# 運行基本測試
python -m pytest tests/ -v

# 運行特定測試
python tests/test_multilingual_rag.py
```

### 3. 啟動應用

```bash
# 啟動後端服務
python main.py

# 啟動前端 (新終端)
streamlit run app.py
```

## 🚨 常見問題

### 問題 1: FAISS 安裝失敗

**解決方案：**
```bash
# Windows 用戶使用開發依賴
pip install -r requirements-dev.txt

# 或使用替代方案
pip install chromadb
```

### 問題 2: PyTorch 安裝問題

**解決方案：**
```bash
# 訪問 PyTorch 官網獲取正確命令
# https://pytorch.org/get-started/locally/

# 例如：CPU 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 問題 3: 依賴衝突

**解決方案：**
```bash
# 創建新的虛擬環境
python -m venv venv_new
source venv_new/bin/activate  # 或 Windows: venv_new\Scripts\activate

# 重新安裝
pip install -r requirements.txt
```

### 問題 4: 記憶體不足

**解決方案：**
```bash
# 使用較小的模型
export OLLAMA_MODEL=llama3:8b
export RAG_CHUNK_SIZE=400
export RAG_SEARCH_K=2
```

## 📊 系統需求

### 最低需求
- Python 3.8+
- 4GB RAM
- 2GB 磁碟空間

### 推薦需求
- Python 3.10+
- 8GB RAM
- 10GB 磁碟空間
- GPU (可選，用於加速)

## 🔄 更新依賴

```bash
# 更新所有依賴到最新版本
pip install --upgrade -r requirements.txt

# 檢查過時的依賴
pip list --outdated

# 更新特定依賴
pip install --upgrade package_name
```

## 📞 獲取幫助

如果遇到安裝問題，請：

1. 檢查 [故障排除指南](troubleshooting.md)
2. 查看 [GitHub Issues](https://github.com/your-username/ClinicSim-AI/issues)
3. 聯絡技術支援：peienwu.ee13@nycu.edu.tw

---

🎉 安裝完成後，請查看 [快速開始指南](quick-start.md) 開始使用 ClinicSim-AI！