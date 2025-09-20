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
            # 使用相似度搜尋，並獲取分數
            results_with_scores = self.vector_store.similarity_search_with_score(query, k=k*2)  # 獲取更多結果以便過濾
            
            if not results_with_scores:
                return "在知識庫中找不到相關資料。"
            
            # 過濾低相關性的結果
            filtered_results = []
            for doc, score in results_with_scores:
                # 相似度分數越小表示越相似，設定更嚴格的閾值
                if score < 1.2:  # 更嚴格的閾值以確保相關性
                    # 額外檢查內容是否與查詢相關
                    if self._is_content_relevant(doc.page_content, query):
                        filtered_results.append(doc)
                if len(filtered_results) >= k:  # 限制結果數量
                    break
            
            if not filtered_results:
                # 如果過濾後沒有結果，使用前k個結果，但再次檢查相關性
                for doc, score in results_with_scores[:k]:
                    if self._is_content_relevant(doc.page_content, query):
                        filtered_results.append(doc)
                        if len(filtered_results) >= k:
                            break
                
                # 如果還是沒有相關結果，返回空
                if not filtered_results:
                    return "在知識庫中找不到與查詢相關的資料。"
            
            # 格式化結果，確保內容與查詢相關
            context = "\n---\n".join([
                self._format_document_content_with_query(doc.metadata.get('source', '未知'), doc.page_content, query)
                for doc in filtered_results
            ])
            
            return context
            
        except Exception as e:
            print(f"[RAG] 搜尋失敗: {e}")
            return f"RAG 搜尋發生錯誤: {str(e)}"
    
    def _format_document_content(self, source: str, content: str) -> str:
        """格式化文檔內容，移除不必要的標題和格式"""
        # 移除文檔開頭的標題（通常是第一行或前幾行）
        lines = content.strip().split('\n')
        
        # 跳過開頭的標題行（通常是文檔標題）
        content_lines = []
        skip_title = True
        
        for line in lines:
            line = line.strip()
            
            # 如果是空行，跳過
            if not line:
                continue
                
            # 如果遇到Markdown標題（## 或 ###），移除標題標記但保留內容
            if line.startswith('##') or line.startswith('###'):
                if skip_title:
                    continue
                else:
                    # 移除標題標記，保留內容
                    line = line.lstrip('#').strip()
            
            # 跳過文檔開頭的標題（包含特定關鍵詞的短行）
            if skip_title and len(line) < 50 and ('指引' in line or '指南' in line or '臨床' in line):
                skip_title = False
                continue
            
            # 移除Markdown格式標記
            line = line.replace('**', '').replace('*', '')
            
            skip_title = False
            if line:  # 只添加非空行
                content_lines.append(line)
        
        # 重新組合內容，用空格分隔，讓內容更自然
        formatted_content = ' '.join(content_lines)
        
        # 清理多餘的空格
        import re
        formatted_content = re.sub(r'\s+', ' ', formatted_content).strip()
        
        # 限制內容長度，避免過長的引用
        if len(formatted_content) > 600:
            formatted_content = formatted_content[:600] + "..."
        
        # 美化檔名顯示
        filename = source.split('/')[-1]
        clean_name = filename.replace('.pdf', '').replace('.txt', '').replace('.jpg', '').replace('_', ' ')
        return f"📚 **{clean_name}**\n\n{formatted_content}"
    
    def _format_document_content_with_query(self, source: str, content: str, query: str) -> str:
        """格式化文檔內容，確保與查詢相關，並提取最相關的段落"""
        # 移除文檔開頭的標題（通常是第一行或前幾行）
        lines = content.strip().split('\n')
        
        # 跳過開頭的標題行（通常是文檔標題）
        content_lines = []
        skip_title = True
        
        for line in lines:
            line = line.strip()
            
            # 如果是空行，跳過
            if not line:
                continue
                
            # 如果遇到Markdown標題（## 或 ###），移除標題標記但保留內容
            if line.startswith('##') or line.startswith('###'):
                if skip_title:
                    continue
                else:
                    # 移除標題標記，保留內容
                    line = line.lstrip('#').strip()
            
            # 跳過文檔開頭的標題（包含特定關鍵詞的短行）
            if skip_title and len(line) < 50 and ('指引' in line or '指南' in line or '臨床' in line):
                skip_title = False
                continue
            
            # 移除Markdown格式標記
            line = line.replace('**', '').replace('*', '')
            
            skip_title = False
            if line:  # 只添加非空行
                content_lines.append(line)
        
        # 重新組合內容
        full_content = ' '.join(content_lines)
        
        # 根據查詢提取最相關的段落
        relevant_content = self._extract_relevant_paragraph(full_content, query)
        
        # 清理多餘的空格
        import re
        relevant_content = re.sub(r'\s+', ' ', relevant_content).strip()
        
        # 限制內容長度，避免過長的引用
        if len(relevant_content) > 500:  # 減少長度以提高精準度
            relevant_content = relevant_content[:500] + "..."
        
        # 美化檔名顯示
        filename = source.split('/')[-1]
        clean_name = filename.replace('.pdf', '').replace('.txt', '').replace('.jpg', '').replace('_', ' ')
        return f"📚 **{clean_name}**\n\n{relevant_content}"
    
    def _extract_relevant_paragraph(self, content: str, query: str) -> str:
        """從內容中提取與查詢最相關的段落"""
        # 將內容按句號分割成段落
        sentences = content.split('。')
        
        # 計算每個句子與查詢的相關性
        query_words = set(query.lower().split())
        best_sentence = ""
        best_score = 0
        
        # 定義查詢相關的關鍵詞映射
        query_keywords = {
            'ecg': ['ecg', '心電圖', '12導程', '心電'],
            'opqrst': ['opqrst', '問診', '病史', 'onset', 'quality', 'radiation', 'severity', 'time'],
            '急性冠心症': ['急性冠心症', 'acs', '心肌梗塞', '心絞痛'],
            '心肌鈣蛋白': ['troponin', '心肌鈣蛋白', '心肌酵素', 'ck-mb', '檢驗', '抽血']
        }
        
        # 擴展查詢關鍵詞
        expanded_query_words = query_words.copy()
        for key, keywords in query_keywords.items():
            if any(word in query.lower() for word in [key] + keywords):
                expanded_query_words.update(keywords)
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            sentence_words = set(sentence.lower().split())
            
            # 計算詞彙重疊度
            overlap = len(expanded_query_words.intersection(sentence_words))
            if overlap > 0:
                # 計算相關性分數（重疊詞數 / 查詢詞數）
                score = overlap / len(expanded_query_words)
                if score > best_score:
                    best_score = score
                    best_sentence = sentence.strip()
        
        # 如果找到相關句子，返回該句子及其前後文
        if best_sentence and best_score > 0.1:  # 設定最小相關性閾值
            # 找到最佳句子在原文中的位置
            best_index = -1
            for i, sent in enumerate(sentences):
                if sent.strip() == best_sentence:
                    best_index = i
                    break
            
            if best_index >= 0:
                # 返回最佳句子及其前後各一句
                start = max(0, best_index - 1)
                end = min(len(sentences), best_index + 2)
                relevant_sentences = sentences[start:end]
                return '。'.join(relevant_sentences)
        
        # 如果沒有找到足夠相關的句子，嘗試在整個內容中搜尋關鍵詞
        if best_score <= 0.1:
            # 直接在內容中搜尋關鍵詞，返回包含關鍵詞的段落
            for keyword in expanded_query_words:
                if keyword in content.lower():
                    # 找到關鍵詞的位置
                    keyword_pos = content.lower().find(keyword)
                    if keyword_pos >= 0:
                        # 提取關鍵詞前後各200個字符
                        start = max(0, keyword_pos - 200)
                        end = min(len(content), keyword_pos + len(keyword) + 200)
                        relevant_content = content[start:end]
                        return relevant_content
        
        # 如果都沒有找到，返回前幾句
        return '。'.join(sentences[:2]) if len(sentences) >= 2 else content
    
    def _is_content_relevant(self, content: str, query: str) -> bool:
        """檢查內容是否與查詢相關"""
        content_lower = content.lower()
        query_lower = query.lower()
        
        # 定義查詢相關的關鍵詞映射
        query_keywords = {
            'ecg': ['ecg', '心電圖', '12導程', '心電', 'electrocardiogram'],
            'opqrst': ['opqrst', '問診', '病史', 'onset', 'quality', 'radiation', 'severity', 'time', '發作', '性質', '放射', '嚴重', '時間'],
            '急性冠心症': ['急性冠心症', 'acs', '心肌梗塞', '心絞痛', 'acute coronary syndrome', 'myocardial infarction'],
            '心肌鈣蛋白': ['troponin', '心肌鈣蛋白', '心肌酵素', 'ck-mb', '檢驗', '抽血', 'cardiac troponin'],
            '實驗室檢查': ['實驗室', '檢驗', '血液', 'laboratory', 'test', 'blood test'],
            '血液檢驗': ['血液', '檢驗', '抽血', 'blood', 'test', 'laboratory']
        }
        
        # 檢查直接匹配
        if any(word in content_lower for word in query_lower.split()):
            return True
        
        # 檢查關鍵詞映射
        for key, keywords in query_keywords.items():
            if any(word in query_lower for word in [key] + keywords):
                if any(keyword in content_lower for keyword in keywords):
                    return True
        
        # 檢查是否包含不相關的內容（如圖片OCR結果）
        irrelevant_indicators = ['案例', '案例2', '案例3', '案例4', '案例5', '特雷弗', '雅各布先生']
        if any(indicator in content for indicator in irrelevant_indicators):
            return False
        
        # 檢查內容長度，太短的內容可能不相關
        if len(content.strip()) < 20:
            return False
        
        return True
    
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
