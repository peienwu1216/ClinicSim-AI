# 🏥 ClinicSim-AI 臨床技能教練系統

> **AI 驅動的醫學教育平台** | 讓醫學生通過 AI 模擬病人練習臨床技能

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.49+-red.svg)](https://streamlit.io)
[![Flask](https://img.shields.io/badge/Flask-3.1+-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 專案簡介

ClinicSim-AI 是一個專為醫學生設計的 AI 臨床技能教練系統，提供：

- 🤖 **AI 模擬病人** - 基於真實案例的智能病人互動
- 📊 **即時評估** - 問診過程中的覆蓋率統計和反饋
- 📚 **RAG 增強報告** - 基於臨床指引的詳細分析報告
- 📝 **引註來源** - 透明的知識來源顯示
- 🎨 **直觀界面** - 現代化的 Web 界面設計

## 🚀 快速開始

### 第一次使用？

**5 分鐘快速體驗：**

```bash
# 1. 克隆專案
git clone https://github.com/your-username/ClinicSim-AI.git
cd ClinicSim-AI

# 2. 自動安裝環境
python install.py

# 3. 啟動系統
python main.py  # 後端
streamlit run app_new.py  # 前端（新終端）
```

**訪問系統：**
- 🌐 前端界面：http://localhost:8501
- 🔧 後端 API：http://localhost:5001

### 系統要求

- **Python**: 3.8 或更高版本
- **記憶體**: 8GB+ RAM（用於 AI 模型）
- **網路**: 用於下載 AI 模型（首次使用）

## 📚 文檔導航

### 👥 使用者指南
- **[快速開始指南](docs/quick-start.md)** - 5 分鐘快速體驗
- **[安裝指南](docs/installation.md)** - 詳細安裝步驟
- **[使用者手冊](docs/user-manual.md)** - 完整功能說明

### 👨‍💻 開發者指南
- **[開發者指南](docs/developer-guide.md)** - 開發環境設置和代碼結構
- **[API 文檔](docs/api-documentation.md)** - 完整的 API 參考
- **[部署指南](docs/deployment.md)** - 生產環境部署

### 🔧 技術文檔
- **[專案架構](docs/architecture.md)** - 系統架構和設計模式
- **[RAG 系統](docs/rag-system.md)** - RAG 技術實現
- **[故障排除](docs/troubleshooting.md)** - 常見問題解決

## 🎮 使用場景

### 🏥 醫學教育
- **OSCE 練習** - 標準化病人考試準備
- **問診技巧** - 病史採集和溝通技巧
- **臨床推理** - 診斷思維訓練

### 📊 評估分析
- **即時反饋** - 問診過程中的即時評估
- **詳細報告** - 基於臨床指引的深度分析
- **進步追蹤** - 學習進度和技能發展

## 🏗️ 系統架構

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Flask API     │    │   RAG System    │
│   前端界面       │◄──►│   後端服務       │◄──►│   知識檢索       │
│                │    │                │    │                │
│ • 聊天界面       │    │ • AI 服務       │    │ • 向量搜尋       │
│ • 報告顯示       │    │ • 案例管理       │    │ • 引註生成       │
│ • 覆蓋率統計     │    │ • 報告生成       │    │ • 臨床指引       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🌟 核心功能

### 1. AI 模擬病人
- 基於真實案例的智能病人角色扮演
- 自然語言對話和情感表達
- 動態生命體徵變化

### 2. 即時評估系統
- 問診覆蓋率實時計算
- 關鍵問題識別
- 進度可視化顯示

### 3. RAG 增強報告
- 基於臨床指引的專業分析
- 引註來源透明顯示
- 個性化學習建議

### 4. 兩階段報告
- **即時報告** - 問診結束後立即生成
- **詳細報告** - 深度分析和改進建議

## 🔧 技術特色

- **模組化架構** - 清晰的代碼結構和依賴管理
- **多環境支援** - 支援開發、測試、生產環境
- **跨平台兼容** - 支援 macOS、Windows、Linux
- **AI 模型整合** - 支援 Ollama、Lemonade 等 AI 服務
- **RAG 技術** - 檢索增強生成，提供準確的臨床知識

## 🤝 貢獻指南

我們歡迎各種形式的貢獻！

### 如何貢獻
1. **Fork** 本專案
2. **創建** 功能分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 分支 (`git push origin feature/AmazingFeature`)
5. **開啟** Pull Request

### 貢獻類型
- 🐛 Bug 修復
- ✨ 新功能開發
- 📚 文檔改進
- 🎨 UI/UX 優化
- 🧪 測試用例

## 📞 支援與聯絡

### 獲取幫助
- 📖 查看 [完整文檔](docs/README.md)
- 🐛 回報 [Issues](https://github.com/your-username/ClinicSim-AI/issues)
- 💬 參與 [討論](https://github.com/your-username/ClinicSim-AI/discussions)

### 社群
- 🌟 給我們一個 Star
- 👀 Watch 專案更新
- 🍴 Fork 並貢獻代碼

## 📄 授權

本專案採用 MIT 授權 - 查看 [LICENSE](LICENSE) 檔案了解詳情。

## 🙏 致謝

感謝所有貢獻者和開源社群的支持！

---

<div align="center">

**⭐ 如果這個專案對您有幫助，請給我們一個 Star！**

[快速開始](docs/quick-start.md) • [安裝指南](docs/installation.md) • [使用者手冊](docs/user-manual.md) • [完整文檔](docs/README.md)

</div>