"""
API 依賴注入
"""

from typing import Dict, Any
from functools import lru_cache

from ..config.settings import get_settings
from ..services.ai_service import get_ai_service, AIServiceFactory, AIProvider
from ..services.case_service import CaseService
from ..services.conversation_service import ConversationService
from ..services.rag_service import RAGService
from ..services.report_service import ReportService
from ..services.map_reduce_service import MapReduceService


@lru_cache(maxsize=None)
def get_dependencies() -> Dict[str, Any]:
    """取得所有依賴服務（單例模式）"""
    settings = get_settings()
    
    # 初始化 AI 服務
    try:
        ai_service = AIServiceFactory.create_from_config(settings)
        print(f"✅ 使用 {settings.ai_provider} AI 服務")
    except Exception as e:
        print(f"⚠️ 無法初始化 {settings.ai_provider} AI 服務: {e}")
        # 使用模擬服務作為備用
        ai_service = AIServiceFactory.create_service(AIProvider.MOCK)
        print("✅ 使用 Mock AI 服務作為備用")
    
    # 初始化其他服務
    case_service = CaseService(settings)
    rag_service = RAGService(settings)
    map_reduce_service = MapReduceService(settings, ai_service)
    conversation_service = ConversationService(settings, case_service, ai_service)
    report_service = ReportService(settings, case_service, ai_service, rag_service, None, None, map_reduce_service)
    
    print(f"✅ 所有服務初始化完成")
    
    return {
        "settings": settings,
        "ai_service": ai_service,
        "case_service": case_service,
        "conversation_service": conversation_service,
        "rag_service": rag_service,
        "map_reduce_service": map_reduce_service,
        "report_service": report_service
    }


def get_service(service_name: str) -> Any:
    """取得特定服務"""
    dependencies = get_dependencies()
    return dependencies.get(service_name)
