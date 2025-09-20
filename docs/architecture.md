# 🏗️ 專案架構

> **系統設計和技術架構** | ClinicSim-AI 的完整架構說明

## 🎯 架構概述

ClinicSim-AI 採用分層架構設計，實現了關注點分離、模組化和可擴展性。

### 設計原則
- **🔧 模組化** - 清晰的模組邊界和職責分離
- **🔄 可擴展** - 支援新功能和組件的輕鬆添加
- **🧪 可測試** - 便於單元測試和整合測試
- **⚙️ 可配置** - 支援多環境配置和部署

## 📊 系統架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                    前端層 (Presentation Layer)                │
├─────────────────────────────────────────────────────────────┤
│  Streamlit 前端組件                                         │
│  ├── SidebarComponent      ├── ChatInterfaceComponent      │
│  ├── ReportDisplayComponent├── VitalSignsComponent         │
│  └── CoverageMeterComponent└── BaseComponent               │
│                                                            │
│  Flask API 路由                                             │
│  ├── /ask_patient         ├── /get_feedback_report         │
│  ├── /get_detailed_report ├── /cases                      │
│  └── /rag/status         └── Error Handlers               │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   應用層 (Application Layer)                 │
├─────────────────────────────────────────────────────────────┤
│  依賴注入容器                                                │
│  ├── Service Factory      ├── Configuration Manager       │
│  └── Dependency Resolver  └── Lifecycle Manager           │
│                                                            │
│  路由處理器                                                 │
│  ├── Request Validation   ├── Response Formatting         │
│  └── Error Handling       └── Logging                     │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  業務層 (Business Layer)                     │
├─────────────────────────────────────────────────────────────┤
│  核心服務                                                    │
│  ├── AIService            ├── CaseService                 │
│  ├── ConversationService  ├── ReportService               │
│  └── RAGService           └── ValidationService           │
│                                                            │
│  業務邏輯                                                    │
│  ├── 對話管理              ├── 報告生成                    │
│  ├── 覆蓋率計算            ├── 引註處理                    │
│  └── 生命體徵更新          └── 案例驗證                    │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  領域層 (Domain Layer)                       │
├─────────────────────────────────────────────────────────────┤
│  領域模型                                                    │
│  ├── Case                 ├── Conversation               │
│  ├── Message             ├── Report                      │
│  ├── Citation            ├── VitalSigns                  │
│  └── User                └── Session                     │
│                                                            │
│  領域服務                                                    │
│  ├── Case Domain Service ├── Conversation Domain Service │
│  └── Report Domain Service└── Validation Domain Service   │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                基礎設施層 (Infrastructure Layer)              │
├─────────────────────────────────────────────────────────────┤
│  數據存儲                                                    │
│  ├── 案例數據 (JSON)       ├── RAG 索引 (FAISS)           │
│  └── 臨床指引 (Documents)  └── 配置數據 (.env)            │
│                                                            │
│  外部服務                                                    │
│  ├── Ollama AI Service    ├── Lemonade AI Service        │
│  ├── HuggingFace Embeddings├── FAISS Vector Store        │
│  └── LangChain Framework  └── Streamlit Frontend         │
│                                                            │
│  工具和輔助                                                  │
│  ├── 文件處理              ├── 文字處理                   │
│  ├── 數據驗證              ├── 錯誤處理                   │
│  └── 日誌記錄              └── 配置管理                   │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 數據流

### 請求處理流程

```
用戶請求 → 前端組件 → API 路由 → 服務層 → 領域層 → 基礎設施層
    ↓         ↓         ↓        ↓        ↓         ↓
  UI 渲染   狀態管理   路由處理   業務邏輯   領域邏輯   數據存取
    ↑         ↑         ↑        ↑        ↑         ↑
用戶響應 ← 前端更新 ← JSON 響應 ← 服務結果 ← 領域結果 ← 數據返回
```

### 對話流程

```
1. 用戶輸入 → 前端驗證 → API 接收
2. 案例載入 → 對話歷史更新 → AI 服務調用
3. AI 回應生成 → 覆蓋率計算 → 生命體徵更新
4. 響應返回 → 前端顯示 → 用戶互動
```

### 報告生成流程

```
1. 對話完成 → 觸發報告生成
2. RAG 搜尋 → 臨床指引檢索 → 引註生成
3. LLM 整合 → 上下文注入 → 報告生成
4. 格式化處理 → 引註標記 → 前端顯示
```

## 🎨 設計模式

### 1. 分層架構 (Layered Architecture)

```python
# 每層都有明確的職責
class PresentationLayer:
    """表現層：處理用戶界面和 API 接口"""
    pass

class ApplicationLayer:
    """應用層：處理應用邏輯和協調"""
    pass

class BusinessLayer:
    """業務層：處理核心業務邏輯"""
    pass

class DomainLayer:
    """領域層：定義業務概念和規則"""
    pass

class InfrastructureLayer:
    """基礎設施層：處理數據存儲和外部服務"""
    pass
```

### 2. 依賴注入 (Dependency Injection)

```python
# 依賴注入容器
class DIContainer:
    def __init__(self):
        self._services = {}
        self._singletons = {}
    
    def register(self, interface, implementation, singleton=False):
        self._services[interface] = implementation
        if singleton:
            self._singletons[interface] = None
    
    def resolve(self, interface):
        if interface in self._singletons:
            if self._singletons[interface] is None:
                self._singletons[interface] = self._create_instance(interface)
            return self._singletons[interface]
        return self._create_instance(interface)
```

### 3. 工廠模式 (Factory Pattern)

```python
# AI 服務工廠
class AIServiceFactory:
    @staticmethod
    def create_from_config(settings: Settings) -> AIService:
        if settings.ai_provider == "ollama":
            return OllamaAIService(settings)
        elif settings.ai_provider == "lemonade":
            return LemonadeAIService(settings)
        else:
            return MockAIService(settings)
```

### 4. 策略模式 (Strategy Pattern)

```python
# AI 服務策略
class AIService(ABC):
    @abstractmethod
    def chat(self, messages: List[dict]) -> str:
        pass

class OllamaAIService(AIService):
    def chat(self, messages: List[dict]) -> str:
        # Ollama 實現
        pass

class LemonadeAIService(AIService):
    def chat(self, messages: List[dict]) -> str:
        # Lemonade 實現
        pass
```

### 5. 觀察者模式 (Observer Pattern)

```python
# 對話狀態觀察者
class ConversationObserver(ABC):
    @abstractmethod
    def on_message_added(self, message: Message):
        pass
    
    @abstractmethod
    def on_coverage_updated(self, coverage: int):
        pass

class CoverageMeterObserver(ConversationObserver):
    def on_coverage_updated(self, coverage: int):
        # 更新覆蓋率顯示
        pass
```

## 🔧 技術棧

### 後端技術

| 技術 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.8+ | 主要開發語言 |
| **Flask** | 3.1+ | Web 框架 |
| **Pydantic** | 2.11+ | 數據驗證和設定 |
| **LangChain** | 0.3+ | RAG 框架 |
| **FAISS** | 1.12+ | 向量搜尋 |
| **Ollama** | 0.5+ | 本地 LLM |

### 前端技術

| 技術 | 版本 | 用途 |
|------|------|------|
| **Streamlit** | 1.49+ | Web 應用框架 |
| **Python** | 3.8+ | 前端開發語言 |
| **CSS** | - | 樣式設計 |
| **JavaScript** | - | 交互邏輯 |

### 開發工具

| 工具 | 用途 |
|------|------|
| **Black** | 代碼格式化 |
| **Flake8** | 代碼檢查 |
| **MyPy** | 類型檢查 |
| **Pytest** | 單元測試 |
| **Pre-commit** | 提交前檢查 |

## 📁 目錄結構

```
ClinicSim-AI/
├── 📁 docs/                    # 文檔目錄
│   ├── quick-start.md          # 快速開始
│   ├── installation.md         # 安裝指南
│   ├── user-manual.md          # 使用者手冊
│   ├── developer-guide.md      # 開發者指南
│   ├── api-documentation.md    # API 文檔
│   ├── architecture.md         # 架構文檔
│   ├── rag-system.md           # RAG 系統
│   ├── deployment.md           # 部署指南
│   └── troubleshooting.md      # 故障排除
├── 📁 src/                     # 源代碼目錄
│   ├── 📁 api/                # API 層
│   │   ├── __init__.py
│   │   ├── routes.py          # 路由定義
│   │   └── dependencies.py    # 依賴注入
│   ├── 📁 config/             # 配置層
│   │   ├── __init__.py
│   │   └── settings.py        # 設定管理
│   ├── 📁 frontend/           # 前端組件
│   │   ├── __init__.py
│   │   ├── app.py             # 主應用
│   │   └── components/        # UI 組件
│   │       ├── __init__.py
│   │       ├── base.py        # 基礎組件
│   │       ├── chat_interface.py
│   │       ├── coverage_meter.py
│   │       ├── report_display.py
│   │       ├── sidebar.py
│   │       └── vital_signs.py
│   ├── 📁 models/             # 數據模型
│   │   ├── __init__.py
│   │   ├── case.py            # 案例模型
│   │   ├── conversation.py    # 對話模型
│   │   ├── report.py          # 報告模型
│   │   └── vital_signs.py     # 生命體徵模型
│   ├── 📁 services/           # 業務邏輯層
│   │   ├── __init__.py
│   │   ├── ai_service.py      # AI 服務
│   │   ├── case_service.py    # 案例服務
│   │   ├── conversation_service.py
│   │   ├── rag_service.py     # RAG 服務
│   │   └── report_service.py  # 報告服務
│   ├── 📁 utils/              # 工具函式
│   │   ├── __init__.py
│   │   ├── file_utils.py      # 檔案操作
│   │   ├── text_processing.py # 文字處理
│   │   └── validation.py      # 數據驗證
│   └── 📁 exceptions/         # 異常處理
│       ├── __init__.py
│       └── base.py            # 基礎異常類
├── 📁 cases/                  # 案例數據
│   └── case_chest_pain_acs_01.json
├── 📁 documents/              # 臨床指引
│   └── acute_chest_pain_guidelines.txt
├── 📁 faiss_index/            # RAG 索引 (不進版本控制)
├── 📁 tests/                  # 測試目錄
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_services.py
│   └── test_models.py
├── 📄 main.py                 # 新版本後端入口
├── 📄 app_new.py              # 新版本前端入口
├── 📄 server.py               # 舊版本後端
├── 📄 app.py                  # 舊版本前端
├── 📄 rag_handler.py          # RAG 處理器
├── 📄 build_index.py          # 索引建立
├── 📄 install.py              # 安裝腳本
├── 📄 requirements-*.txt      # 依賴文件
├── 📄 .env                    # 環境配置
├── 📄 .gitignore              # Git 忽略
├── 📄 Dockerfile              # Docker 配置
├── 📄 docker-compose.yml      # Docker Compose
└── 📄 README.md               # 專案說明
```

## 🔄 數據模型關係

### 核心實體關係

```
Case (案例)
├── has many → Conversation (對話)
├── has many → Message (訊息)
├── has many → Report (報告)
└── has one → PatientProfile (病人資料)

Conversation (對話)
├── belongs to → Case
├── has many → Message
├── has many → Report
└── has one → VitalSigns

Message (訊息)
├── belongs to → Conversation
├── has role → user/assistant
└── has content → text

Report (報告)
├── belongs to → Conversation
├── has many → Citation
└── has type → feedback/detailed

Citation (引註)
├── belongs to → Report
├── has query → search query
├── has source → document source
└── has content → retrieved text
```

## 🚀 擴展性設計

### 水平擴展

```python
# 支援多實例部署
class LoadBalancer:
    def __init__(self):
        self.instances = []
    
    def add_instance(self, instance):
        self.instances.append(instance)
    
    def route_request(self, request):
        # 負載均衡邏輯
        return self.select_instance(request)
```

### 垂直擴展

```python
# 支援資源動態調整
class ResourceManager:
    def __init__(self):
        self.cpu_limit = 80
        self.memory_limit = 85
    
    def check_resources(self):
        # 檢查資源使用情況
        pass
    
    def scale_up(self):
        # 垂直擴展邏輯
        pass
```

### 功能擴展

```python
# 插件系統
class PluginManager:
    def __init__(self):
        self.plugins = {}
    
    def register_plugin(self, name, plugin):
        self.plugins[name] = plugin
    
    def execute_plugin(self, name, *args, **kwargs):
        if name in self.plugins:
            return self.plugins[name].execute(*args, **kwargs)
```

## 🔒 安全性設計

### 輸入驗證

```python
# 使用 Pydantic 進行輸入驗證
class MessageRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    role: MessageRole = Field(...)
    
    @validator('content')
    def validate_content(cls, v):
        # 防止 XSS 攻擊
        return html.escape(v)
```

### 錯誤處理

```python
# 統一的錯誤處理
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500
```

### 日誌安全

```python
# 安全的日誌記錄
class SecureLogger:
    def log_request(self, request):
        # 移除敏感資訊
        sanitized_request = self.sanitize_request(request)
        logger.info(f"Request: {sanitized_request}")
    
    def sanitize_request(self, request):
        # 移除密碼、令牌等敏感資訊
        pass
```

## 📊 監控和觀測性

### 健康檢查

```python
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "services": {
            "ai_service": check_ai_service(),
            "rag_service": check_rag_service(),
            "database": check_database()
        }
    })
```

### 指標收集

```python
# 使用 Prometheus 收集指標
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('requests_total', 'Total requests')
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    REQUEST_COUNT.inc()
    REQUEST_DURATION.observe(time.time() - request.start_time)
    return response
```

## 🔮 未來架構演進

### 微服務架構

```
┌─────────────────────────────────────────────────────────────┐
│                   微服務架構                                │
├─────────────────────────────────────────────────────────────┤
│  API Gateway → 服務發現 → 配置中心 → 監控中心              │
│       ↓            ↓           ↓           ↓               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │  AI     │  │  Case   │  │  RAG    │  │  Report │       │
│  │ Service │  │ Service │  │ Service │  │ Service │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### 容器化部署

```dockerfile
# 多階段構建
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim as runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
EXPOSE 5001
CMD ["python", "main.py"]
```

### 雲原生架構

```yaml
# Kubernetes 部署
apiVersion: apps/v1
kind: Deployment
metadata:
  name: clinicsim-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: clinicsim-ai
  template:
    metadata:
      labels:
        app: clinicsim-ai
    spec:
      containers:
      - name: clinicsim-ai
        image: clinicsim-ai:latest
        ports:
        - containerPort: 5001
        env:
        - name: AI_PROVIDER
          value: "ollama"
```

---

**這個架構為 ClinicSim-AI 提供了堅實的基礎，支援當前的功能需求和未來的擴展！** 🎉
