"""
系統配置管理
"""

import os
from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    """系統配置類別"""
    
    # 應用程式基本設定
    app_name: str = Field(default="ClinicSim-AI", env="APP_NAME")
    app_version: str = Field(default="2.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # 伺服器設定
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=5001, env="PORT")
    
    # 前端客戶端設定（用於前端連接後端）
    backend_host: str = Field(default="127.0.0.1", env="BACKEND_HOST")
    backend_port: int = Field(default=5001, env="BACKEND_PORT")
    
    # AI 模型設定
    ai_provider: str = Field(default="ollama", env="AI_PROVIDER")  # ollama, lemonade, openai
    ollama_host: str = Field(default="http://127.0.0.1:11434", env="OLLAMA_HOST")
    ollama_model: str = Field(default="llama3:8b", env="OLLAMA_MODEL")
    
    # Lemonade Server 設定
    lemonade_base_url: str = Field(default="http://localhost:8080/api/v1", env="LEMONADE_BASE_URL")
    lemonade_model: str = Field(default="Llama-3.2-1B-Instruct-Hybrid", env="LEMONADE_MODEL")
    
    # 路徑設定
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    cases_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "cases")
    documents_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "documents")
    faiss_index_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "faiss_index")
    report_history_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "report_history")
    
    # RAG 設定
    rag_model_name: str = Field(default="nomic-ai/nomic-embed-text-v1.5", env="RAG_MODEL_NAME")
    rag_chunk_size: int = Field(default=800, env="RAG_CHUNK_SIZE")
    rag_chunk_overlap: int = Field(default=100, env="RAG_CHUNK_OVERLAP")
    rag_search_k: int = Field(default=3, env="RAG_SEARCH_K")
    
    # 案例設定
    default_case_id: str = Field(default="case_chest_pain_acs_01", env="DEFAULT_CASE_ID")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"  # 忽略額外的環境變數
    }
        
    def get_case_path(self, case_id: str) -> Path:
        """取得案例檔案路徑"""
        return self.cases_dir / f"{case_id}.json"
    
    def get_document_paths(self) -> list[Path]:
        """取得所有文檔路徑"""
        if not self.documents_dir.exists():
            return []
        
        document_paths = []
        for file_path in self.documents_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt', '.md']:
                document_paths.append(file_path)
        return document_paths


# 全域設定實例
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """取得全域設定實例（單例模式）"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """重新載入設定"""
    global _settings
    _settings = Settings()
    return _settings
