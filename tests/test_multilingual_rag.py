"""
測試多語言RAG改進效果
"""

import sys
from pathlib import Path

# 添加src目錄到路徑
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.rag_service import RAGService

def test_multilingual_queries():
    """測試多語言查詢生成"""
    print("🔍 測試多語言RAG查詢生成")
    print("=" * 50)
    
    # 初始化RAG服務
    rag_service = RAGService()
    
    # 測試對話內容
    test_conversations = [
        "醫生，我想了解ECG心電圖在胸痛診斷中的重要性",
        "How to perform proper history taking for chest pain?",
        "請問如何進行胸痛的鑑別診斷？",
        "What are the diagnostic criteria for STEMI?",
        "OPQRST問診技巧是什麼？"
    ]
    
    for i, conversation in enumerate(test_conversations, 1):
        print(f"\n📝 測試對話 {i}: {conversation}")
        print("-" * 40)
        
        # 生成查詢
        queries = rag_service.generate_rag_queries(conversation, "chest_pain")
        
        print("🔍 生成的查詢:")
        for j, query in enumerate(queries, 1):
            # 檢測語言
            is_chinese = any('\u4e00' <= char <= '\u9fff' for char in query)
            language = "中文" if is_chinese else "英文"
            print(f"  {j}. [{language}] {query}")
        
        # 統計語言分布
        chinese_count = sum(1 for q in queries if any('\u4e00' <= char <= '\u9fff' for char in q))
        english_count = len(queries) - chinese_count
        print(f"\n📊 語言分布: 中文 {chinese_count} | 英文 {english_count}")

def test_rag_search_results():
    """測試RAG搜尋結果"""
    print("\n\n🔍 測試RAG搜尋結果")
    print("=" * 50)
    
    rag_service = RAGService()
    
    if not rag_service.is_available():
        print("❌ RAG服務不可用，請先執行 python build_index.py")
        return
    
    # 測試不同語言的查詢
    test_queries = [
        "acute chest pain diagnostic protocol",  # 英文查詢
        "急性胸痛診斷流程",                      # 中文查詢
        "ECG interpretation",                   # 英文醫學術語
        "心電圖判讀"                            # 中文醫學術語
    ]
    
    for query in test_queries:
        print(f"\n🔍 查詢: {query}")
        print("-" * 30)
        
        try:
            # 執行搜尋
            results = rag_service.search(query, k=2)
            
            if results and "找不到相關資料" not in results:
                print("✅ 找到相關資料:")
                # 顯示結果摘要
                lines = results.split('\n---\n')
                for i, line in enumerate(lines[:2], 1):
                    if '來源:' in line:
                        source_line = line.split('\n')[0]
                        content_preview = line.split('\n')[1][:100] + "..." if len(line.split('\n')[1]) > 100 else line.split('\n')[1]
                        print(f"  {i}. {source_line}")
                        print(f"     內容預覽: {content_preview}")
            else:
                print("❌ 未找到相關資料")
                
        except Exception as e:
            print(f"❌ 搜尋失敗: {e}")

def analyze_document_language_distribution():
    """分析文檔語言分布"""
    print("\n\n📊 分析文檔語言分布")
    print("=" * 50)
    
    documents_dir = Path("documents")
    
    if not documents_dir.exists():
        print("❌ documents目錄不存在")
        return
    
    # 分析文檔語言分布
    chinese_docs = []
    english_docs = []
    mixed_docs = []
    
    for file_path in documents_dir.rglob("*.pdf"):
        filename = file_path.name
        
        # 簡單的語言判斷（基於檔名）
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in filename)
        has_english = any(char.isalpha() and ord(char) < 128 for char in filename)
        
        if has_chinese and has_english:
            mixed_docs.append(filename)
        elif has_chinese:
            chinese_docs.append(filename)
        elif has_english:
            english_docs.append(filename)
    
    print(f"📄 文檔語言分布:")
    print(f"  中文文檔: {len(chinese_docs)}")
    for doc in chinese_docs:
        print(f"    - {doc}")
    
    print(f"\n  英文文檔: {len(english_docs)}")
    for doc in english_docs:
        print(f"    - {doc}")
    
    print(f"\n  混合語言: {len(mixed_docs)}")
    for doc in mixed_docs:
        print(f"    - {doc}")
    
    print(f"\n📊 總計: {len(chinese_docs) + len(english_docs) + len(mixed_docs)} 個文檔")

def main():
    """主函數"""
    print("🧪 多語言RAG改進測試")
    print("=" * 60)
    
    # 測試查詢生成
    test_multilingual_queries()
    
    # 測試搜尋結果
    test_rag_search_results()
    
    # 分析文檔分布
    analyze_document_language_distribution()
    
    print("\n\n🎉 測試完成！")
    print("\n💡 改進建議:")
    print("1. 多語言查詢確保能搜尋到中英文資料")
    print("2. 醫學術語查詢更容易匹配國際指南")
    print("3. 根據對話內容動態調整查詢優先順序")
    print("4. 建議增加更多英文醫學文檔以平衡語言分布")

if __name__ == "__main__":
    main()
