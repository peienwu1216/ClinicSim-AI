#!/usr/bin/env python3
"""
簡單的 PDF 測試腳本
直接使用 PyMuPDF 測試 PDF 檔案解析
"""

import sys
from pathlib import Path

def test_pdf_with_pymupdf():
    """使用 PyMuPDF 直接測試 PDF 檔案"""
    print("🧪 使用 PyMuPDF 測試 PDF 檔案")
    print("=" * 50)
    
    try:
        import fitz  # PyMuPDF
        
        # 測試的 PDF 檔案
        pdf_files = [
            "documents/Research/D-Dimer對ACS判讀的影響.pdf",
            "documents/Research/D-Dimer對肺栓塞的負預測.pdf", 
            "documents/Research/肺炎診斷綜合判斷.pdf"
        ]
        
        for pdf_file in pdf_files:
            file_path = Path(pdf_file)
            print(f"\n📄 測試檔案: {file_path.name}")
            print("-" * 30)
            
            if not file_path.exists():
                print(f"❌ 檔案不存在: {file_path}")
                continue
            
            try:
                # 開啟 PDF 檔案
                doc = fitz.open(str(file_path))
                print(f"✅ 成功開啟，共 {doc.page_count} 頁")
                
                # 檢查前幾頁的內容
                total_chars = 0
                chinese_chars = 0
                
                for page_num in range(min(3, doc.page_count)):  # 檢查前3頁
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    
                    print(f"  頁面 {page_num + 1}: {len(text)} 字元")
                    
                    # 統計中文字元
                    page_chinese = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
                    chinese_chars += page_chinese
                    total_chars += len(text)
                    
                    # 顯示前200字元作為預覽
                    if text.strip():
                        preview = text[:200].replace('\n', ' ')
                        print(f"    預覽: {preview}...")
                    else:
                        print(f"    ⚠️ 頁面內容為空")
                
                print(f"  總字元數: {total_chars}")
                print(f"  中文字元數: {chinese_chars}")
                
                # 檢查關鍵詞
                keywords = ["D-Dimer", "ACS", "急性冠心症", "診斷", "判讀", "肺栓塞", "肺炎"]
                found_keywords = []
                
                # 讀取所有頁面內容來搜尋關鍵詞
                full_text = ""
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    full_text += page.get_text()
                
                for keyword in keywords:
                    if keyword in full_text:
                        found_keywords.append(keyword)
                
                print(f"  找到關鍵詞: {found_keywords}")
                
                doc.close()
                
            except Exception as e:
                print(f"❌ 處理失敗: {e}")
        
        print("\n" + "=" * 50)
        print("✅ PDF 測試完成")
        
    except ImportError as e:
        print(f"❌ 缺少 PyMuPDF: {e}")
        print("請執行: pip install pymupdf")
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    test_pdf_with_pymupdf()
