#!/usr/bin/env python3
"""
測試 PDF 檔案解析功能
檢查 Research 資料夾中的 PDF 檔案是否能被正確讀取
"""

import sys
from pathlib import Path

# 添加 src 目錄到路徑
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def test_pdf_parsing():
    """測試 PDF 檔案解析"""
    print("🧪 測試 PDF 檔案解析功能")
    print("=" * 50)
    
    # 測試的 PDF 檔案
    pdf_files = [
        "documents/Research/D-Dimer對ACS判讀的影響.pdf",
        "documents/Research/D-Dimer對肺栓塞的負預測.pdf", 
        "documents/Research/肺炎診斷綜合判斷.pdf"
    ]
    
    try:
        from langchain_community.document_loaders import PyMuPDFLoader
        
        for pdf_file in pdf_files:
            file_path = Path(pdf_file)
            print(f"\n📄 測試檔案: {file_path.name}")
            print("-" * 30)
            
            if not file_path.exists():
                print(f"❌ 檔案不存在: {file_path}")
                continue
            
            try:
                # 使用 PyMuPDFLoader 載入 PDF
                loader = PyMuPDFLoader(str(file_path))
                docs = loader.load()
                
                print(f"✅ 成功載入，共 {len(docs)} 頁")
                
                # 檢查每頁的內容
                for i, doc in enumerate(docs[:3]):  # 只檢查前3頁
                    content = doc.page_content.strip()
                    print(f"  頁面 {i+1}: {len(content)} 字元")
                    
                    # 顯示前200字元作為預覽
                    if content:
                        preview = content[:200].replace('\n', ' ')
                        print(f"    預覽: {preview}...")
                    else:
                        print(f"    ⚠️ 頁面內容為空")
                
                # 檢查是否有更多頁面
                if len(docs) > 3:
                    print(f"    ... 還有 {len(docs) - 3} 頁")
                
                # 檢查 metadata
                if docs:
                    metadata = docs[0].metadata
                    print(f"  Metadata: {metadata}")
                
            except Exception as e:
                print(f"❌ 載入失敗: {e}")
        
        print("\n" + "=" * 50)
        print("✅ PDF 解析測試完成")
        
    except ImportError as e:
        print(f"❌ 缺少必要依賴: {e}")
        print("請執行: pip install pymupdf langchain-community")
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

def test_specific_pdf_content():
    """測試特定 PDF 檔案的內容提取"""
    print("\n🔍 詳細內容分析")
    print("=" * 50)
    
    try:
        from langchain_community.document_loaders import PyMuPDFLoader
        
        # 測試第一個 PDF 檔案
        pdf_file = "documents/Research/D-Dimer對ACS判讀的影響.pdf"
        file_path = Path(pdf_file)
        
        if file_path.exists():
            print(f"📄 分析檔案: {file_path.name}")
            
            loader = PyMuPDFLoader(str(file_path))
            docs = loader.load()
            
            # 合併所有頁面內容
            full_content = "\n".join([doc.page_content for doc in docs])
            
            print(f"總字元數: {len(full_content)}")
            print(f"總頁數: {len(docs)}")
            
            # 檢查是否包含中文內容
            chinese_chars = sum(1 for char in full_content if '\u4e00' <= char <= '\u9fff')
            print(f"中文字元數: {chinese_chars}")
            
            # 檢查關鍵詞
            keywords = ["D-Dimer", "ACS", "急性冠心症", "診斷", "判讀"]
            found_keywords = []
            for keyword in keywords:
                if keyword in full_content:
                    found_keywords.append(keyword)
            
            print(f"找到關鍵詞: {found_keywords}")
            
            # 顯示前500字元
            print(f"\n內容預覽 (前500字元):")
            print("-" * 30)
            print(full_content[:500])
            print("-" * 30)
            
        else:
            print(f"❌ 檔案不存在: {file_path}")
            
    except Exception as e:
        print(f"❌ 詳細分析失敗: {e}")

if __name__ == "__main__":
    test_pdf_parsing()
    test_specific_pdf_content()
