"""
AI 服務抽象層
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum

from ..models.conversation import Message, MessageRole


class AIProvider(str, Enum):
    """AI 提供者類型"""
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


class LemonadeAIService(AIService):
    """Lemonade AI 服務實現"""
    
    def __init__(self, model: str = "Qwen2.5-0.5B-Instruct-CPU", host: str = "http://127.0.0.1:5001"):
        self.model = model
        self.host = host
        self._available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """檢查 Lemonade 是否可用"""
        try:
            import requests
            response = requests.get(f"{self.host}/api/v1/models", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def chat(self, messages: List[Message], **kwargs) -> str:
        """發送聊天請求到 Lemonade"""
        if not self.is_available():
            raise RuntimeError("Lemonade service not available")
        
        # 导入并使用 call_AI.py 的方法
        import sys
        import os
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        if project_root not in sys.path:
            sys.path.append(project_root)
        from call_AI import call_ai
        
        # 将消息列表转换为字符串
        if isinstance(messages, list) and len(messages) > 0:
            # 获取最后一条用户消息
            last_message = messages[-1]
            if hasattr(last_message, 'content'):
                message_content = last_message.content
            else:
                message_content = str(last_message)
        else:
            message_content = str(messages)
        
        return call_ai(message_content, model=self.model, host=self.host)
    
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
        if provider == AIProvider.LEMONADE:
            model = kwargs.get('model', 'Qwen2.5-0.5B-Instruct-CPU')
            host = kwargs.get('host', 'http://127.0.0.1:5001')
            return LemonadeAIService(model=model, host=host)
        elif provider == AIProvider.MOCK:
            return MockAIService()
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
    
    @staticmethod
    def create_from_config(config) -> AIService:
        """從配置創建 AI 服務"""
        provider = AIProvider(config.ai_provider)
        
        if provider == AIProvider.LEMONADE:
            return LemonadeAIService(
                model=config.lemonade_model,
                host=config.lemonade_host
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