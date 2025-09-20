# 👨‍💻 開發者指南

> **開發環境設置和代碼結構** | 讓開發者快速上手 ClinicSim-AI 開發

## 🏗️ 專案架構

### 目錄結構

```
ClinicSim-AI/
├── 📁 docs/                    # 文檔目錄
│   ├── quick-start.md
│   ├── installation.md
│   ├── user-manual.md
│   ├── developer-guide.md
│   ├── api-documentation.md
│   ├── architecture.md
│   ├── rag-system.md
│   ├── deployment.md
│   └── troubleshooting.md
├── 📁 src/                     # 源代碼目錄
│   ├── 📁 api/                # API 層
│   │   ├── routes.py          # 路由定義
│   │   └── dependencies.py    # 依賴注入
│   ├── 📁 config/             # 配置層
│   │   └── settings.py        # 設定管理
│   ├── 📁 frontend/           # 前端組件
│   │   ├── app.py             # 主應用
│   │   └── components/        # UI 組件
│   ├── 📁 models/             # 數據模型
│   │   ├── case.py            # 案例模型
│   │   ├── conversation.py    # 對話模型
│   │   └── report.py          # 報告模型
│   ├── 📁 services/           # 業務邏輯層
│   │   ├── ai_service.py      # AI 服務
│   │   ├── case_service.py    # 案例服務
│   │   ├── conversation_service.py
│   │   ├── rag_service.py     # RAG 服務
│   │   └── report_service.py  # 報告服務
│   ├── 📁 utils/              # 工具函式
│   │   ├── file_utils.py      # 檔案操作
│   │   ├── text_processing.py # 文字處理
│   │   └── validation.py      # 數據驗證
│   └── 📁 exceptions/         # 異常處理
│       └── base.py            # 基礎異常類
├── 📁 cases/                  # 案例數據
├── 📁 documents/              # 臨床指引
├── 📁 faiss_index/            # RAG 索引
├── 📄 main.py                 # 新版本後端入口
├── 📄 app_new.py              # 新版本前端入口
├── 📄 server.py               # 舊版本後端
├── 📄 app.py                  # 舊版本前端
├── 📄 rag_handler.py          # RAG 處理器
├── 📄 build_index.py          # 索引建立
├── 📄 install.py              # 安裝腳本
├── 📄 requirements-*.txt      # 依賴文件
└── 📄 .env                    # 環境配置
```

## 🛠️ 開發環境設置

### 1. 環境準備

```bash
# 克隆專案
git clone https://github.com/your-username/ClinicSim-AI.git
cd ClinicSim-AI

# 建立開發分支
git checkout -b feature/your-feature-name

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

### 2. 安裝開發依賴

```bash
# 安裝開發環境依賴
pip install -r requirements-dev.txt

# 安裝開發工具
pip install black flake8 mypy pytest
```

### 3. 開發工具配置

#### VS Code 設定 (.vscode/settings.json)
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

#### Pre-commit 設定 (.pre-commit-config.yaml)
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.8
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
```

## 🏛️ 架構設計

### 分層架構

```
┌─────────────────────────────────────────────────────────┐
│                   表現層 (Presentation)                   │
│  Streamlit 前端組件 + Flask API 路由                     │
└─────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────┐
│                   應用層 (Application)                    │
│  服務層 + 依賴注入 + 路由處理                             │
└─────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────┐
│                   領域層 (Domain)                        │
│  數據模型 + 業務邏輯 + 領域服務                           │
└─────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────┐
│                   基礎設施層 (Infrastructure)              │
│  工具函式 + 配置管理 + 異常處理                           │
└─────────────────────────────────────────────────────────┘
```

### 核心設計模式

#### 1. 依賴注入 (Dependency Injection)

```python
# src/api/dependencies.py
def get_dependencies() -> dict:
    """獲取所有服務依賴"""
    settings = get_settings()
    
    return {
        'ai_service': AIServiceFactory.create_from_config(settings),
        'case_service': CaseService(settings),
        'conversation_service': ConversationService(settings),
        'rag_service': RAGService(settings),
        'report_service': ReportService(settings)
    }

# 在路由中使用
@app.route('/ask_patient', methods=['POST'])
def ask_patient_route(deps: dict = Depends(get_dependencies)):
    ai_service = deps['ai_service']
    # ...
```

#### 2. 工廠模式 (Factory Pattern)

```python
# src/services/ai_service.py
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

#### 3. 策略模式 (Strategy Pattern)

```python
# src/services/ai_service.py
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

## 🔧 開發工作流程

### 1. 功能開發流程

```bash
# 1. 創建功能分支
git checkout -b feature/new-feature

# 2. 開發功能
# 編寫代碼...

# 3. 運行測試
pytest tests/

# 4. 代碼格式化
black src/
flake8 src/

# 5. 提交代碼
git add .
git commit -m "feat: add new feature"

# 6. 推送分支
git push origin feature/new-feature

# 7. 創建 Pull Request
```

### 2. 代碼規範

#### Python 代碼風格
- 遵循 PEP 8 規範
- 使用 Black 進行格式化
- 使用 Flake8 進行靜態檢查
- 使用 MyPy 進行類型檢查

#### 命名規範
```python
# 類名：PascalCase
class CaseService:
    pass

# 函數名：snake_case
def get_case_by_id(case_id: str) -> Case:
    pass

# 常數：UPPER_SNAKE_CASE
DEFAULT_CHUNK_SIZE = 1000

# 私有方法：前綴下劃線
def _validate_case_data(data: dict) -> bool:
    pass
```

#### 文檔字符串
```python
def calculate_coverage(history: List[Message], case_id: str) -> int:
    """
    計算問診覆蓋率。
    
    Args:
        history: 對話歷史列表
        case_id: 案例 ID
        
    Returns:
        覆蓋率百分比 (0-100)
        
    Raises:
        CaseNotFoundError: 當案例不存在時
        ValidationError: 當輸入數據無效時
    """
    pass
```

### 3. 測試策略

#### 單元測試
```python
# tests/test_case_service.py
import pytest
from src.services.case_service import CaseService
from src.models.case import Case

def test_load_case_success():
    """測試成功載入案例"""
    service = CaseService()
    case = service.load_case("case_chest_pain_acs_01")
    
    assert isinstance(case, Case)
    assert case.id == "case_chest_pain_acs_01"

def test_load_case_not_found():
    """測試載入不存在的案例"""
    service = CaseService()
    
    with pytest.raises(CaseNotFoundError):
        service.load_case("nonexistent_case")
```

#### 整合測試
```python
# tests/test_api_integration.py
import requests

def test_ask_patient_endpoint():
    """測試 ask_patient API 端點"""
    response = requests.post(
        "http://localhost:5001/ask_patient",
        json={
            "history": [{"role": "user", "content": "你好"}],
            "case_id": "case_chest_pain_acs_01"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "coverage" in data
```

#### 測試運行
```bash
# 運行所有測試
pytest

# 運行特定測試
pytest tests/test_case_service.py

# 運行測試並生成覆蓋率報告
pytest --cov=src tests/

# 運行測試並生成 HTML 報告
pytest --cov=src --cov-report=html tests/
```

## 📝 添加新功能

### 1. 添加新的 API 端點

```python
# src/api/routes.py
@app.route('/new_endpoint', methods=['POST'])
def new_endpoint_route(
    request_data: dict,
    deps: dict = Depends(get_dependencies)
):
    """新的 API 端點"""
    try:
        # 驗證輸入
        validate_input(request_data)
        
        # 調用服務
        service = deps['your_service']
        result = service.process(request_data)
        
        return jsonify({"success": True, "data": result})
    
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500
```

### 2. 添加新的服務

```python
# src/services/your_service.py
from src.services.base import BaseService
from src.models.your_model import YourModel

class YourService(BaseService):
    """您的服務類"""
    
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.your_config = settings.your_config
    
    def process(self, data: dict) -> YourModel:
        """處理業務邏輯"""
        # 實現您的邏輯
        pass
    
    def validate(self, data: dict) -> bool:
        """驗證數據"""
        # 實現驗證邏輯
        pass
```

### 3. 添加新的數據模型

```python
# src/models/your_model.py
from pydantic import BaseModel, Field
from typing import Optional, List

class YourModel(BaseModel):
    """您的數據模型"""
    
    id: str = Field(..., description="唯一標識符")
    name: str = Field(..., description="名稱")
    description: Optional[str] = Field(None, description="描述")
    tags: List[str] = Field(default_factory=list, description="標籤列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "example_id",
                "name": "示例名稱",
                "description": "這是一個示例",
                "tags": ["標籤1", "標籤2"]
            }
        }
```

### 4. 添加新的前端組件

```python
# src/frontend/components/your_component.py
import streamlit as st
from src.frontend.components.base import BaseComponent

class YourComponent(BaseComponent):
    """您的前端組件"""
    
    def render(self, **kwargs):
        """渲染組件"""
        st.title("您的組件")
        
        # 實現您的 UI 邏輯
        user_input = st.text_input("輸入內容")
        
        if st.button("提交"):
            # 處理用戶輸入
            self.handle_submit(user_input)
    
    def handle_submit(self, input_data: str):
        """處理提交"""
        # 實現提交邏輯
        pass
```

## 🔍 調試技巧

### 1. 日誌記錄

```python
# src/utils/logger.py
import logging
import sys

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """設置日誌記錄器"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # 控制台處理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    return logger

# 使用範例
logger = setup_logger(__name__)
logger.info("這是一條資訊日誌")
logger.error("這是一條錯誤日誌")
```

### 2. 斷點調試

```python
# 使用 pdb 進行調試
import pdb

def debug_function():
    # 設置斷點
    pdb.set_trace()
    
    # 您的代碼
    result = some_computation()
    
    return result
```

### 3. 性能分析

```python
# 使用 cProfile 進行性能分析
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # 您的代碼
    your_function()
    
    profiler.disable()
    
    # 分析結果
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # 顯示前 10 個最慢的函數
```

## 🚀 部署準備

### 1. 環境變數配置

```bash
# 生產環境 .env
AI_PROVIDER=ollama
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3:8b
HOST=0.0.0.0
PORT=5001
DEBUG=false
LOG_LEVEL=INFO
```

### 2. Docker 配置

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY requirements-production.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements-production.txt

# 複製應用代碼
COPY . .

# 暴露端口
EXPOSE 5001

# 啟動命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "main:app"]
```

### 3. 健康檢查

```python
# src/api/routes.py
@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    try:
        # 檢查依賴服務
        deps = get_dependencies()
        
        # 檢查 AI 服務
        ai_service = deps['ai_service']
        ai_status = ai_service.health_check()
        
        # 檢查 RAG 服務
        rag_service = deps['rag_service']
        rag_status = rag_service.health_check()
        
        return jsonify({
            "status": "healthy",
            "ai_service": ai_status,
            "rag_service": rag_status,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500
```

## 📚 文檔維護

### 1. API 文檔

```python
# 使用 Flask-RESTX 或類似工具自動生成 API 文檔
from flask_restx import Api, Resource, fields

api = Api(app, doc='/docs/')

# 定義數據模型
case_model = api.model('Case', {
    'id': fields.String(required=True, description='案例 ID'),
    'name': fields.String(required=True, description='案例名稱'),
    'description': fields.String(description='案例描述')
})

# 定義 API 端點
@api.route('/cases')
class CaseList(Resource):
    @api.doc('list_cases')
    @api.marshal_list_with(case_model)
    def get(self):
        """獲取案例列表"""
        pass
```

### 2. 代碼文檔

```python
# 使用 Sphinx 生成代碼文檔
# docs/conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

# 生成文檔
# sphinx-apidoc -o docs src/
# make html
```

## 🤝 貢獻指南

### 1. 提交規範

```bash
# 提交訊息格式
<type>(<scope>): <subject>

<body>

<footer>

# 範例
feat(api): add new endpoint for case management

Add a new REST API endpoint to manage clinical cases.
This includes CRUD operations for case data.

Closes #123
```

### 2. Pull Request 流程

1. **Fork 專案**
2. **創建功能分支**
3. **編寫代碼和測試**
4. **運行所有檢查**
5. **提交 Pull Request**
6. **代碼審查**
7. **合併到主分支**

### 3. 代碼審查檢查清單

- [ ] 代碼遵循專案規範
- [ ] 所有測試通過
- [ ] 文檔已更新
- [ ] 沒有安全問題
- [ ] 性能影響已評估

---

**希望這個指南能幫助您順利進行開發！** 🎉
