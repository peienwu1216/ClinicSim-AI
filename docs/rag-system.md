# 📚 RAG 系統文檔

> **檢索增強生成技術實現** | 基於臨床指引的智慧報告生成

## 🎯 系統概述

ClinicSim-AI 整合了 RAG (Retrieval-Augmented Generation) 技術，能夠在生成診後分析報告時提供基於臨床指引的專業建議。

### 核心價值
- **🔍 智慧檢索** - 基於語義相似度的知識檢索
- **📝 引註透明** - 明確標示知識來源
- **🎓 專業建議** - 基於權威臨床指引的建議
- **⚡ 即時整合** - 與 LLM 無縫整合

## 🏗️ 系統架構

### 核心組件

```
┌─────────────────────────────────────────────────────────┐
│                    RAG 系統架構                          │
├─────────────────────────────────────────────────────────┤
│  📁 documents/          📁 faiss_index/                 │
│  ├── 臨床指引文件        ├── index.faiss               │
│  ├── OSCE 標準          ├── index.pkl                 │
│  └── 診斷流程           └── 向量資料庫                  │
└─────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────┐
│                RAG 處理流程                              │
├─────────────────────────────────────────────────────────┤
│  1. 文檔分塊 (Chunking)                                │
│  2. 向量化 (Embedding)                                 │
│  3. 索引建立 (Indexing)                                │
│  4. 相似度搜尋 (Similarity Search)                     │
│  5. 上下文注入 (Context Injection)                     │
└─────────────────────────────────────────────────────────┘
```

### 技術棧

| 組件 | 技術 | 用途 |
|------|------|------|
| **文檔處理** | PyPDF, LangChain | PDF 解析和文字提取 |
| **向量化** | HuggingFace Embeddings | 文字轉換為向量 |
| **索引** | FAISS | 高效向量搜尋 |
| **檢索** | LangChain | 語義相似度搜尋 |
| **整合** | 自定義邏輯 | 與 LLM 整合 |

## 🚀 使用流程

### 1. 準備知識文件

#### 支援的文件格式
- **PDF** - 臨床指引、教科書章節
- **TXT** - 純文字格式的指引
- **MD** - Markdown 格式的文檔

#### 文件放置
```bash
documents/
├── acute_chest_pain_guidelines.txt
├── osce_evaluation_criteria.pdf
├── clinical_decision_making.md
└── emergency_protocols.txt
```

### 2. 建立向量索引

```bash
# 執行索引建立腳本
python build_index.py

# 輸出
💡 [RAG] 正在建立向量索引...
📄 處理文件: acute_chest_pain_guidelines.txt
🔢 分塊數量: 45
📊 向量維度: 768
✅ 索引建立完成: faiss_index/
```

### 3. 系統整合

RAG 系統會自動在服務器啟動時載入：

```python
# rag_handler.py
class RAGSystem:
    def __init__(self):
        self._load_index()
    
    def search(self, query: str, k: int = 3) -> str:
        # 執行相似度搜尋
        results = self.vector_store.similarity_search(query, k=k)
        return self._format_results(results)
```

## 🔧 配置和參數

### 索引建立參數

```python
# build_index.py 配置
CHUNK_SIZE = 1000        # 文檔分塊大小
CHUNK_OVERLAP = 200      # 分塊重疊大小
EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5"  # 嵌入模型
SEARCH_K = 3             # 搜尋結果數量
```

### 搜尋參數

```python
# rag_handler.py 配置
def search(self, query: str, k: int = 3) -> str:
    """
    Args:
        query: 搜尋查詢
        k: 返回結果數量 (預設 3)
    """
    results = self.vector_store.similarity_search(query, k=k)
    return self._format_results(results)
```

## 📝 使用範例

### 基本搜尋

```python
from rag_handler import rag_system

# 搜尋相關臨床指引
query = "急性胸痛診斷流程"
results = rag_system.search(query, k=3)

print(results)
# 輸出：
# 來源: documents/acute_chest_pain_guidelines.txt
# 內容: 急性胸痛臨床指引
# 
# ## 概述
# 急性胸痛是急診科最常見的主訴之一...
```

### 在報告生成中使用

```python
# server.py 中的整合範例
def get_detailed_report(full_conversation, case_id):
    # 1. 生成多個相關查詢
    rag_queries = [
        "急性胸痛診斷流程和檢查順序",
        "ECG 心電圖在胸痛評估中的重要性",
        "STEMI 和不穩定型心絞痛的診斷標準"
    ]
    
    # 2. 搜尋相關知識
    rag_contexts = []
    citations = []
    
    for i, query in enumerate(rag_queries, 1):
        context = rag_system.search(query, k=2)
        citations.append({
            "id": i,
            "query": query,
            "source": f"臨床指引 {i}",
            "content": context
        })
        rag_contexts.append(f"### 關於 {query} [引註 {i}]\n{context}")
    
    # 3. 整合到 LLM Prompt
    combined_rag_context = "\n\n".join(rag_contexts)
    
    # 4. 生成報告
    prompt = f"""
    基於以下臨床指引生成報告：
    
    {combined_rag_context}
    
    請引用相應的指引，使用 [引註 X] 格式。
    """
```

## 🎨 引註系統

### 引註格式

```markdown
根據 [引註 1] 的診斷流程指引：
- ECG 心電圖檢查應在 10 分鐘內完成
- 這是急性胸痛評估的第一優先檢查

如 [引註 2] 所述，心電圖是急性胸痛評估的關鍵工具...
```

### 引註資料結構

```python
citation = {
    "id": 1,
    "query": "急性胸痛診斷流程",
    "source": "臨床指引 1",
    "content": "急性胸痛臨床指引\n\n## 概述\n急性胸痛是急診科最常見的主訴..."
}
```

### 前端顯示

```python
# Streamlit 前端中的引註顯示
def display_citations(citations):
    for citation in citations:
        with st.expander(f"📚 [引註 {citation['id']}] {citation['query']}"):
            st.markdown(f"**來源**: {citation['source']}")
            st.markdown(f"**查詢**: {citation['query']}")
            st.markdown("**內容**:")
            st.markdown(citation['content'])
```

## ⚡ 效能優化

### 索引優化

```python
# 調整分塊參數以平衡效能和準確性
CHUNK_SIZE = 800        # 較小的分塊提高精確度
CHUNK_OVERLAP = 150     # 適度的重疊確保連續性
```

### 搜尋優化

```python
# 使用更快的嵌入模型
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # 更快的模型

# 調整搜尋參數
SEARCH_K = 5            # 更多結果提高覆蓋率
SIMILARITY_THRESHOLD = 0.7  # 相似度閾值過濾
```

### 快取策略

```python
# 實作搜尋結果快取
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query: str, k: int) -> str:
    return rag_system.search(query, k)
```

## 🔍 故障排除

### 常見問題

#### 1. 索引建立失敗
```bash
# 錯誤：記憶體不足
# 解決：減少分塊大小
CHUNK_SIZE = 500

# 錯誤：檔案格式不支援
# 解決：轉換為 TXT 格式
```

#### 2. 搜尋結果為空
```bash
# 檢查索引狀態
curl http://localhost:5001/rag/status

# 重新建立索引
python build_index.py
```

#### 3. 搜尋速度慢
```bash
# 使用更快的嵌入模型
# 減少搜尋結果數量
# 啟用快取機制
```

### 診斷工具

```python
# RAG 系統診斷
def diagnose_rag_system():
    print("🔍 RAG 系統診斷")
    print(f"索引路徑: {rag_system.index_path}")
    print(f"嵌入模型: {rag_system.model_name}")
    print(f"向量存儲: {'已載入' if rag_system.vector_store else '未載入'}")
    
    # 測試搜尋
    test_query = "胸痛診斷"
    result = rag_system.search(test_query, k=1)
    print(f"測試搜尋: {'成功' if result else '失敗'}")
```

## 🚀 進階功能

### 多語言支援

```python
# 支援多語言嵌入模型
EMBEDDING_MODELS = {
    "zh": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "en": "sentence-transformers/all-MiniLM-L6-v2"
}
```

### 動態索引更新

```python
# 支援增量更新索引
def update_index(new_documents):
    """增量更新索引"""
    # 處理新文檔
    # 添加到現有索引
    # 重新保存索引
```

### 混合檢索

```python
# 結合關鍵字和語義搜尋
def hybrid_search(query: str):
    # 關鍵字搜尋
    keyword_results = keyword_search(query)
    
    # 語義搜尋
    semantic_results = semantic_search(query)
    
    # 結果融合
    return merge_results(keyword_results, semantic_results)
```

## 📊 監控和分析

### 使用統計

```python
# 記錄搜尋統計
search_stats = {
    "total_searches": 0,
    "avg_response_time": 0.0,
    "popular_queries": [],
    "citation_usage": {}
}
```

### 效能指標

- **搜尋延遲** - 平均搜尋回應時間
- **命中率** - 有效搜尋結果比例
- **引註使用率** - 引註在報告中的使用情況
- **用戶滿意度** - 基於反饋的品質評估

---

**RAG 系統是 ClinicSim-AI 的核心功能之一，為用戶提供基於權威臨床指引的專業建議！** 🎉
