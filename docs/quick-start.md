# 🚀 快速開始指南

> **5 分鐘快速體驗 ClinicSim-AI** | 讓您立即開始使用 AI 臨床技能教練

## 📋 系統要求

- **Python**: 3.8 或更高版本
- **記憶體**: 8GB+ RAM
- **網路**: 用於下載 AI 模型（首次使用）
- **作業系統**: macOS、Windows 或 Linux

## ⚡ 快速安裝

### 方法一：自動安裝（推薦）

```bash
# 1. 克隆專案
git clone https://github.com/your-username/ClinicSim-AI.git
cd ClinicSim-AI

# 2. 自動安裝環境
python install.py

# 3. 啟動系統
python main.py  # 後端服務
streamlit run app_new.py  # 前端界面（新終端）
```

### 方法二：手動安裝

```bash
# 1. 建立虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 2. 安裝依賴
pip install -r requirements-dev.txt

# 3. 建立 RAG 索引
python build_index.py

# 4. 啟動系統
python main.py
streamlit run app_new.py
```

## 🌐 訪問系統

啟動成功後，您可以在瀏覽器中訪問：

- **🎨 前端界面**: http://localhost:8501
- **🔧 後端 API**: http://localhost:5001
- **❤️ 健康檢查**: http://localhost:5001/health

## 🎮 第一次使用

### 1. 選擇案例
- 在左側邊欄選擇「急性胸痛案例」
- 查看案例背景資訊

### 2. 開始問診
- 在聊天界面輸入您的問題
- 例如：「你好，請問你哪裡不舒服？」
- AI 病人會根據案例設定回應

### 3. 查看評估
- 右上角顯示問診覆蓋率
- 左側顯示生命體徵變化

### 4. 生成報告
- 點擊「生成即時報告」查看基本評估
- 點擊「生成詳細報告」獲得深度分析

## 🔧 環境配置

### 創建 .env 檔案

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
```

### 安裝 Ollama（可選）

如果您想使用本地 AI 模型：

```bash
# 安裝 Ollama
# 訪問 https://ollama.ai/ 下載安裝

# 下載模型
ollama pull llama3:8b

# 啟動 Ollama 服務
ollama serve
```

## 🎯 功能預覽

### 主要功能
- **🤖 AI 病人對話** - 智慧模擬病人回應
- **📊 即時評估** - 問診覆蓋率統計
- **📚 詳細報告** - 基於臨床指引的分析
- **📝 引註來源** - 透明的知識來源
- **🎨 現代界面** - 直觀的用戶體驗

### 支援的案例
- **急性胸痛** - 急性冠心症候群案例
- **更多案例** - 持續擴充中...

## ❓ 常見問題

### Q: 啟動失敗怎麼辦？
**A**: 檢查 Python 版本和依賴安裝：
```bash
python --version  # 應該 >= 3.8
pip list | grep flask  # 檢查 Flask 是否安裝
```

### Q: RAG 功能無法使用？
**A**: 確保已建立索引：
```bash
python build_index.py
```

### Q: AI 回應很慢？
**A**: 檢查 Ollama 是否正常運行：
```bash
ollama list
ollama serve
```

### Q: 端口被佔用？
**A**: 修改 .env 中的 PORT 設定，或關閉佔用端口的程序

## 🆘 需要幫助？

1. **查看完整文檔**：
   - [安裝指南](installation.md) - 詳細安裝步驟
   - [使用者手冊](user-manual.md) - 完整功能說明
   - [故障排除](troubleshooting.md) - 問題解決

2. **獲取支援**：
   - 回報 [Issues](https://github.com/your-username/ClinicSim-AI/issues)
   - 參與 [討論](https://github.com/your-username/ClinicSim-AI/discussions)

## 🎉 下一步

恭喜！您已經成功啟動了 ClinicSim-AI。接下來可以：

- 📖 閱讀 [使用者手冊](user-manual.md) 了解更多功能
- 🛠️ 查看 [開發者指南](developer-guide.md) 開始開發
- 🚀 參考 [部署指南](deployment.md) 部署到生產環境

---

**祝您使用愉快！** 🎉
