# 🍋 Lemonade Server 配置指南

> 本指南將協助您安裝和配置 Lemonade Server，以獲得最佳的 AI 推理效能

## 📖 什麼是 Lemonade Server？

Lemonade Server 是一個專為生產環境設計的高效能 AI 推理服務，提供：

- ⚡ **超快推理速度**：比標準 Ollama 快 2-3 倍
- 🚀 **低延遲響應**：專為即時應用優化
- 🔧 **簡化部署**：一鍵安裝和配置
- 📈 **高可用性**：支援負載平衡和故障轉移
- 💰 **成本效益**：降低運營成本

## 🚀 快速安裝

### 方法一：使用 Docker (推薦)

```bash
# 拉取 Lemonade Server 映像
docker pull lemonade/lemonade-server:latest

# 啟動 Lemonade Server
docker run -d \
  --name lemonade-server \
  -p 11434:11434 \
  -v ~/.lemonade:/root/.lemonade \
  lemonade/lemonade-server:latest
```

### 方法二：直接安裝

```bash
# 下載並安裝 Lemonade Server
curl -fsSL https://lemonade.ai/install.sh | sh

# 啟動服務
lemonade serve
```

## ⚙️ 配置設定

### 1. 基本配置

創建配置文件 `~/.lemonade/config.yaml`：

```yaml
# Lemonade Server 配置
server:
  host: "0.0.0.0"
  port: 11434
  
# 模型配置
models:
  default: "llama3:8b"
  cache_size: "8GB"
  
# 效能優化
performance:
  gpu_layers: 35
  context_length: 4096
  batch_size: 512
  
# 日誌設定
logging:
  level: "info"
  file: "/var/log/lemonade/server.log"
```

### 2. 下載推薦模型

```bash
# 下載 Llama 3 8B 模型 (推薦用於 ClinicSim-AI)
lemonade pull llama3:8b

# 或下載其他模型
lemonade pull llama3:70b    # 更大模型，更高準確度
lemonade pull codellama:13b # 程式碼專用模型
```

### 3. 環境變數配置

在您的 `.env` 文件中添加：

```bash
# Lemonade Server 配置
LEMONADE_HOST=http://127.0.0.1:11434
LEMONADE_MODEL=llama3:8b

# 效能設定
LEMONADE_GPU_LAYERS=35
LEMONADE_CONTEXT_LENGTH=4096
LEMONADE_BATCH_SIZE=512

# 備選方案 (如果 Lemonade 不可用)
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3:8b
```

## 🔧 與 ClinicSim-AI 整合

### 1. 安裝 Lemonade 依賴

```bash
# 使用 Lemonade 專用依賴
pip install -r requirements-lemonade.txt
```

### 2. 配置 AI 服務

在 `src/services/ai_service.py` 中，系統會自動偵測並優先使用 Lemonade Server：

```python
# 自動偵測可用的 AI 服務
def get_ai_client():
    if is_lemonade_available():
        return LemonadeClient()
    elif is_ollama_available():
        return OllamaClient()
    else:
        return OpenAIClient()
```

### 3. 驗證配置

```bash
# 檢查 Lemonade Server 狀態
curl http://127.0.0.1:11434/api/tags

# 測試模型推理
curl -X POST http://127.0.0.1:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3:8b",
    "prompt": "Hello, how are you?",
    "stream": false
  }'
```

## 📊 效能監控

### 1. 內建監控

Lemonade Server 提供內建的效能監控：

```bash
# 查看服務狀態
lemonade status

# 查看效能指標
lemonade metrics

# 查看日誌
lemonade logs
```

### 2. 自定義監控

```python
# 在 ClinicSim-AI 中監控效能
from src.utils.monitoring import monitor_lemonade_performance

# 啟動效能監控
monitor_lemonade_performance()
```

## 🚀 生產環境部署

### 1. Docker Compose 部署

創建 `docker-compose.yml`：

```yaml
version: '3.8'
services:
  lemonade-server:
    image: lemonade/lemonade-server:latest
    ports:
      - "11434:11434"
    volumes:
      - ~/.lemonade:/root/.lemonade
      - ~/models:/root/models
    environment:
      - LEMONADE_MODEL=llama3:8b
      - LEMONADE_GPU_LAYERS=35
    restart: unless-stopped
    
  clinic-sim-ai:
    build: .
    ports:
      - "5001:5001"
      - "8501:8501"
    environment:
      - LEMONADE_HOST=http://lemonade-server:11434
    depends_on:
      - lemonade-server
    restart: unless-stopped
```

### 2. Kubernetes 部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lemonade-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: lemonade-server
  template:
    metadata:
      labels:
        app: lemonade-server
    spec:
      containers:
      - name: lemonade-server
        image: lemonade/lemonade-server:latest
        ports:
        - containerPort: 11434
        env:
        - name: LEMONADE_MODEL
          value: "llama3:8b"
        resources:
          requests:
            memory: "8Gi"
            cpu: "4"
          limits:
            memory: "16Gi"
            cpu: "8"
```

## 🔧 故障排除

### 常見問題

1. **連接失敗**
```bash
# 檢查服務狀態
systemctl status lemonade-server

# 重啟服務
systemctl restart lemonade-server
```

2. **記憶體不足**
```bash
# 調整模型參數
lemonade config --gpu-layers 20 --context-length 2048
```

3. **模型載入失敗**
```bash
# 重新下載模型
lemonade pull llama3:8b --force
```

### 效能調優

1. **GPU 加速**
```bash
# 啟用 GPU 加速
lemonade config --gpu-layers 35
```

2. **記憶體優化**
```bash
# 調整快取大小
lemonade config --cache-size 4GB
```

3. **批次處理**
```bash
# 優化批次大小
lemonade config --batch-size 512
```

## 📚 進階配置

### 1. 負載平衡

```yaml
# 多實例負載平衡
load_balancer:
  instances:
    - host: "127.0.0.1:11434"
    - host: "127.0.0.1:11435"
    - host: "127.0.0.1:11436"
  strategy: "round_robin"
```

### 2. 快取策略

```yaml
# 智能快取配置
cache:
  strategy: "lru"
  max_size: "8GB"
  ttl: "3600s"
```

### 3. 安全設定

```yaml
# API 安全配置
security:
  api_key: "your-secret-key"
  rate_limit: "100/minute"
  cors_origins: ["http://localhost:8501"]
```

## 🆘 支援與社群

- 📖 [官方文檔](https://docs.lemonade.ai)
- 💬 [Discord 社群](https://discord.gg/lemonade)
- 🐛 [問題回報](https://github.com/lemonade-ai/server/issues)
- 📧 [技術支援](mailto:support@lemonade.ai)

---

🎉 恭喜！您已成功配置 Lemonade Server。現在可以享受更快速、更穩定的 AI 推理體驗！
