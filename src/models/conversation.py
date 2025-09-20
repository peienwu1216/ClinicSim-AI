"""
對話相關數據模型
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """訊息角色"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """單一訊息模型"""
    role: MessageRole
    content: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ConversationState(str, Enum):
    """對話狀態"""
    ACTIVE = "active"
    ENDED = "ended"
    REPORT_GENERATED = "report_generated"
    DETAILED_REPORT_GENERATED = "detailed_report_generated"


class Conversation(BaseModel):
    """對話模型"""
    case_id: str
    messages: List[Message] = Field(default_factory=list)
    state: ConversationState = ConversationState.ACTIVE
    coverage: int = 0
    vital_signs: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def add_message(self, role: MessageRole, content: str, **kwargs) -> None:
        """新增訊息"""
        message = Message(role=role, content=content, **kwargs)
        self.messages.append(message)
    
    def get_user_messages(self) -> List[Message]:
        """取得使用者訊息"""
        return [msg for msg in self.messages if msg.role == MessageRole.USER]
    
    def get_conversation_text(self) -> str:
        """取得對話文字格式"""
        return "\n".join([f"{msg.role}: {msg.content}" for msg in self.messages])
    
    def end_conversation(self) -> None:
        """結束對話"""
        self.state = ConversationState.ENDED
    
    def mark_report_generated(self) -> None:
        """標記報告已生成"""
        self.state = ConversationState.REPORT_GENERATED
    
    def mark_detailed_report_generated(self) -> None:
        """標記詳細報告已生成"""
        self.state = ConversationState.DETAILED_REPORT_GENERATED
