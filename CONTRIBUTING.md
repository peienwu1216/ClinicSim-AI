# 🤝 貢獻指南

感謝您對 ClinicSim-AI 專案的關注！我們歡迎各種形式的貢獻。

## 📋 貢獻類型

### 🐛 錯誤報告
- 使用 GitHub Issues 報告問題
- 提供詳細的重現步驟
- 包含錯誤訊息和環境資訊

### ✨ 功能建議
- 提出新功能想法
- 討論改進建議
- 參與功能設計討論

### 💻 程式碼貢獻
- 修復錯誤
- 實現新功能
- 改善程式碼品質
- 優化效能

### 📚 文檔改進
- 改善現有文檔
- 添加使用範例
- 翻譯文檔

## 🚀 開始貢獻

### 1. Fork 專案
```bash
git clone https://github.com/your-username/ClinicSim-AI.git
cd ClinicSim-AI
```

### 2. 設置開發環境
```bash
# 安裝依賴
pip install -r requirements-dev.txt

# 設置環境變數
cp .env.example .env
```

### 3. 創建功能分支
```bash
git checkout -b feature/your-feature-name
```

### 4. 進行開發
- 遵循現有的程式碼風格
- 添加適當的註解
- 撰寫測試用例

### 5. 提交變更
```bash
git add .
git commit -m "Add: 簡潔描述您的變更"
git push origin feature/your-feature-name
```

### 6. 開啟 Pull Request
- 提供清晰的描述
- 連結相關的 Issues
- 請求程式碼審查

## 📝 程式碼規範

### Python 程式碼風格
- 使用 PEP 8 風格指南
- 函數和類別名稱使用 snake_case
- 常數使用 UPPER_CASE
- 添加適當的 docstring

### 提交訊息規範
```
類型: 簡潔描述

詳細描述（可選）

關聯 Issue: #123
```

類型包括：
- `Add:` 新增功能
- `Fix:` 修復錯誤
- `Update:` 更新現有功能
- `Remove:` 移除功能
- `Docs:` 文檔變更
- `Style:` 程式碼風格調整
- `Refactor:` 重構程式碼
- `Test:` 測試相關

## 🧪 測試

### 運行測試
```bash
# 運行所有測試
python -m pytest tests/

# 運行特定測試
python -m pytest tests/test_multilingual_rag.py
```

### 撰寫測試
- 為新功能撰寫測試
- 確保測試覆蓋率
- 使用描述性的測試名稱

## 📖 文檔

### 文檔結構
- `docs/` - 主要文檔
- `docs/development/` - 開發文檔
- `README.md` - 專案說明
- `CONTRIBUTING.md` - 貢獻指南

### 文檔撰寫規範
- 使用清晰的標題結構
- 提供程式碼範例
- 添加適當的圖表和截圖
- 保持文檔更新

## 🔍 程式碼審查

### 審查重點
- 程式碼品質和風格
- 功能正確性
- 效能考量
- 安全性檢查
- 文檔完整性

### 審查流程
1. 自動化檢查（linting, testing）
2. 人工審查
3. 討論和改進
4. 合併或要求修改

## 🏷️ 標籤系統

### Issue 標籤
- `bug` - 錯誤報告
- `enhancement` - 功能建議
- `documentation` - 文檔相關
- `good first issue` - 適合新手
- `help wanted` - 需要幫助

### Pull Request 標籤
- `ready for review` - 準備審查
- `work in progress` - 進行中
- `needs testing` - 需要測試
- `breaking change` - 重大變更

## 📞 聯絡與支援

- 💬 [GitHub Discussions](https://github.com/your-username/ClinicSim-AI/discussions)
- 🐛 [Issue Tracker](https://github.com/your-username/ClinicSim-AI/issues)
- 📧 電子郵件：peienwu.ee13@nycu.edu.tw

## 🙏 致謝

感謝所有貢獻者對專案的付出！您的貢獻讓 ClinicSim-AI 變得更好。

---

🎉 準備好開始貢獻了嗎？我們期待您的參與！
