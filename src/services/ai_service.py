"""
AI 服務抽象層
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum

# Lemonade Server 相關套件
try:
    from openai import OpenAI
except ImportError:
    # 提醒使用者安裝
    raise ImportError("openai package not found. Please install it by running: pip install openai")

from ..models.conversation import Message, MessageRole


class AIProvider(str, Enum):
    """AI 提供者類型"""
    OLLAMA = "ollama"
    LEMONADE = "lemonade"
    OPENAI = "openai"
    MOCK = "mock"


class AIService(ABC):
    """AI 服務抽象基類"""
    
    @abstractmethod
    def chat(self, messages: List[Message], **kwargs) -> str:
        """發送聊天請求"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """檢查服務是否可用"""
        pass


class OllamaAIService(AIService):
    """Ollama AI 服務實現"""
    
    def __init__(self, host: str, model: str):
        self.host = host
        self.model = model
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化 Ollama 客戶端"""
        try:
            import ollama
            self._client = ollama.Client(host=self.host)
        except ImportError:
            raise ImportError("ollama package not installed. Run: pip install ollama")
    
    def chat(self, messages: List[Message], **kwargs) -> str:
        """發送聊天請求到 Ollama"""
        if not self._client:
            raise RuntimeError("Ollama client not initialized")
        
        # 轉換訊息格式
        ollama_messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]
        
        response = self._client.chat(
            model=self.model,
            messages=ollama_messages,
            **kwargs
        )
        return response['message']['content']
    
    def is_available(self) -> bool:
        """檢查 Ollama 服務是否可用"""
        try:
            if not self._client:
                return False
            # 嘗試列出模型來測試連接
            self._client.list()
            return True
        except Exception:
            return False


class LemonadeAIService(AIService):
    """Lemonade AI 服務實現 (使用 OpenAI 相容 API)"""
    
    def __init__(self, base_url: str, model: str, api_key: str = "lemonade"):
        self.model = model
        try:
            self.client = OpenAI(base_url=base_url, api_key=api_key)
            print(f"✅ 初始化 Lemonade 客戶端成功: {base_url}")
        except Exception as e:
            print(f"❌ 無法初始化 Lemonade (OpenAI) 客戶端: {e}")
            self.client = None

    def chat(self, messages: List[Message], **kwargs) -> str:
        """發送聊天請求到 Lemonade Server"""
        if not self.client:
            raise RuntimeError("Lemonade client not initialized or failed to initialize.")

        # 將 Message 物件轉換為 OpenAI 需要的字典格式
        lemonade_messages = [
            {"role": msg.role.value, "content": msg.content} 
            for msg in messages
        ]
        
        try:
            print(f"🚀 正在呼叫 Lemonade Server: {self.client.base_url}")
            print(f"📝 使用模型: {self.model}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=lemonade_messages,
                **kwargs
            )
            result = response.choices[0].message.content
            print(f"✅ Lemonade Server 回應成功")
            return result
        except Exception as e:
            error_msg = f"❌ 呼叫 Lemonade chat API 失敗: {e}"
            print(error_msg)
            return f"無法連接到 Lemonade 服務，請檢查服務是否正在運行於 {self.client.base_url}。錯誤詳情: {e}"

    def is_available(self) -> bool:
        """檢查 Lemonade 服務是否可用"""
        if not self.client:
            print("⚠️ Lemonade 客戶端未初始化")
            return False
        try:
            # 透過列出模型來驗證連線
            models = self.client.models.list()
            print(f"✅ Lemonade Server 連接成功，位於 {self.client.base_url}")
            print(f"📋 可用模型: {[model.id for model in models.data]}")
            return True
        except Exception as e:
            print(f"⚠️ 無法連接到 Lemonade Server: {e}")
            return False


class MockAIService(AIService):
    """模擬 AI 服務，用於測試和開發"""
    
    def chat(self, messages: List[Message], **kwargs) -> str:
        """返回模擬回應"""
        last_message = messages[-1] if messages else None
        if last_message and last_message.role == MessageRole.USER:
            return f"[Mock AI] 回應: {last_message.content}"
        return "[Mock AI] 這是一個模擬回應"
    
    def is_available(self) -> bool:
        """模擬服務總是可用"""
        return True


class AIServiceFactory:
    """AI 服務工廠類"""
    
    @staticmethod
    def create_service(provider: AIProvider, **kwargs) -> AIService:
        """創建 AI 服務實例"""
        if provider == AIProvider.OLLAMA:
            return OllamaAIService(
                host=kwargs.get("host", "http://127.0.0.1:11434"),
                model=kwargs.get("model", "llama3:8b")
            )
        elif provider == AIProvider.LEMONADE:
            return LemonadeAIService(
                base_url=kwargs.get("base_url"),
                model=kwargs.get("model")
            )
        elif provider == AIProvider.MOCK:
            return MockAIService()
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
    
    @staticmethod
    def create_from_config(config) -> AIService:
        """從配置創建 AI 服務"""
        provider = AIProvider(config.ai_provider)
        
        if provider == AIProvider.OLLAMA:
            return OllamaAIService(
                host=config.ollama_host,
                model=config.ollama_model
            )
        elif provider == AIProvider.LEMONADE:
            return LemonadeAIService(
                base_url=config.lemonade_base_url,
                model=config.lemonade_model
            )
        elif provider == AIProvider.MOCK:
            return MockAIService()
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")


# 全域 AI 服務實例
_ai_service: Optional[AIService] = None


def get_ai_service(config=None) -> AIService:
    """取得全域 AI 服務實例（單例模式）"""
    global _ai_service
    if _ai_service is None and config:
        _ai_service = AIServiceFactory.create_from_config(config)
    return _ai_service


def set_ai_service(service: AIService) -> None:
    """設定全域 AI 服務實例"""
    global _ai_service
    _ai_service = service
