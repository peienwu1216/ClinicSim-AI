"""
RAG系統多語言查詢改進
解決語言偏向問題，確保能搜尋到英文資料
"""

def generate_multilingual_rag_queries(conversation_text: str, case_type: str = "chest_pain") -> list:
    """
    生成多語言RAG查詢，確保能搜尋到中英文資料
    """
    
    # 多語言查詢模板
    multilingual_queries = {
        "chest_pain": {
            "chinese": [
                "急性胸痛診斷流程和檢查順序",
                "ECG 心電圖在胸痛評估中的重要性", 
                "STEMI 和不穩定型心絞痛的診斷標準",
                "胸痛問診的 OPQRST 技巧和重點",
                "OSCE 問診技巧和病史詢問指南",
                "急性胸痛的鑑別診斷和檢查項目"
            ],
            "english": [
                "acute chest pain diagnostic protocol and examination sequence",
                "ECG electrocardiogram importance in chest pain evaluation",
                "STEMI and unstable angina diagnostic criteria",
                "OPQRST technique for chest pain history taking",
                "OSCE history taking skills and guidelines",
                "differential diagnosis and investigations for acute chest pain"
            ],
            "medical_terms": [
                "acute coronary syndrome diagnosis",
                "myocardial infarction diagnostic criteria",
                "chest pain emergency evaluation",
                "cardiac enzymes troponin",
                "12-lead ECG interpretation",
                "chest pain red flags"
            ]
        }
    }
    
    queries = []
    case_queries = multilingual_queries.get(case_type, multilingual_queries["chest_pain"])
    
    # 根據對話內容選擇最相關的查詢
    conversation_lower = conversation_text.lower()
    
    # 中文查詢
    queries.extend(case_queries["chinese"][:2])
    
    # 英文查詢
    queries.extend(case_queries["english"][:2])
    
    # 醫學術語查詢（更容易匹配國際指南）
    queries.extend(case_queries["medical_terms"][:2])
    
    # 根據對話內容動態調整
    if any(keyword in conversation_lower for keyword in ["ecg", "心電圖", "12導程", "electrocardiogram"]):
        queries.insert(0, "12-lead ECG interpretation")
        queries.insert(1, "ECG electrocardiogram importance in chest pain evaluation")
        
    if any(keyword in conversation_lower for keyword in ["問診", "病史", "osce", "history taking"]):
        queries.insert(0, "OSCE history taking skills and guidelines")
        queries.insert(1, "OPQRST technique for chest pain history taking")
        
    if any(keyword in conversation_lower for keyword in ["鑑別", "診斷", "檢查", "diagnosis", "investigation"]):
        queries.insert(0, "acute chest pain diagnostic protocol")
        queries.insert(1, "differential diagnosis and investigations")
    
    return queries[:6]  # 返回前6個最相關的查詢


def improved_rag_search_with_language_balance(rag_service, conversation_text: str, case_type: str = "chest_pain"):
    """
    改進的RAG搜尋，平衡中英文資料
    """
    # 生成多語言查詢
    queries = generate_multilingual_rag_queries(conversation_text, case_type)
    
    all_citations = []
    seen_content = set()  # 避免重複內容
    
    for query in queries:
        try:
            # 執行搜尋
            citations = rag_service.search_with_citations([query], k=2)
            
            for citation in citations:
                # 避免重複內容
                content_hash = hash(citation.content[:100])
                if content_hash not in seen_content:
                    seen_content.add(content_hash)
                    all_citations.append(citation)
                    
        except Exception as e:
            print(f"RAG搜尋失敗 (查詢: {query}): {e}")
            continue
    
    return all_citations[:8]  # 返回前8個最佳結果


# 使用示例
if __name__ == "__main__":
    # 測試多語言查詢生成
    test_conversation = "醫生，我想了解ECG心電圖在胸痛診斷中的重要性，以及如何進行問診。"
    
    queries = generate_multilingual_rag_queries(test_conversation)
    
    print("🔍 多語言RAG查詢示例:")
    print("=" * 50)
    for i, query in enumerate(queries, 1):
        print(f"{i}. {query}")
    
    print("\n📋 查詢語言分布:")
    chinese_count = sum(1 for q in queries if any('\u4e00' <= char <= '\u9fff' for char in q))
    english_count = len(queries) - chinese_count
    print(f"中文查詢: {chinese_count}")
    print(f"英文查詢: {english_count}")
    print(f"總計: {len(queries)}")
