"""
RAG (Retrieval-Augmented Generation) 服務
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..config.settings import get_settings
from ..models.report import Citation


class RAGService:
    """RAG 服務類"""
    
    def __init__(self, settings=None):
        self.settings = settings or get_settings()
        self.vector_store = None
        self.embeddings = None
        self._initialize_rag()
    
    def _initialize_rag(self) -> None:
        """初始化 RAG 系統"""
        if not self.settings.faiss_index_dir.exists():
            print(f"⚠️ 警告：RAG 索引目錄不存在: {self.settings.faiss_index_dir}")
            print("   請先執行 `python build_index.py` 來建立索引")
            return
        
        try:
            print("💡 [RAG] 正在載入 RAG 向量索引...")
            
            # 初始化 embedding 模型
            from langchain_community.embeddings import HuggingFaceEmbeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.settings.rag_model_name,
                model_kwargs={'trust_remote_code': True},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            # 載入 FAISS 索引
            from langchain_community.vectorstores import FAISS
            self.vector_store = FAISS.load_local(
                str(self.settings.faiss_index_dir),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
            print("✅ [RAG] RAG 索引載入成功")
            
        except Exception as e:
            print(f"❌ [RAG] RAG 索引載入失敗: {e}")
            self.vector_store = None
            self.embeddings = None
    
    def search(self, query: str, k: Optional[int] = None) -> str:
        """執行 RAG 搜尋"""
        if not self.vector_store:
            return "RAG 系統未初始化，無法執行搜尋。"
        
        k = k or self.settings.rag_search_k
        print(f"[RAG] 正在搜尋關於 '{query}' 的資料...")
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            
            if not results:
                return "在知識庫中找不到相關資料。"
            
            # 格式化結果
            context = "\n---\n".join([
                f"來源: {doc.metadata.get('source', '未知')}\n內容: {doc.page_content}"
                for doc in results
            ])
            
            return context
            
        except Exception as e:
            print(f"[RAG] 搜尋失敗: {e}")
            return f"RAG 搜尋發生錯誤: {str(e)}"
    
    def search_with_citations(self, queries: List[str], k: Optional[int] = None) -> List[Citation]:
        """執行多個查詢並返回帶引註的結果"""
        citations = []
        
        for i, query in enumerate(queries, 1):
            context = self.search(query, k)
            
            if context and "RAG 系統未初始化" not in context and "找不到相關資料" not in context:
                citation = Citation(
                    id=i,
                    query=query,
                    source=f"臨床指引 {i}",
                    content=context,
                    metadata={"search_k": k or self.settings.rag_search_k}
                )
                citations.append(citation)
        
        return citations
    
    def generate_rag_queries(self, conversation_text: str, case_type: str = "chest_pain") -> List[str]:
        """根據對話內容和案例類型生成 RAG 查詢"""
        base_queries = {
            "chest_pain": [
                "急性胸痛診斷流程和檢查順序",
                "ECG 心電圖在胸痛評估中的重要性",
                "STEMI 和不穩定型心絞痛的診斷標準",
                "胸痛問診的 OPQRST 技巧和重點"
            ],
            "default": [
                "臨床診斷流程和檢查順序",
                "關鍵症狀的評估方法",
                "診斷標準和治療指引",
                "問診技巧和重點"
            ]
        }
        
        return base_queries.get(case_type, base_queries["default"])
    
    def is_available(self) -> bool:
        """檢查 RAG 服務是否可用"""
        return self.vector_store is not None
    
    def get_index_info(self) -> Dict[str, Any]:
        """取得索引資訊"""
        if not self.vector_store:
            return {"status": "not_initialized", "index_path": str(self.settings.faiss_index_dir)}
        
        return {
            "status": "initialized",
            "index_path": str(self.settings.faiss_index_dir),
            "embedding_model": self.settings.rag_model_name,
            "search_k": self.settings.rag_search_k
        }
