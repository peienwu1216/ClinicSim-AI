# ClinicSim-AI - AI-powered Clinical Skills Training Platform

一個專為醫學生設計的 AI 驅動臨床技能訓練平台，提供 OSCE MOCK EXAM 模擬考試體驗。

## 🚀 快速開始

### 1. 啟動後端服務
```bash
python main.py
```

### 2. 啟動前端應用
```bash
streamlit run app.py
```

### ⚡ AMD NPU 加速 (推薦)
如果您有支援 AMD Ryzen AI 的硬體，可以使用 NPU 加速版本：

```bash
# 使用 NPU 加速啟動
python start_npu.py

# 或使用批次檔 (Windows)
start_npu.bat
```

詳細設定請參考 [NPU_SETUP.md](NPU_SETUP.md)

## ✨ 主要功能

### 🏥 OSCE MOCK EXAM 模擬
- **AI病人對話**：與模擬病人進行真實的 OSCE 考試情境對話
- **即時回饋**：AI提供專業的臨床技能評估和指導
- **覆蓋率追蹤**：即時顯示 OSCE 考試項目覆蓋率進度

### 📋 臨床決策面板
- **床邊檢查**：ECG心電圖（含視覺化）、POCUS超音波
- **實驗室檢驗**：心肌酵素、全血球計數
- **影像學檢查**：胸部X光（含視覺化）
- **藥物處方**：氧氣、阿斯匹靈、硝化甘油、嗎啡

### 📊 OSCE 智能評估系統
- **即時評估報告**：OSCE 考試結束後立即生成技能評估
- **詳細分析報告**：包含RAG臨床指引的深度分析與改進建議
- **引註來源**：提供臨床指引的詳細引用與學習資源

### 💓 生命體徵監控
- **即時監控**：心率、血壓、血氧、呼吸頻率
- **動態更新**：根據問診進度自動更新

## 🎨 界面特色

- **專業設計**：醫療級UI設計，提供專業的學習環境
- **響應式佈局**：左側聊天，右側臨床Orders，底部監控面板
- **視覺化學習**：ECG、X光等檢查結果的圖片顯示
- **緊湊設計**：節省空間，提高操作效率

## 🛠️ 技術架構

### 前端
- **Streamlit**：現代化的Python Web應用框架
- **自定義CSS**：專業的醫療級界面設計
- **組件化架構**：模組化的組件設計

### 後端
- **FastAPI**：高性能的API服務
- **AI集成**：集成大型語言模型
- **RAG系統**：檢索增強生成，提供臨床指引

## 📁 項目結構

```
ClinicSim-AI/
├── app.py                 # 統一前端入口
├── main.py               # 後端服務入口
├── src/                  # 源代碼目錄
│   ├── frontend/         # 前端組件
│   ├── services/         # 業務邏輯
│   └── models/          # 數據模型
├── static/              # 靜態資源
│   └── samples/         # 樣本圖片
├── cases/               # 病例數據
└── requirements.txt     # 依賴包
```

## 🔧 開發設置

### 安裝依賴
```bash
pip install -r requirements.txt
```

### 環境變量
創建 `.env` 文件並配置：
```
OPENAI_API_KEY=your_api_key
HOST=127.0.0.1
PORT=5001
```

## 📖 使用指南

1. **開始問診**：在聊天框中輸入問題開始與AI病人對話
2. **開立醫囑**：使用右側臨床決策面板開立檢查和藥物
3. **查看結果**：ECG、X光等檢查會自動顯示相應圖片
4. **結束問診**：點擊「總結與計畫」按鈕結束問診
5. **查看報告**：獲得即時評估和詳細分析報告

## 🎯 OSCE 學習目標

- **問診技巧**：掌握標準的 OSCE 問診流程與技巧
- **臨床思維**：培養系統性的臨床診斷思維與決策能力
- **決策能力**：練習臨床檢查和治療決策的 OSCE 考試情境
- **專業素養**：提升醫學專業素養、溝通技巧與考試表現

## 🤝 貢獻

歡迎提交Issue和Pull Request來改進這個項目！

## 📄 許可證

MIT License

---

**🧑‍⚕️ ClinicSim AI - AI-powered Clinical Skills Training Platform for Medical Students OSCE MOCK EXAM**