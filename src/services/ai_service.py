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

# AMD NPU 加速相關套件
try:
    from lemonade.api import from_pretrained, get_device_info
    LEMONADE_SDK_AVAILABLE = True
except ImportError:
    LEMONADE_SDK_AVAILABLE = False
    print("⚠️ lemonade-sdk not found. NPU acceleration will not be available.")

from ..models.conversation import Message, MessageRole
from ..config.traditional_chinese_config import ensure_traditional_chinese


class AIProvider(str, Enum):
    """AI 提供者類型"""
    OLLAMA = "ollama"
    LEMONADE = "lemonade"  # 統一的 Lemonade 提供者（支援 SDK 和 Server 模式）
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
    """統一的 Lemonade AI 服務實現 (支援 SDK 和 Server 模式)"""
    
    def __init__(self, config):
        self.config = config
        self.model = None
        self.tokenizer = None
        self.client = None
        self.device_info = None
        self._initialize_service()
    
    def _initialize_service(self):
        """初始化服務（SDK 或 Server 模式）"""
        if self.config.is_lemonade_server_mode():
            self._initialize_server_mode()
        else:
            self._initialize_sdk_mode()
    
    def _initialize_sdk_mode(self):
        """初始化 SDK 模式（直接載入模型）"""
        if not LEMONADE_SDK_AVAILABLE:
            raise RuntimeError("lemonade-sdk not available. Install with: pip install lemonade-sdk")
        
        print(f"[Lemonade SDK] 載入模型: {self.config.lemonade_model_checkpoint}")
        print(f"[Lemonade SDK] 使用 recipe: {self.config.lemonade_recipe}")
        
        try:
            # 載入模型和 tokenizer
            self.model, self.tokenizer = from_pretrained(
                checkpoint=self.config.lemonade_model_checkpoint,
                recipe=self.config.lemonade_recipe
            )
            
            # 獲取設備信息
            self.device_info = get_device_info()
            print(f"[Lemonade SDK] 設備信息: {self.device_info}")
            
            # 檢查 NPU 可用性
            if self.config.lemonade_recipe == "oga-npu" and not self._is_npu_available():
                print("⚠️ 警告: 請求使用 NPU 但未檢測到 NPU 設備")
                print("建議切換到: LEMONADE_RECIPE=oga-hybrid 或 hf-cpu")
            
        except Exception as e:
            print(f"❌ 無法載入 Lemonade 模型: {e}")
            raise RuntimeError(f"Failed to load Lemonade model: {e}")
    
    def _initialize_server_mode(self):
        """初始化 Server 模式（OpenAI 兼容 API）"""
        try:
            self.client = OpenAI(
                base_url=self.config.lemonade_base_url,
                api_key=self.config.lemonade_api_key
            )
            print(f"[Lemonade Server] 連接成功: {self.config.lemonade_base_url}")
            print(f"[Lemonade Server] 使用模型: {self.config.get_effective_model_name()}")
        except Exception as e:
            print(f"❌ 無法初始化 Lemonade Server 客戶端: {e}")
            raise RuntimeError(f"Failed to initialize Lemonade Server client: {e}")
    
    def _is_npu_available(self) -> bool:
        """檢查 NPU 是否可用"""
        if not self.device_info:
            return False
        
        # 檢查設備信息中是否包含 NPU 相關信息
        device_str = str(self.device_info).lower()
        return any(keyword in device_str for keyword in ["npu", "ryzen", "amd", "hybrid"])
    
    def chat(self, messages: List[Message], **kwargs) -> str:
        """發送聊天請求"""
        if self.config.is_lemonade_server_mode():
            return self._chat_server_mode(messages, **kwargs)
        else:
            return self._chat_sdk_mode(messages, **kwargs)
    
    def _chat_sdk_mode(self, messages: List[Message], **kwargs) -> str:
        """SDK 模式聊天"""
        if not self.model or not self.tokenizer:
            raise RuntimeError("Lemonade model not loaded")
        
        # 將消息轉換為文本
        prompt = self._messages_to_prompt(messages)
        
        try:
            print(f"[Lemonade SDK] 生成回應 (recipe: {self.config.lemonade_recipe})")
            response = self.model.generate(prompt, max_new_tokens=kwargs.get('max_tokens', 512))
            return response
        except Exception as e:
            error_msg = f"❌ Lemonade SDK 生成失敗: {e}"
            print(error_msg)
            return f"無法生成回應，請檢查模型載入狀態。錯誤詳情: {e}"
    
    def _chat_server_mode(self, messages: List[Message], **kwargs) -> str:
        """Server 模式聊天"""
        if not self.client:
            raise RuntimeError("Lemonade Server client not initialized")
        
        # 將 Message 物件轉換為 OpenAI 需要的字典格式
        lemonade_messages = [
            {"role": msg.role.value, "content": msg.content} 
            for msg in messages
        ]
        
        try:
            print(f"[Lemonade Server] 發送請求到: {self.client.base_url}")
            print(f"[Lemonade Server] 使用模型: {self.config.get_effective_model_name()}")
            
            response = self.client.chat.completions.create(
                model=self.config.get_effective_model_name(),
                messages=lemonade_messages,
                **kwargs
            )
            result = response.choices[0].message.content
            print(f"[Lemonade Server] 回應成功")
            return result
        except Exception as e:
            error_msg = f"❌ Lemonade Server 請求失敗: {e}"
            print(error_msg)
            return f"無法連接到 Lemonade Server，請檢查服務狀態。錯誤詳情: {e}"
    
    def _messages_to_prompt(self, messages: List[Message]) -> str:
        """將消息列表轉換為提示文本"""
        prompt_parts = []
        for msg in messages:
            if msg.role == MessageRole.USER:
                prompt_parts.append(f"User: {msg.content}")
            elif msg.role == MessageRole.ASSISTANT:
                prompt_parts.append(f"Assistant: {msg.content}")
            elif msg.role == MessageRole.SYSTEM:
                prompt_parts.append(f"System: {msg.content}")
        
        return "\n".join(prompt_parts)
    
    def is_available(self) -> bool:
        """檢查服務是否可用"""
        if self.config.is_lemonade_server_mode():
            return self._is_server_available()
        else:
            return self._is_sdk_available()
    
    def _is_sdk_available(self) -> bool:
        """檢查 SDK 模式是否可用"""
        if not self.model or not self.tokenizer:
            print("⚠️ Lemonade SDK 模型未載入")
            return False
        
        try:
            # 執行簡單的測試推理
            test_prompt = "Hello"
            test_response = self.model.generate(test_prompt, max_new_tokens=10)
            print(f"[Lemonade SDK] 測試推理成功: {test_response[:50]}...")
            return True
        except Exception as e:
            print(f"⚠️ Lemonade SDK 測試推理失敗: {e}")
            return False
    
    def _is_server_available(self) -> bool:
        """檢查 Server 模式是否可用"""
        if not self.client:
            print("⚠️ Lemonade Server 客戶端未初始化")
            return False
        
        try:
            # 透過列出模型來驗證連線
            models = self.client.models.list()
            print(f"[Lemonade Server] 連接成功，位於 {self.client.base_url}")
            print(f"[Lemonade Server] 可用模型: {[model.id for model in models.data]}")
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
            # 需要傳入 config 物件
            config = kwargs.get("config")
            if not config:
                raise ValueError("Lemonade service requires config object")
            return LemonadeAIService(config)
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
            return LemonadeAIService(config)
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
