"""
AI 服務抽象層
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum

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
    """Lemonade AI 服務實現"""
    
    def __init__(self):
        self._available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """檢查 Lemonade 是否可用"""
        try:
            from lemonade import expose
            return True
        except ImportError:
            return False
    
    def chat(self, messages: List[Message], **kwargs) -> str:
        """發送聊天請求到 Lemonade"""
        if not self.is_available():
            raise RuntimeError("Lemonade service not available")
        
        # 這裡需要根據實際的 Lemonade API 進行實現
        # 目前返回模擬回應
        return "[From Lemonade] 這是一個來自 Lemonade 的回應..."
    
    def is_available(self) -> bool:
        """檢查 Lemonade 服務是否可用"""
        return self._available


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
            return LemonadeAIService()
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
            return LemonadeAIService()
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
