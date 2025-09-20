"""
報告相關數據模型
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class ReportType(str, Enum):
    """報告類型"""
    FEEDBACK = "feedback"
    DETAILED = "detailed"


class Citation(BaseModel):
    """引註模型"""
    id: int
    query: str
    source: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class Report(BaseModel):
    """報告模型"""
    report_type: ReportType
    content: str
    case_id: str
    conversation_id: Optional[str] = None
    citations: List[Citation] = Field(default_factory=list)
    rag_queries: List[str] = Field(default_factory=list)
    coverage: int = 0
    metadata: Optional[Dict[str, Any]] = None
    
    def add_citation(self, citation: Citation) -> None:
        """新增引註"""
        self.citations.append(citation)
    
    def add_rag_query(self, query: str) -> None:
        """新增 RAG 查詢"""
        if query not in self.rag_queries:
            self.rag_queries.append(query)
