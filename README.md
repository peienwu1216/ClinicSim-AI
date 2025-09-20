# 🧑‍⚕️ ClinicSim-AI

> 一個為醫學生設計的 AI 臨床技能教練，結合 RAG 技術提供智能化的臨床問診訓練

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 專案簡介

ClinicSim-AI 是一個創新的醫療教育平台，專為醫學生設計。透過 AI 技術模擬真實的臨床問診情境，結合 RAG (Retrieval-Augmented Generation) 技術，提供基於臨床指引的智能回饋，幫助學生提升臨床診斷能力。

### ✨ 主要特色

- 🎯 **智能問診模擬**：AI 病人提供真實的臨床互動體驗
- 📚 **RAG 技術整合**：基於臨床指引提供專業回饋
- 📊 **即時評估系統**：動態追蹤問診覆蓋率和學習進度
- 🏥 **標準化流程**：遵循急性胸痛診斷標準流程
- 💊 **臨床決策支援**：整合診斷工具和處置建議
- 📱 **響應式設計**：支援多種裝置使用

## 🚀 快速開始

### 環境需求

- Python 3.8+
- **🍋 Lemonade Server** (推薦 - 高效能 AI 推理服務)
- Ollama (本地 AI 模型 - 備選方案)
- 或 OpenAI API Key (雲端方案)

### 安裝步驟

1. **克隆專案**
```bash
git clone https://github.com/your-username/ClinicSim-AI.git
cd ClinicSim-AI
```

2. **安裝依賴**
```bash
# 使用 Lemonade 依賴 (推薦)
pip install -r requirements-lemonade.txt

# 或使用標準依賴
pip install -r requirements.txt
```

3. **配置環境變數**
```bash
# 複製環境變數範本
cp .env.example .env

# 編輯 .env 文件 - Lemonade Server 配置
# LEMONADE_HOST=http://127.0.0.1:11434
# LEMONADE_MODEL=llama3:8b
# OLLAMA_HOST=http://127.0.0.1:11434  # 備選方案
# OLLAMA_MODEL=llama3:8b
```

4. **啟動服務**
```bash
# 啟動 Lemonade Server (推薦)
# 請參考 Lemonade Server 官方文檔進行安裝和配置

# 啟動後端服務
python main.py

# 啟動前端介面
streamlit run app.py
```

5. **訪問應用**
- 前端界面：http://localhost:8501
- 後端 API：http://127.0.0.1:5001

## 📁 專案結構

```
ClinicSim-AI/
├── 📁 src/                    # 核心源碼
│   ├── 📁 api/                # API 路由和依賴
│   ├── 📁 config/             # 配置管理
│   ├── 📁 frontend/           # 前端組件
│   ├── 📁 models/             # 數據模型
│   ├── 📁 services/           # 業務邏輯服務
│   └── 📁 utils/              # 工具函數
├── 📁 docs/                   # 文檔
│   ├── 📁 development/        # 開發文檔
│   └── 📁 reports/            # 開發報告
├── 📁 scripts/                # 腳本和工具
├── 📁 cases/                  # 病例數據
├── 📁 documents/              # 臨床文檔
├── 📁 static/                 # 靜態資源
├── 📁 reports/                # 報告歷史
├── 📄 app.py                  # 主應用程式
├── 📄 main.py                 # 後端服務入口
└── 📄 requirements.txt        # 依賴清單
```

## 🎯 核心功能

### 1. 智能問診系統
- 模擬真實病人互動
- 支援多種問診技巧
- 即時語音轉文字

### 2. 臨床決策支援
- 急性胸痛診斷流程
- 標準化檢查建議
- 緊急處置指引

### 3. 學習評估系統
- 問診覆蓋率追蹤
- 生命體徵監測
- 智能回饋報告

### 4. RAG 知識庫
- 臨床指引檢索
- 證據基礎建議
- 多語言支援

## 🛠️ 技術架構

- **前端**：Streamlit + HTML/CSS/JavaScript
- **後端**：Flask + FastAPI
- **🍋 AI 推理**：**Lemonade Server** (推薦) / Ollama (本地) / OpenAI API
- **RAG 技術**：FAISS + LangChain
- **數據庫**：JSON 文件存儲
- **部署**：Docker + Cloud Platforms

### 🍋 Lemonade Server 優勢

- ⚡ **高效能推理**：專為生產環境優化的 AI 推理服務
- 🚀 **快速響應**：低延遲的模型推理速度
- 🔧 **易於部署**：簡化的安裝和配置流程
- 📈 **可擴展性**：支援負載平衡和集群部署
- 💰 **成本效益**：相比雲端 API 更經濟實惠

## 📚 文檔

- [安裝指南](docs/installation.md)
- [快速開始](docs/quick-start.md)
- [🍋 Lemonade Server 配置指南](docs/lemonade-setup.md)
- [開發者指南](docs/developer-guide.md)
- [API 文檔](docs/api-documentation.md)
- [架構說明](docs/architecture.md)
- [故障排除](docs/troubleshooting.md)

## 🤝 貢獻指南

我們歡迎社區貢獻！請查看 [開發者指南](docs/developer-guide.md) 了解如何參與開發。

1. Fork 本專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 授權條款

本專案採用 MIT 授權條款 - 查看 [LICENSE](LICENSE) 文件了解詳情。

## 🙏 致謝

- 感謝醫師提供的專業指導
- 感謝開源社區的技術支援
- 感謝醫學系學長姊的建議

## 📞 聯絡我們

- 專案維護者：吳沛恩
- 電子郵件：peienwu.ee13@nycu.edu.tw

---

⭐ 如果這個專案對您有幫助，請給我們一個 Star！