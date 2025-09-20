import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

class RAGSystem:
    """
    一個獨立的 RAG 系統類別，封裝了所有與 RAG 相關的操作。
    """
    def __init__(self, index_path="faiss_index", model_name="nomic-ai/nomic-embed-text-v1.5"):
        self.index_path = index_path
        self.model_name = model_name
        self.vector_store = None
        self._load_index()

    def _load_index(self):
        """在初始化時載入 FAISS 索引，只執行一次。"""
        if not os.path.exists(self.index_path):
            print(f"⚠️ 警告：在 '{self.index_path}' 找不到索引檔案。RAG 功能將無法運作。")
            print("   > 請先執行 `python build_index.py` 來建立索引。")
            return
        
        try:
            print("💡 [RAG] 正在載入 RAG 向量索引...")
            embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs={'trust_remote_code': True},
                encode_kwargs={'normalize_embeddings': True}
            )
            self.vector_store = FAISS.load_local(
                self.index_path, 
                embeddings, 
                allow_dangerous_deserialization=True # FAISS 索引的標準作法
            )
            print("✅ [RAG] RAG 索引載入成功。")
        except Exception as e:
            print(f"❌ [RAG] RAG 索引載入失敗: {e}")

    def search(self, query: str, k: int = 3) -> str:
        """
        對載入的索引執行相似度搜尋。
        返回格式化後的上下文，方便直接注入 Prompt。
        """
        if not self.vector_store:
            return "RAG 系統未初始化，無法執行搜尋。"

        print(f"[RAG] 正在搜尋關於 '{query}' 的資料...")
        results = self.vector_store.similarity_search(query, k=k)
        
        if not results:
            return "在知識庫中找不到相關資料。"

        context = "\n---\n".join([
            f"來源: {doc.metadata.get('source', '未知')}\n內容: {doc.page_content}" 
            for doc in results
        ])
        return context

# 在 server.py 啟動時，只會建立一次這個物件
rag_system = RAGSystem()
