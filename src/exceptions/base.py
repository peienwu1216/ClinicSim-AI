"""
基礎異常類別
"""


class ClinicSimError(Exception):
    """ClinicSim 基礎異常類別"""
    pass


class CaseNotFoundError(ClinicSimError):
    """案例未找到異常"""
    pass


class CaseLoadError(ClinicSimError):
    """案例載入失敗異常"""
    pass


class AIServiceError(ClinicSimError):
    """AI 服務異常"""
    pass


class RAGServiceError(ClinicSimError):
    """RAG 服務異常"""
    pass
