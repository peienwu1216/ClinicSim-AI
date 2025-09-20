"""
PDF 視覺化工具
用於從原始 PDF 中截取並產生高亮顯示的圖片
"""

import os
import fitz  # PyMuPDF
from pathlib import Path
from typing import Optional, List, Tuple
import hashlib

from ..models.report import Citation


class PDFVisualizer:
    """PDF 視覺化服務"""
    
    def __init__(self, documents_path: str = "documents", cache_dir: str = "static/snippets"):
        self.documents_path = Path(documents_path)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def create_source_snippet(self, citation: Citation, highlight_text: bool = True) -> Optional[str]:
        """
        根據 citation 物件，從原始 PDF 中找到對應文字，
        高亮它，並將其渲染成一張圖片。
        返回圖片的路徑。
        """
        if not citation.page_number:
            print(f"⚠️ 引註 {citation.id} 沒有頁碼資訊，無法產生截圖")
            return None
        
        # 從 metadata 中獲取原始來源檔案路徑
        original_source = citation.metadata.get('original_source', '') if citation.metadata else ''
        if not original_source:
            print(f"⚠️ 引註 {citation.id} 沒有原始來源資訊")
            return None
        
        source_path = Path(original_source)
        if not source_path.exists():
            print(f"⚠️ 原始檔案不存在: {source_path}")
            return None
        
        page_number = citation.page_number - 1  # fitz 的頁碼是從 0 開始的
        text_to_find = citation.content
        
        # 產生一個唯一的快取檔名
        cache_key = f"cite_{citation.id}_{source_path.stem}_p{citation.page_number}"
        cache_key_hash = hashlib.md5(cache_key.encode()).hexdigest()[:8]
        snippet_filename = f"{cache_key_hash}.png"
        output_path = self.cache_dir / snippet_filename
        
        # 如果已經產生過，直接回傳路徑
        if output_path.exists():
            return str(output_path)
        
        try:
            doc = fitz.open(str(source_path))
            
            if page_number >= doc.page_count:
                print(f"⚠️ 頁碼 {page_number + 1} 超出文件範圍 (總共 {doc.page_count} 頁)")
                doc.close()
                return None
            
            page = doc.load_page(page_number)
            
            if highlight_text:
                # 在頁面中搜尋文字片段，它會回傳所有匹配項的座標
                text_instances = page.search_for(text_to_find)
                
                # 為所有找到的文字加上高亮註解
                for inst in text_instances:
                    highlight = page.add_highlight_annot(inst)
                    highlight.update()
            
            # 將整頁渲染成一張圖片
            # dpi=200 可以提升圖片解析度
            pix = page.get_pixmap(dpi=200)
            pix.save(str(output_path))
            
            doc.close()
            print(f"✅ 成功產生 PDF 截圖: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ 產生 PDF 截圖失敗: {e}")
            return None
    
    def create_page_snippet(self, source_path: str, page_number: int, 
                           highlight_texts: Optional[List[str]] = None) -> Optional[str]:
        """
        從指定 PDF 的指定頁面產生截圖，可選高亮特定文字
        
        Args:
            source_path: PDF 檔案路徑
            page_number: 頁碼 (從 1 開始)
            highlight_texts: 要高亮的文字列表
        
        Returns:
            截圖檔案路徑，如果失敗則返回 None
        """
        source_path = Path(source_path)
        if not source_path.exists():
            print(f"⚠️ 檔案不存在: {source_path}")
            return None
        
        # 產生快取檔名
        cache_key = f"page_{source_path.stem}_p{page_number}"
        if highlight_texts:
            highlight_hash = hashlib.md5('|'.join(highlight_texts).encode()).hexdigest()[:4]
            cache_key += f"_h{highlight_hash}"
        
        cache_key_hash = hashlib.md5(cache_key.encode()).hexdigest()[:8]
        snippet_filename = f"{cache_key_hash}.png"
        output_path = self.cache_dir / snippet_filename
        
        # 如果已經產生過，直接回傳路徑
        if output_path.exists():
            return str(output_path)
        
        try:
            doc = fitz.open(str(source_path))
            
            if page_number - 1 >= doc.page_count:
                print(f"⚠️ 頁碼 {page_number} 超出文件範圍 (總共 {doc.page_count} 頁)")
                doc.close()
                return None
            
            page = doc.load_page(page_number - 1)  # fitz 的頁碼是從 0 開始的
            
            if highlight_texts:
                # 高亮指定的文字
                for text in highlight_texts:
                    text_instances = page.search_for(text)
                    for inst in text_instances:
                        highlight = page.add_highlight_annot(inst)
                        highlight.update()
            
            # 將整頁渲染成一張圖片
            pix = page.get_pixmap(dpi=200)
            pix.save(str(output_path))
            
            doc.close()
            print(f"✅ 成功產生頁面截圖: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ 產生頁面截圖失敗: {e}")
            return None
    
    def get_page_text(self, source_path: str, page_number: int) -> Optional[str]:
        """
        獲取指定 PDF 頁面的文字內容
        
        Args:
            source_path: PDF 檔案路徑
            page_number: 頁碼 (從 1 開始)
        
        Returns:
            頁面文字內容，如果失敗則返回 None
        """
        source_path = Path(source_path)
        if not source_path.exists():
            return None
        
        try:
            doc = fitz.open(str(source_path))
            
            if page_number - 1 >= doc.page_count:
                doc.close()
                return None
            
            page = doc.load_page(page_number - 1)
            text = page.get_text()
            doc.close()
            
            return text
            
        except Exception as e:
            print(f"❌ 獲取頁面文字失敗: {e}")
            return None
    
    def find_text_in_page(self, source_path: str, page_number: int, search_text: str) -> List[Tuple[int, int, int, int]]:
        """
        在指定頁面中搜尋文字，返回匹配的矩形座標
        
        Args:
            source_path: PDF 檔案路徑
            page_number: 頁碼 (從 1 開始)
            search_text: 要搜尋的文字
        
        Returns:
            匹配的矩形座標列表 [(x0, y0, x1, y1), ...]
        """
        source_path = Path(source_path)
        if not source_path.exists():
            return []
        
        try:
            doc = fitz.open(str(source_path))
            
            if page_number - 1 >= doc.page_count:
                doc.close()
                return []
            
            page = doc.load_page(page_number - 1)
            text_instances = page.search_for(search_text)
            doc.close()
            
            return text_instances
            
        except Exception as e:
            print(f"❌ 搜尋頁面文字失敗: {e}")
            return []
    
    def cleanup_cache(self, max_age_days: int = 7) -> None:
        """
        清理過期的快取檔案
        
        Args:
            max_age_days: 最大保留天數
        """
        import time
        
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60
        
        for file_path in self.cache_dir.glob("*.png"):
            if current_time - file_path.stat().st_mtime > max_age_seconds:
                file_path.unlink()
                print(f"🗑️ 清理過期快取: {file_path.name}")


# 全域實例
pdf_visualizer = PDFVisualizer()
