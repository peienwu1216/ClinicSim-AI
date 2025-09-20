"""
Notion API 相關例外類別
"""


class NotionAPIError(Exception):
    """Notion API 一般錯誤"""
    pass


class NotionAuthError(NotionAPIError):
    """Notion API 認證錯誤"""
    pass


class NotionDatabaseError(NotionAPIError):
    """Notion Database 存取錯誤"""
    pass


class NotionRateLimitError(NotionAPIError):
    """Notion API 速率限制錯誤"""
    pass
