# ClinicSim-AI Cursor 開發指南

## 🏗️ 專案架構概覽

本專案已重構為模組化、可維護的架構，遵循關注點分離原則。

### 📁 目錄結構

```
ClinicSim-AI/
├── src/                          # 核心源碼目錄
│   ├── __init__.py              # 模組初始化
│   ├── config/                  # 配置管理
│   │   ├── __init__.py
│   │   └── settings.py          # 系統設定（Pydantic BaseSettings）
│   ├── models/                  # 數據模型
│   │   ├── __init__.py
│   │   ├── case.py             # 案例模型
│   │   ├── conversation.py     # 對話模型
│   │   ├── report.py           # 報告模型
│   │   └── vital_signs.py      # 生命體徵模型
│   ├── services/               # 業務邏輯服務層
│   │   ├── __init__.py
│   │   ├── ai_service.py       # AI 服務抽象層
│   │   ├── case_service.py     # 案例管理服務
│   │   ├── conversation_service.py  # 對話管理服務
│   │   ├── rag_service.py      # RAG 服務
│   │   └── report_service.py   # 報告生成服務
│   ├── api/                    # API 層
│   │   ├── __init__.py
│   │   ├── dependencies.py     # 依賴注入
│   │   └── routes.py           # Flask 路由定義
│   ├── frontend/               # 前端組件
│   │   ├── __init__.py
│   │   ├── app.py             # Streamlit 主應用程式
│   │   └── components/        # 可重用組件
│   │       ├── __init__.py
│   │       ├── base.py        # 基礎組件類別
│   │       ├── sidebar.py     # 側邊欄組件
│   │       ├── chat_interface.py  # 聊天介面組件
│   │       ├── report_display.py  # 報告顯示組件
│   │       ├── vital_signs.py     # 生命體徵組件
│   │       └── coverage_meter.py  # 覆蓋率儀表板組件
│   ├── exceptions/             # 自定義異常
│   │   ├── __init__.py
│   │   └── base.py            # 基礎異常類別
│   └── utils/                 # 工具函式
│       ├── __init__.py
│       ├── text_processing.py # 文字處理工具
│       ├── validation.py      # 數據驗證工具
│       └── file_utils.py      # 檔案處理工具
├── main.py                    # 後端主入口點
├── app_new.py                # 新版本前端入口點
├── app.py                    # 舊版本前端（保留）
├── server.py                 # 舊版本後端（保留）
├── build_index.py            # RAG 索引建構工具
├── rag_handler.py            # 舊版本 RAG（保留）
├── cases/                    # 案例數據目錄
├── documents/                # 文檔目錄
├── faiss_index/             # FAISS 向量索引目錄
└── requirements.txt          # 依賴清單
```

## 🎯 核心設計原則

### 1. 關注點分離 (Separation of Concerns)
- **Models**: 純數據模型，使用 Pydantic 進行驗證
- **Services**: 業務邏輯處理，不涉及 UI 或 API 細節
- **API**: 僅處理 HTTP 請求和回應
- **Frontend**: 僅處理 UI 展示和用戶交互

### 2. 依賴注入 (Dependency Injection)
- 所有服務通過 `dependencies.py` 統一管理
- 使用單例模式確保服務實例一致性
- 便於測試和模擬

### 3. 配置管理
- 使用 Pydantic BaseSettings 進行配置管理
- 支援環境變數和 .env 檔案
- 類型安全的配置驗證

### 4. 錯誤處理
- 自定義異常類別層次結構
- 統一的錯誤處理機制
- 詳細的錯誤日誌記錄

## 🚀 開發工作流程

### 1. 啟動開發環境

```bash
# 啟動後端
python main.py

# 啟動前端（新版本）
streamlit run app_new.py

# 或使用舊版本
streamlit run app.py
```

### 2. 添加新功能

#### 添加新的數據模型
1. 在 `src/models/` 中創建新的模型檔案
2. 使用 Pydantic BaseModel 定義結構
3. 在 `src/models/__init__.py` 中導出

#### 添加新的服務
1. 在 `src/services/` 中創建服務檔案
2. 實現業務邏輯
3. 在 `src/api/dependencies.py` 中註冊服務
4. 在 `src/services/__init__.py` 中導出

#### 添加新的 API 端點
1. 在 `src/api/routes.py` 中添加路由函式
2. 使用依賴注入獲取服務
3. 實現錯誤處理和數據驗證

#### 添加新的前端組件
1. 在 `src/frontend/components/` 中創建組件檔案
2. 繼承 `BaseComponent` 類別
3. 實現 `render()` 方法
4. 在 `src/frontend/components/__init__.py` 中導出

### 3. 測試策略

#### 單元測試
```bash
# 為每個服務創建測試檔案
pytest tests/unit/test_case_service.py
pytest tests/unit/test_ai_service.py
```

#### 整合測試
```bash
# 測試 API 端點
pytest tests/integration/test_api_routes.py
```

#### 端到端測試
```bash
# 測試完整用戶流程
pytest tests/e2e/test_complete_workflow.py
```

## 🔧 配置管理

### 環境變數設定
創建 `.env` 檔案：

```env
# 應用程式設定
APP_NAME=ClinicSim-AI
APP_VERSION=2.0.0
DEBUG=false

# 伺服器設定
HOST=0.0.0.0
PORT=5001

# AI 設定
AI_PROVIDER=ollama  # ollama, lemonade, mock
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3:8b

# RAG 設定
RAG_MODEL_NAME=nomic-ai/nomic-embed-text-v1.5
RAG_CHUNK_SIZE=800
RAG_CHUNK_OVERLAP=100
RAG_SEARCH_K=3

# 案例設定
DEFAULT_CASE_ID=case_chest_pain_acs_01
```

### 動態配置載入
```python
from src.config import get_settings

settings = get_settings()
print(f"AI Provider: {settings.ai_provider}")
print(f"Ollama Host: {settings.ollama_host}")
```

## 🎨 前端組件開發

### 基礎組件結構
```python
from src.frontend.components.base import BaseComponent
import streamlit as st

class MyComponent(BaseComponent):
    def __init__(self, key_prefix: str = ""):
        super().__init__(key_prefix)
    
    def render(self, **kwargs) -> None:
        # 實現組件渲染邏輯
        st.write("Hello World")
        
        # 使用狀態管理
        if st.button("Click me"):
            self.set_state("clicked", True)
        
        if self.get_state("clicked", False):
            st.success("Button was clicked!")
```

### 組件使用
```python
from src.frontend.components import MyComponent

# 在應用程式中使用
my_component = MyComponent("my_prefix")
my_component.render()
```

## 🔌 API 開發

### 新增 API 端點
```python
# 在 src/api/routes.py 中
@app.route('/my_endpoint', methods=['POST'])
def my_endpoint_route():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "缺少請求數據"}), 400
        
        # 取得服務依賴
        deps = get_dependencies()
        my_service = deps['my_service']
        
        # 處理業務邏輯
        result = my_service.process_data(data)
        
        return jsonify({"result": result})
        
    except Exception as e:
        app.logger.error(f"my_endpoint 錯誤: {traceback.format_exc()}")
        return jsonify({"error": "內部伺服器錯誤"}), 500
```

### 依賴注入
```python
# 在 src/api/dependencies.py 中
def get_dependencies() -> Dict[str, Any]:
    settings = get_settings()
    
    # 初始化新服務
    my_service = MyService(settings)
    
    return {
        # ... 其他服務
        "my_service": my_service
    }
```

## 🧪 測試開發

### 服務測試
```python
# tests/unit/test_my_service.py
import pytest
from src.services.my_service import MyService
from src.config.settings import get_settings

class TestMyService:
    def setup_method(self):
        self.settings = get_settings()
        self.service = MyService(self.settings)
    
    def test_process_data(self):
        input_data = {"test": "data"}
        result = self.service.process_data(input_data)
        
        assert result is not None
        assert "processed" in result
```

### API 測試
```python
# tests/integration/test_api.py
import pytest
from src.api import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()

def test_my_endpoint(client):
    response = client.post('/my_endpoint', json={"test": "data"})
    
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data
```

## 📊 監控和日誌

### 日誌配置
```python
import logging

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 在服務中使用
logger.info("處理用戶請求")
logger.error("發生錯誤", exc_info=True)
```

### 健康檢查
```python
# API 端點: /health
{
    "status": "healthy",
    "service": "ClinicSim-AI",
    "version": "2.0.0"
}
```

## 🚀 部署指南

### 生產環境配置
```env
DEBUG=false
AI_PROVIDER=ollama
OLLAMA_HOST=http://your-ollama-server:11434
OLLAMA_MODEL=llama3:8b
```

### Docker 部署
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5001

CMD ["python", "main.py"]
```

## 🐛 常見問題和解決方案

### 1. 導入錯誤
**問題**: `ModuleNotFoundError: No module named 'src'`
**解決**: 確保在專案根目錄運行，並檢查 `sys.path` 設定

### 2. AI 服務連接失敗
**問題**: AI 服務無法連接
**解決**: 檢查 AI 提供者配置和網路連接

### 3. RAG 索引未找到
**問題**: RAG 系統未初始化
**解決**: 執行 `python build_index.py` 建立索引

### 4. 前端組件狀態問題
**問題**: Streamlit 組件狀態不正確
**解決**: 使用 `key_prefix` 確保狀態鍵的唯一性

## 📚 最佳實踐

### 1. 代碼組織
- 保持每個檔案專注於單一職責
- 使用類型提示提高代碼可讀性
- 遵循 PEP 8 代碼風格

### 2. 錯誤處理
- 使用自定義異常類別
- 記錄詳細的錯誤資訊
- 提供用戶友善的錯誤訊息

### 3. 性能優化
- 使用緩存減少重複計算
- 異步處理長時間運行的任務
- 優化數據庫查詢

### 4. 安全性
- 驗證所有輸入數據
- 使用安全的檔案路徑操作
- 實施適當的錯誤處理

## 🔄 遷移指南

### 從舊版本遷移
1. 備份現有數據和配置
2. 更新依賴套件
3. 測試新功能
4. 逐步遷移現有功能

### 向後兼容性
- 保留舊的入口點檔案（`app.py`, `server.py`）
- 提供遷移工具和文檔
- 支援漸進式升級

---

## 📞 支援和貢獻

如果您在開發過程中遇到問題，請：

1. 檢查本指南的常見問題部分
2. 查看專案的 Issue 頁面
3. 創建新的 Issue 並提供詳細資訊
4. 參與討論和貢獻代碼

**祝您開發愉快！** 🎉
