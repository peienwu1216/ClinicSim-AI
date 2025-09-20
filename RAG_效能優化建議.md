# RAG 效能優化建議

## 問題分析

### 當前效能狀況
- **RAG 搜尋速度**：0.2-0.5 秒（優秀）
- **即時回饋報告**：0.1 秒（優秀）
- **詳細分析報告**：71.7 秒（需要優化）

### 瓶頸識別
- RAG 搜尋：2 秒（3%）
- LLM 生成：69.7 秒（97%）
- **結論：RAG 不是瓶頸，LLM 生成是主要問題**

## 優化方案

### 方案一：減少 RAG 查詢數量（推薦）
```python
# 修改 src/services/rag_service.py
def generate_rag_queries(self, conversation_text: str, case_type: str = "chest_pain") -> List[str]:
    """根據對話內容和案例類型生成 RAG 查詢"""
    base_queries = {
        "chest_pain": [
            "急性胸痛診斷流程和檢查順序",  # 保留最重要的查詢
            "ECG 心電圖在胸痛評估中的重要性"  # 只保留 2 個查詢
        ],
        "default": [
            "臨床診斷流程和檢查順序",
            "關鍵症狀的評估方法"
        ]
    }
    return base_queries.get(case_type, base_queries["default"])
```

### 方案二：並行 RAG 搜尋
```python
# 使用並行處理加速 RAG 搜尋
import asyncio
import concurrent.futures

def search_with_citations_parallel(self, queries: List[str], k: Optional[int] = None) -> List[Citation]:
    """並行執行多個 RAG 查詢"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(self.search, query, k) for query in queries]
        results = [future.result() for future in futures]
    
    citations = []
    for i, (query, result) in enumerate(zip(queries, results), 1):
        if result and "RAG 系統未初始化" not in result:
            citation = Citation(
                id=i,
                query=query,
                source=f"臨床指引 {i}",
                content=result,
                metadata={"search_k": k or self.settings.rag_search_k}
            )
            citations.append(citation)
    
    return citations
```

### 方案三：快取 RAG 結果
```python
# 添加 RAG 結果快取
from functools import lru_cache

class RAGService:
    def __init__(self, settings=None):
        # ... 現有初始化代碼 ...
        self._cache = {}
    
    @lru_cache(maxsize=100)
    def search_cached(self, query: str, k: int) -> str:
        """帶快取的 RAG 搜尋"""
        return self.search(query, k)
```

### 方案四：優化 LLM 提示詞
```python
# 縮短 LLM 提示詞，減少生成時間
def _generate_detailed_analysis_with_llm(self, conversation: Conversation, case: Case, citations: List[Citation]) -> str:
    """使用簡化的 LLM 提示詞"""
    # 使用更簡潔的提示詞
    simplified_prompt = f"""
    請根據以下對話生成簡潔的診後分析報告：
    
    對話內容：{conversation.get_conversation_text()[:500]}...
    
    相關指引：{citations[0].content[:300] if citations else "無"}
    
    請提供：
    1. 問診評估（3-5 點）
    2. 改進建議（3-5 點）
    3. 總體評分
    
    保持簡潔，每點不超過 2 行。
    """
    # ... 其餘代碼 ...
```

## 立即可實施的優化

### 1. 減少 RAG 查詢數量
將查詢從 4 個減少到 2 個，可以節省約 1 秒。

### 2. 添加進度指示器
在詳細報告生成時顯示進度，改善用戶體驗。

### 3. 提供快速模式
添加一個「快速報告」選項，只使用 1 個 RAG 查詢。

## 預期效果

| 優化方案 | 預期改善 | 實施難度 |
|----------|----------|----------|
| 減少查詢數量 | 節省 1-2 秒 | 簡單 |
| 並行搜尋 | 節省 1-2 秒 | 中等 |
| 結果快取 | 重複查詢時節省 2-4 秒 | 中等 |
| 優化提示詞 | 節省 20-30 秒 | 簡單 |

## 結論

**RAG 搜尋速度本身是優秀的**，真正的瓶頸在於 LLM 生成時間。建議：

1. **立即實施**：減少 RAG 查詢數量到 2 個
2. **短期優化**：添加進度指示器和快速模式
3. **長期優化**：考慮使用更快的 LLM 模型或優化提示詞

**RAG 不會顯著影響問答速度，但會提升報告品質！**
