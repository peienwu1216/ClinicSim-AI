# 專案結構說明

## 📁 目錄結構

```
ClinicSim-AI/
├── 📁 src/                    # 核心源碼目錄
│   ├── 📁 api/                # API 相關
│   │   ├── __init__.py
│   │   ├── dependencies.py    # API 依賴注入
│   │   └── routes.py          # API 路由定義
│   ├── 📁 config/             # 配置管理
│   │   ├── __init__.py
│   │   ├── settings.py        # 系統配置
│   │   └── scoring_sys.json   # 評分系統配置
│   ├── 📁 frontend/           # 前端組件
│   │   ├── __init__.py
│   │   ├── app.py             # 前端主應用
│   │   └── 📁 components/     # UI 組件
│   ├── 📁 models/             # 數據模型
│   │   ├── __init__.py
│   │   ├── case.py            # 病例模型
│   │   ├── conversation.py    # 對話模型
│   │   ├── report.py          # 報告模型
│   │   └── vital_signs.py     # 生命體徵模型
│   ├── 📁 services/           # 業務邏輯服務
│   │   ├── __init__.py
│   │   ├── ai_service.py      # AI 服務
│   │   ├── case_service.py    # 病例服務
│   │   ├── conversation_service.py  # 對話服務
│   │   ├── notion_service.py  # Notion 整合
│   │   ├── rag_service.py     # RAG 服務
│   │   └── report_service.py  # 報告服務
│   └── 📁 utils/              # 工具函數
├── 📁 docs/                   # 文檔目錄
│   ├── 📁 development/        # 開發文檔
│   │   └── project-structure.md
│   ├── 📁 reports/            # 開發報告
│   │   ├── JSON_序列化修復總結.md
│   │   ├── PDF_視覺化功能實現總結.md
│   │   ├── RAG_效能優化建議.md
│   │   ├── RAG_測試報告.md
│   │   ├── RAG多語言改進總結.md
│   │   ├── UI_佈局改進總結.md
│   │   ├── UI_改進實現總結.md
│   │   ├── UI_改進總結.md
│   │   ├── 佈局改進總結.md
│   │   └── 隨機病例選擇功能說明.md
│   ├── api-documentation.md   # API 文檔
│   ├── api_contract.md        # API 合約
│   ├── architecture.md        # 架構說明
│   ├── deployment.md          # 部署指南
│   ├── developer-guide.md     # 開發者指南
│   ├── installation.md        # 安裝指南
│   ├── notion-integration-setup.md  # Notion 整合設定
│   ├── pdf-visualization-guide.md   # PDF 視覺化指南
│   ├── quick-start.md         # 快速開始
│   ├── rag-system.md          # RAG 系統說明
│   ├── README.md              # 文檔說明
│   ├── troubleshooting.md     # 故障排除
│   └── user-manual.md         # 使用者手冊
├── 📁 scripts/                # 腳本和工具
│   ├── build_index.py         # 建構索引
│   ├── clinical_orders_simple.py  # 簡化臨床指令
│   ├── generate_sample_images.py  # 生成範例圖片
│   ├── get-pip.py             # pip 安裝腳本
│   ├── improve_rag_multilingual.py  # RAG 多語言改進
│   ├── install.py             # 安裝腳本
│   ├── rag_handler.py         # RAG 處理器
│   ├── rag_handler_simple.py  # 簡化 RAG 處理器
│   ├── server.py              # 伺服器
│   ├── simple_server.py       # 簡化伺服器
│   ├── start.sh               # 啟動腳本
│   ├── start_new.sh           # 新啟動腳本
│   ├── test_multilingual_rag.py  # 多語言 RAG 測試
│   └── test.py                # 測試腳本
├── 📁 cases/                  # 病例數據
│   ├── case_1.json
│   ├── case_2.json
│   ├── case_3.json
│   ├── case_4.json
│   ├── case_5.json
│   ├── case_6.json
│   ├── case_7.json
│   ├── case_8.json
│   ├── case_9.json
│   └── case_chest_pain_acs_01.json
├── 📁 documents/              # 臨床文檔
│   ├── 📁 CaseStudy/          # 案例研究
│   ├── 📁 Guideline/          # 臨床指引
│   ├── 📁 Research/           # 研究文獻
│   └── 📁 Review/             # 文獻回顧
├── 📁 static/                 # 靜態資源
│   ├── 📁 samples/            # 範例圖片
│   └── 📁 snippets/           # 程式碼片段
├── 📁 reports/                # 報告歷史
│   └── 📁 report_history/     # 歷史報告
├── 📄 app.py                  # 主應用程式 (Streamlit)
├── 📄 main.py                 # 後端服務入口
├── 📄 requirements.txt        # 主要依賴
├── 📄 requirements-base.txt   # 基礎依賴
├── 📄 requirements-dev.txt    # 開發依賴
├── 📄 requirements-lemonade.txt  # Lemonade 依賴
├── 📄 requirements-production.txt  # 生產依賴
├── 📄 requirements-windows.txt  # Windows 依賴
├── 📄 README.md               # 專案說明
├── 📄 LICENSE                 # 授權條款
└── 📄 .gitignore              # Git 忽略文件
```

## 🔧 主要文件說明

### 核心應用文件
- `app.py`: Streamlit 前端主應用程式
- `main.py`: Flask 後端服務入口點

### 配置文件
- `requirements*.txt`: 各種環境的依賴清單
- `.env`: 環境變數配置 (需要自行創建)
- `.gitignore`: Git 版本控制忽略規則

### 數據目錄
- `cases/`: 儲存病例 JSON 數據
- `documents/`: 臨床文檔和指引
- `faiss_index/`: RAG 系統的向量索引
- `static/`: 靜態資源文件

### 文檔目錄
- `docs/`: 所有專案文檔
- `docs/development/`: 開發相關文檔
- `docs/reports/`: 開發過程報告

### 腳本目錄
- `scripts/`: 各種輔助腳本和工具

## 🚀 開發建議

1. **新增功能**: 在 `src/` 目錄下對應的子目錄中開發
2. **文檔更新**: 將文檔放在 `docs/` 目錄中
3. **腳本工具**: 將輔助腳本放在 `scripts/` 目錄中
4. **測試文件**: 使用 `test_` 前綴命名測試文件
5. **配置管理**: 使用 `src/config/settings.py` 統一管理配置

## 📝 命名規範

- **目錄**: 使用小寫字母和連字符 (kebab-case)
- **Python 文件**: 使用小寫字母和下劃線 (snake_case)
- **JSON 文件**: 使用小寫字母和下劃線 (snake_case)
- **Markdown 文件**: 使用小寫字母和連字符 (kebab-case)
- **類別名稱**: 使用大寫字母開頭 (PascalCase)
- **函數和變數**: 使用小寫字母和下劃線 (snake_case)
