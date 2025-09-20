# 🐳 Docker 設置指南

本指南將協助您使用 Docker 快速部署 ClinicSim-AI。

## 🚀 快速開始

### 選項一：僅啟動應用（推薦新手）

```bash
# 1. 構建並啟動應用
docker-compose -f docker-compose.simple.yml up --build

# 2. 訪問應用
# 前端: http://localhost:8501
# 後端: http://localhost:5001
```

### 選項二：包含AI服務

```bash
# 1. 啟動應用和Ollama AI服務
docker-compose -f docker-compose.simple.yml --profile ai up --build

# 2. 等待Ollama下載模型（首次運行需要時間）
# 3. 訪問應用
```

### 選項三：完整服務（生產環境）

```bash
# 1. 啟動所有服務
docker-compose up --build

# 2. 訪問應用
# 前端: http://localhost:8501
# 後端: http://localhost:5001
# Ollama: http://localhost:11434
```

## 📋 前置需求

### 1. 安裝 Docker

#### macOS
```bash
# 使用 Homebrew
brew install --cask docker

# 或下載 Docker Desktop
# https://www.docker.com/products/docker-desktop
```

#### Windows
```bash
# 下載 Docker Desktop
# https://www.docker.com/products/docker-desktop
```

#### Linux (Ubuntu)
```bash
# 安裝 Docker
sudo apt update
sudo apt install docker.io docker-compose

# 啟動 Docker 服務
sudo systemctl start docker
sudo systemctl enable docker

# 將用戶添加到 docker 群組
sudo usermod -aG docker $USER
```

### 2. 檢查安裝

```bash
# 檢查 Docker 版本
docker --version

# 檢查 Docker Compose 版本
docker-compose --version

# 測試 Docker 是否正常運行
docker run hello-world
```

## 🔧 配置說明

### 環境變數

在 `docker-compose.yml` 中設置：

```yaml
environment:
  - HOST=0.0.0.0          # 主機地址
  - PORT=5001             # 後端端口
  - DEBUG=false           # 調試模式
  - OLLAMA_HOST=http://ollama:11434  # Ollama 服務地址
  - OLLAMA_MODEL=llama3:8b           # AI 模型
  - OPENAI_API_KEY=your_key         # OpenAI API Key (可選)
```

### 端口映射

| 服務 | 容器端口 | 主機端口 | 說明 |
|------|----------|----------|------|
| ClinicSim-AI | 8501 | 8501 | Streamlit 前端 |
| ClinicSim-AI | 5001 | 5001 | Flask 後端 |
| Ollama | 11434 | 11434 | AI 服務 |

### 數據持久化

```yaml
volumes:
  - ./cases:/app/cases           # 病例數據
  - ./documents:/app/documents   # 臨床文檔
  - ./faiss_index:/app/faiss_index  # RAG 索引
```

## 🛠️ 常用命令

### 基本操作

```bash
# 啟動服務
docker-compose up

# 背景啟動
docker-compose up -d

# 重新構建並啟動
docker-compose up --build

# 停止服務
docker-compose down

# 查看日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f clinic-sim-ai
```

### 開發和調試

```bash
# 進入容器
docker-compose exec clinic-sim-ai bash

# 重啟特定服務
docker-compose restart clinic-sim-ai

# 查看服務狀態
docker-compose ps

# 清理未使用的映像
docker system prune
```

### 數據管理

```bash
# 備份數據
docker-compose exec clinic-sim-ai tar -czf /tmp/backup.tar.gz /app/cases /app/documents

# 恢復數據
docker cp backup.tar.gz container_id:/tmp/
docker-compose exec clinic-sim-ai tar -xzf /tmp/backup.tar.gz -C /app/
```

## 🚨 故障排除

### 常見問題

#### 1. 端口被佔用

```bash
# 檢查端口使用情況
netstat -tulpn | grep :8501
netstat -tulpn | grep :5001

# 修改端口映射
# 在 docker-compose.yml 中修改:
ports:
  - "8502:8501"  # 使用不同端口
  - "5002:5001"
```

#### 2. 權限問題

```bash
# 修復文件權限
sudo chown -R $USER:$USER .

# 或使用 sudo 運行
sudo docker-compose up
```

#### 3. 記憶體不足

```bash
# 檢查系統資源
docker stats

# 限制容器資源使用
# 在 docker-compose.yml 中添加:
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '1.0'
```

#### 4. Ollama 模型下載失敗

```bash
# 手動下載模型
docker-compose exec ollama ollama pull llama3:8b

# 或使用更小的模型
# 修改環境變數: OLLAMA_MODEL=llama3:8b
```

#### 5. 網路連接問題

```bash
# 檢查容器網路
docker network ls
docker network inspect clinic-network

# 重建網路
docker-compose down
docker network prune
docker-compose up
```

### 日誌分析

```bash
# 查看所有服務日誌
docker-compose logs

# 查看錯誤日誌
docker-compose logs | grep -i error

# 實時查看日誌
docker-compose logs -f --tail=100
```

## 🔒 安全建議

### 生產環境

```yaml
# 1. 使用非 root 用戶
user: "1000:1000"

# 2. 限制資源使用
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '1.0'

# 3. 使用環境變數文件
env_file:
  - .env.production

# 4. 啟用健康檢查
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5001/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 網路安全

```bash
# 1. 使用內部網路
networks:
  - internal

# 2. 不暴露不必要的端口
# 移除 ports 映射，使用內部通信

# 3. 使用 HTTPS
# 配置 Nginx 反向代理和 SSL 證書
```

## 📊 監控和維護

### 健康檢查

```bash
# 檢查服務健康狀態
docker-compose ps

# 檢查健康檢查結果
docker inspect clinic-sim-ai | grep -A 10 Health
```

### 性能監控

```bash
# 查看資源使用情況
docker stats

# 查看容器詳細信息
docker inspect clinic-sim-ai
```

### 定期維護

```bash
# 清理未使用的映像和容器
docker system prune -a

# 更新映像
docker-compose pull
docker-compose up -d

# 備份重要數據
docker-compose exec clinic-sim-ai tar -czf /tmp/backup-$(date +%Y%m%d).tar.gz /app/cases /app/documents
```

## 🎯 最佳實踐

1. **開發環境**：使用 `docker-compose.simple.yml`
2. **測試環境**：使用完整的 `docker-compose.yml`
3. **生產環境**：添加安全配置和監控
4. **定期更新**：保持 Docker 映像和依賴更新
5. **數據備份**：定期備份重要數據
6. **監控日誌**：設置日誌輪轉和監控

---

🎉 現在您可以使用 Docker 快速部署 ClinicSim-AI 了！
