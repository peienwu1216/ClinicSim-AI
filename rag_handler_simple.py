import os
import json
import re
from typing import List, Dict, Any

class SimpleRAGSystem:
    """
    一個簡化的 RAG 系統，不依賴 langchain_community
    使用基本的文本搜索和關鍵字匹配
    """
    def __init__(self, documents_dir="documents"):
        self.documents_dir = documents_dir
        self.documents = []
        self._load_documents()
    
    def _load_documents(self):
        """載入文檔目錄中的所有文本文件"""
        if not os.path.exists(self.documents_dir):
            print(f"⚠️ 警告：文檔目錄 '{self.documents_dir}' 不存在。RAG 功能將無法運作。")
            return
        
        try:
            print("💡 [RAG] 正在載入文檔...")
            for filename in os.listdir(self.documents_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.documents_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.documents.append({
                            'source': filename,
                            'content': content,
                            'lines': content.split('\n')
                        })
            print(f"✅ [RAG] 成功載入 {len(self.documents)} 個文檔。")
        except Exception as e:
            print(f"❌ [RAG] 文檔載入失敗: {e}")
    
    def _simple_search(self, query: str, text: str) -> float:
        """簡單的文本相似度計算"""
        query_words = set(re.findall(r'\w+', query.lower()))
        text_words = set(re.findall(r'\w+', text.lower()))
        
        if not query_words:
            return 0.0
        
        # 計算詞彙重疊度
        intersection = query_words.intersection(text_words)
        return len(intersection) / len(query_words)
    
    def search(self, query: str, k: int = 3) -> str:
        """
        對載入的文檔執行簡單的文本搜索
        返回格式化後的上下文
        """
        if not self.documents:
            return "RAG 系統未初始化，無法執行搜尋。"
        
        print(f"[RAG] 正在搜尋關於 '{query}' 的資料...")
        
        # 計算每個文檔的相關性分數
        results = []
        for doc in self.documents:
            # 搜索整個文檔
            doc_score = self._simple_search(query, doc['content'])
            
            # 搜索每個段落
            for i, line in enumerate(doc['lines']):
                if line.strip():
                    line_score = self._simple_search(query, line)
                    if line_score > 0:
                        results.append({
                            'source': doc['source'],
                            'content': line.strip(),
                            'score': line_score,
                            'line_number': i + 1
                        })
        
        # 按分數排序並取前 k 個結果
        results.sort(key=lambda x: x['score'], reverse=True)
        top_results = results[:k]
        
        if not top_results:
            return "在知識庫中找不到相關資料。"
        
        context = "\n---\n".join([
            f"來源: {result['source']} (第 {result['line_number']} 行)\n內容: {result['content']}" 
            for result in top_results
        ])
        return context

# 創建 RAG 系統實例
rag_system = SimpleRAGSystem()
