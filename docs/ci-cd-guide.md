# 🚀 CI/CD 指南

本指南說明 ClinicSim-AI 的持續集成和持續部署 (CI/CD) 流程。

## 📋 概述

我們使用 GitHub Actions 實現完整的 CI/CD 流程，包括：

- 🔍 **代碼質量檢查**：Flake8、Black、MyPy
- 🧪 **自動化測試**：單元測試、集成測試、覆蓋率測試
- 🌐 **多平台測試**：Ubuntu、Windows、macOS
- 🔒 **安全掃描**：依賴安全檢查、代碼安全掃描
- 🐳 **容器化部署**：Docker 映像構建和推送
- 📦 **自動發布**：GitHub Releases 和分發包

## 🔧 本地測試

### 快速開始

```bash
# 1. 檢查測試環境
python scripts/test_setup.py

# 2. 運行所有測試
python scripts/run_tests.py --type all

# 3. 運行代碼檢查
python scripts/run_tests.py --type lint

# 4. 運行覆蓋率測試
python scripts/run_tests.py --type coverage
```

### 測試類型

| 命令 | 描述 |
|------|------|
| `--type unit` | 運行單元測試 |
| `--type integration` | 運行集成測試 |
| `--type all` | 運行所有測試 |
| `--type coverage` | 運行覆蓋率測試 |
| `--type lint` | 運行代碼檢查 |
| `--type quick` | 運行快速測試（跳過慢速測試） |

## 🏗️ CI/CD 流程

### 1. 持續集成 (CI)

當您推送代碼或創建 Pull Request 時，會自動觸發以下流程：

#### 🔍 代碼質量檢查
```yaml
- Flake8 代碼風格檢查
- Black 代碼格式檢查  
- MyPy 類型檢查
```

#### 🧪 自動化測試
```yaml
- 單元測試 (test_basic_functionality.py)
- 集成測試 (test_api_endpoints.py)
- 多平台測試 (Ubuntu, Windows, macOS)
- Python 版本測試 (3.9, 3.10, 3.11)
```

#### 📊 測試覆蓋率
```yaml
- 生成覆蓋率報告
- 上傳到 Codecov
- 覆蓋率門檻檢查
```

#### 🔒 安全掃描
```yaml
- Safety 依賴安全檢查
- Bandit 代碼安全掃描
- 生成安全報告
```

### 2. 持續部署 (CD)

#### 🚀 自動部署觸發條件
- 推送到 `main` 分支
- 創建 Git 標籤 (v*.*.*)
- 手動觸發工作流

#### 📦 部署流程
```yaml
1. 創建 GitHub Release
2. 構建 Docker 映像
3. 推送到 GitHub Container Registry
4. 構建分發包
5. 部署到測試環境
6. 部署到生產環境 (僅正式版本)
```

## 🐳 Docker 部署

### 本地 Docker 運行

```bash
# 構建映像
docker build -t clinic-sim-ai .

# 運行容器
docker run -p 8501:8501 -p 5001:5001 clinic-sim-ai
```

### Docker Compose 部署

```bash
# 啟動所有服務
docker-compose up -d

# 啟動生產環境 (包含 Nginx 和 Redis)
docker-compose --profile production up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

## 📊 監控和報告

### GitHub Actions 報告

每次 CI/CD 運行都會生成詳細報告：

- ✅ 測試結果總結
- 📊 覆蓋率報告
- 🔒 安全掃描結果
- 🐳 Docker 構建狀態
- 📦 部署狀態

### 訪問報告

1. 進入 GitHub 專案頁面
2. 點擊 "Actions" 標籤
3. 選擇對應的工作流
4. 查看詳細的執行報告

## 🚀 發布流程

### 自動發布

1. **創建版本標籤**：
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. **GitHub Actions 自動執行**：
   - 創建 GitHub Release
   - 構建 Docker 映像
   - 生成分發包
   - 部署到環境

### 手動發布

1. 進入 GitHub Actions
2. 選擇 "Release Pipeline"
3. 點擊 "Run workflow"
4. 輸入版本號 (例如: v1.0.0)
5. 點擊 "Run workflow"

## 🔧 配置說明

### 環境變數

在 GitHub 倉庫設置中添加以下 Secrets：

```yaml
# GitHub Container Registry
GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

# 部署環境 (可選)
DEPLOY_TOKEN: your_deploy_token
AWS_ACCESS_KEY_ID: your_aws_key
AWS_SECRET_ACCESS_KEY: your_aws_secret
```

### 環境配置

創建以下環境：

1. **staging**: 測試環境
2. **production**: 生產環境

每個環境可以設置不同的保護規則和 Secrets。

## 📈 最佳實踐

### 開發流程

1. **功能開發**：
   ```bash
   git checkout -b feature/new-feature
   # 開發代碼
   git commit -m "Add: new feature"
   git push origin feature/new-feature
   ```

2. **創建 Pull Request**：
   - 自動觸發 CI 流程
   - 代碼審查
   - 測試通過後合併

3. **發布版本**：
   ```bash
   git checkout main
   git pull origin main
   git tag v1.0.0
   git push origin v1.0.0
   ```

### 測試策略

- ✅ **單元測試**：測試個別函數和類
- ✅ **集成測試**：測試 API 端點和服務間交互
- ✅ **端到端測試**：測試完整用戶流程
- ✅ **性能測試**：測試應用性能和負載

### 代碼質量

- 📏 **代碼風格**：使用 Black 自動格式化
- 🔍 **代碼檢查**：使用 Flake8 檢查風格問題
- 🔬 **類型檢查**：使用 MyPy 檢查類型錯誤
- 📚 **文檔**：為所有公共 API 撰寫文檔

## 🆘 故障排除

### 常見問題

#### 1. 測試失敗
```bash
# 本地重現問題
python scripts/run_tests.py --type unit -v

# 檢查依賴
python scripts/test_setup.py
```

#### 2. Docker 構建失敗
```bash
# 檢查 Dockerfile
docker build -t test-image .

# 檢查依賴
docker run --rm test-image pip list
```

#### 3. 部署失敗
```bash
# 檢查環境變數
echo $GITHUB_TOKEN

# 檢查權限
gh auth status
```

### 獲取幫助

1. 📖 查看 [GitHub Actions 文檔](https://docs.github.com/en/actions)
2. 🐛 在 [GitHub Issues](https://github.com/your-username/ClinicSim-AI/issues) 報告問題
3. 💬 參與 [GitHub Discussions](https://github.com/your-username/ClinicSim-AI/discussions)

## 🎯 未來改進

- [ ] 添加性能測試
- [ ] 實現藍綠部署
- [ ] 添加監控和告警
- [ ] 實現自動回滾
- [ ] 添加多環境部署

---

🎉 恭喜！您現在了解了 ClinicSim-AI 的完整 CI/CD 流程。這將確保代碼質量和部署的可靠性！
