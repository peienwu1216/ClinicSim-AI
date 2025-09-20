# 🚀 部署指南

> **生產環境部署** | 完整的部署流程和最佳實踐

## 🎯 部署概述

本指南涵蓋 ClinicSim-AI 在不同環境中的部署方法，包括本地開發、測試環境和生產環境。

### 部署選項

| 環境 | 方法 | 適用場景 |
|------|------|----------|
| **本地開發** | 直接運行 | 開發和測試 |
| **Docker** | 容器化部署 | 測試和演示 |
| **雲端部署** | 雲服務平台 | 生產環境 |
| **Lemonade** | 比賽環境 | 競賽部署 |

## 🖥️ 本地部署

### 開發環境部署

```bash
# 1. 克隆專案
git clone https://github.com/your-username/ClinicSim-AI.git
cd ClinicSim-AI

# 2. 自動安裝
python install.py

# 3. 啟動服務
python main.py  # 後端
streamlit run app_new.py  # 前端
```

### 生產模式部署

```bash
# 使用 Gunicorn 部署
pip install gunicorn

# 啟動生產服務器
gunicorn -w 4 -b 0.0.0.0:5001 main:app

# 使用 Waitress (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5001 main:app
```

## 🐳 Docker 部署

### 1. 創建 Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY requirements-production.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements-production.txt

# 複製應用代碼
COPY . .

# 創建非 root 用戶
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# 暴露端口
EXPOSE 5001

# 健康檢查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# 啟動命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "--timeout", "120", "main:app"]
```

### 2. 創建 docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "5001:5001"
    environment:
      - AI_PROVIDER=ollama
      - OLLAMA_HOST=http://ollama:11434
      - DEBUG=false
    depends_on:
      - ollama
    volumes:
      - ./faiss_index:/app/faiss_index
      - ./cases:/app/cases
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:5001
    depends_on:
      - backend
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  ollama_data:
```

### 3. 前端 Dockerfile

```dockerfile
# Dockerfile.frontend
FROM python:3.11-slim

WORKDIR /app

COPY requirements-production.txt .
RUN pip install --no-cache-dir -r requirements-production.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_new.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 4. Nginx 配置

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:5001;
    }

    upstream frontend {
        server frontend:8501;
    }

    server {
        listen 80;
        server_name your-domain.com;

        # 重定向到 HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # API 路由
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # 前端路由
        location / {
            proxy_pass http://frontend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### 5. 部署命令

```bash
# 構建和啟動
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down

# 重新構建
docker-compose up -d --build
```

## ☁️ 雲端部署

### AWS 部署

#### 1. EC2 部署

```bash
# 啟動 EC2 實例
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1d0 \
    --instance-type t3.medium \
    --key-name your-key \
    --security-group-ids sg-xxxxxxxxx

# 連接實例
ssh -i your-key.pem ec2-user@your-instance-ip

# 安裝 Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# 部署應用
git clone https://github.com/your-username/ClinicSim-AI.git
cd ClinicSim-AI
docker-compose up -d
```

#### 2. ECS 部署

```yaml
# ecs-task-definition.json
{
  "family": "clinicsim-ai",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "your-account.dkr.ecr.region.amazonaws.com/clinicsim-ai:latest",
      "portMappings": [
        {
          "containerPort": 5001,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "AI_PROVIDER",
          "value": "ollama"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/clinicsim-ai",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud 部署

#### 1. Cloud Run 部署

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/clinicsim-ai', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/clinicsim-ai']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: [
      'run', 'deploy', 'clinicsim-ai',
      '--image', 'gcr.io/$PROJECT_ID/clinicsim-ai',
      '--platform', 'managed',
      '--region', 'us-central1',
      '--allow-unauthenticated'
    ]
```

```bash
# 部署到 Cloud Run
gcloud builds submit --config cloudbuild.yaml
```

### Azure 部署

#### 1. Container Instances 部署

```bash
# 創建資源組
az group create --name clinicsim-ai-rg --location eastus

# 部署容器實例
az container create \
    --resource-group clinicsim-ai-rg \
    --name clinicsim-ai \
    --image your-registry.azurecr.io/clinicsim-ai:latest \
    --dns-name-label clinicsim-ai \
    --ports 5001 \
    --environment-variables AI_PROVIDER=ollama
```

## 🏆 Lemonade 部署

### 1. 準備工作

```bash
# 在本地建立 RAG 索引
python build_index.py

# 打包索引檔案
tar -czf faiss_index.tar.gz faiss_index/

# 打包應用程式
tar -czf clinicsim-ai.tar.gz \
    --exclude=venv \
    --exclude=.git \
    --exclude=__pycache__ \
    .
```

### 2. 上傳和部署

```bash
# 上傳到 Lemonade 服務器
scp clinicsim-ai.tar.gz faiss_index.tar.gz user@lemonade-server:/path/to/deployment/

# 在 Lemonade 服務器上
ssh user@lemonade-server

# 解壓縮
tar -xzf clinicsim-ai.tar.gz
tar -xzf faiss_index.tar.gz

# 安裝依賴
python -m venv venv
source venv/bin/activate
pip install -r requirements-lemonade.txt

# 設置環境變數
export AI_PROVIDER=lemonade
export LEMONADE_HOST=http://lemonade-ai:8080

# 啟動應用
python main.py
```

### 3. Lemonade 特定配置

```python
# lemonade_config.py
class LemonadeConfig:
    AI_PROVIDER = "lemonade"
    LEMONADE_HOST = os.getenv("LEMONADE_HOST", "http://lemonade-ai:8080")
    LEMONADE_MODEL = os.getenv("LEMONADE_MODEL", "qwen3-1.7b")
    
    # Lemonade 特定的優化
    CHUNK_SIZE = 800  # 較小的分塊
    SEARCH_K = 3      # 適中的搜尋結果數量
    TIMEOUT = 30      # 較短的超時時間
```

## 🔧 環境配置

### 生產環境配置

```bash
# .env.production
# AI 服務配置
AI_PROVIDER=ollama
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=llama3:8b

# 服務器配置
HOST=0.0.0.0
PORT=5001
DEBUG=false
LOG_LEVEL=INFO

# RAG 配置
RAG_INDEX_PATH=/app/faiss_index
EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5

# 安全配置
SECRET_KEY=your-secret-key
CORS_ORIGINS=["https://yourdomain.com"]

# 監控配置
ENABLE_METRICS=true
METRICS_PORT=9090
```

### 開發環境配置

```bash
# .env.development
AI_PROVIDER=ollama
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3:8b
HOST=127.0.0.1
PORT=5001
DEBUG=true
LOG_LEVEL=DEBUG
```

## 📊 監控和日誌

### 日誌配置

```python
# logging_config.py
import logging
import logging.handlers

def setup_logging():
    # 創建日誌目錄
    os.makedirs('logs', exist_ok=True)
    
    # 配置根日誌器
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                'logs/app.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
```

### 監控配置

```python
# monitoring.py
from prometheus_client import Counter, Histogram, start_http_server

# 定義指標
REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint).inc()
    REQUEST_DURATION.observe(time.time() - request.start_time)
    return response

# 啟動監控服務器
start_http_server(9090)
```

### 健康檢查

```python
# health_check.py
@app.route('/health')
def health_check():
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "services": {}
    }
    
    # 檢查 AI 服務
    try:
        ai_service = get_ai_service()
        ai_service.health_check()
        health_status["services"]["ai_service"] = "healthy"
    except Exception as e:
        health_status["services"]["ai_service"] = f"unhealthy: {str(e)}"
    
    # 檢查 RAG 服務
    try:
        rag_service = get_rag_service()
        rag_service.health_check()
        health_status["services"]["rag_service"] = "healthy"
    except Exception as e:
        health_status["services"]["rag_service"] = f"unhealthy: {str(e)}"
    
    return jsonify(health_status)
```

## 🔒 安全配置

### SSL/TLS 配置

```nginx
# SSL 配置
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/ssl/certs/yourdomain.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # 其他安全標頭
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
}
```

### 防火牆配置

```bash
# UFW 防火牆配置
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5001/tcp  # 僅開發環境
sudo ufw enable
```

### 環境變數安全

```bash
# 使用 Docker Secrets
echo "your-secret-key" | docker secret create secret_key -
echo "your-database-password" | docker secret create db_password -

# 在 docker-compose.yml 中使用
services:
  backend:
    secrets:
      - secret_key
      - db_password
    environment:
      - SECRET_KEY_FILE=/run/secrets/secret_key
      - DB_PASSWORD_FILE=/run/secrets/db_password
```

## 📈 性能優化

### 應用程式優化

```python
# 連接池配置
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# 快取配置
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@cache.memoize(timeout=300)
def expensive_operation(param):
    # 快取 5 分鐘
    pass
```

### 資料庫優化

```sql
-- 索引優化
CREATE INDEX idx_conversation_case_id ON conversations(case_id);
CREATE INDEX idx_message_conversation_id ON messages(conversation_id);
CREATE INDEX idx_report_conversation_id ON reports(conversation_id);

-- 查詢優化
EXPLAIN ANALYZE SELECT * FROM conversations WHERE case_id = 'case_chest_pain_acs_01';
```

### 系統優化

```bash
# 系統參數調整
echo 'net.core.somaxconn = 65535' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_max_syn_backlog = 65535' >> /etc/sysctl.conf
sysctl -p

# 檔案描述符限制
echo '* soft nofile 65535' >> /etc/security/limits.conf
echo '* hard nofile 65535' >> /etc/security/limits.conf
```

## 🔄 CI/CD 流水線

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: |
          docker build -t clinicsim-ai:${{ github.sha }} .
      - name: Push to registry
        run: |
          docker tag clinicsim-ai:${{ github.sha }} your-registry/clinicsim-ai:latest
          docker push your-registry/clinicsim-ai:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # 部署到生產環境
          kubectl set image deployment/clinicsim-ai clinicsim-ai=your-registry/clinicsim-ai:${{ github.sha }}
```

## 🆘 故障排除

### 常見部署問題

#### 1. 容器啟動失敗
```bash
# 查看容器日誌
docker logs <container_id>

# 檢查容器狀態
docker ps -a

# 進入容器調試
docker exec -it <container_id> /bin/bash
```

#### 2. 服務無法訪問
```bash
# 檢查端口監聽
netstat -tlnp | grep :5001

# 檢查防火牆
sudo ufw status

# 檢查 DNS 解析
nslookup yourdomain.com
```

#### 3. 性能問題
```bash
# 監控資源使用
htop
iostat -x 1
df -h

# 分析應用程式性能
py-spy top --pid <pid>
```

---

**部署完成後，請查看 [故障排除](troubleshooting.md) 文檔解決可能遇到的問題！** 🎉
