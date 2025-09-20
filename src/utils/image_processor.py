"""
圖片處理工具模組
用於從圖片檔案中提取文字內容
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from PIL import Image
import pytesseract
import easyocr
from langchain.schema import Document


class ImageProcessor:
    """圖片處理器"""
    
    def __init__(self):
        self.easyocr_reader = None
        self._init_easyocr()
    
    def _init_easyocr(self):
        """初始化 EasyOCR"""
        try:
            # 支援中文和英文
            self.easyocr_reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
            print("✅ EasyOCR 初始化成功")
        except Exception as e:
            print(f"⚠️ EasyOCR 初始化失敗: {e}")
            self.easyocr_reader = None
    
    def extract_text_from_image(self, image_path: Path, method: str = "easyocr") -> str:
        """從圖片中提取文字
        
        Args:
            image_path: 圖片檔案路徑
            method: 提取方法 ("easyocr" 或 "tesseract")
        
        Returns:
            提取的文字內容
        """
        try:
            if method == "easyocr" and self.easyocr_reader:
                return self._extract_with_easyocr(image_path)
            elif method == "tesseract":
                return self._extract_with_tesseract(image_path)
            else:
                print(f"⚠️ 不支援的方法: {method}")
                return ""
        except Exception as e:
            print(f"❌ 圖片文字提取失敗 {image_path}: {e}")
            return ""
    
    def _extract_with_easyocr(self, image_path: Path) -> str:
        """使用 EasyOCR 提取文字"""
        try:
            results = self.easyocr_reader.readtext(str(image_path))
            text_parts = []
            
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # 只保留信心度較高的文字
                    text_parts.append(text)
            
            return "\n".join(text_parts)
        except Exception as e:
            print(f"EasyOCR 提取失敗: {e}")
            return ""
    
    def _extract_with_tesseract(self, image_path: Path) -> str:
        """使用 Tesseract 提取文字"""
        try:
            # 設定 Tesseract 支援中文
            custom_config = r'--oem 3 --psm 6 -l chi_sim+eng'
            text = pytesseract.image_to_string(
                Image.open(image_path), 
                config=custom_config
            )
            return text.strip()
        except Exception as e:
            print(f"Tesseract 提取失敗: {e}")
            return ""
    
    def process_image_to_document(self, image_path: Path, method: str = "easyocr") -> Optional[Document]:
        """將圖片轉換為 LangChain Document 物件
        
        Args:
            image_path: 圖片檔案路徑
            method: 文字提取方法
        
        Returns:
            Document 物件或 None
        """
        try:
            # 提取文字
            text_content = self.extract_text_from_image(image_path, method)
            
            if not text_content.strip():
                print(f"⚠️ 無法從圖片中提取文字: {image_path}")
                return None
            
            # 建立 Document 物件
            metadata = {
                "source": str(image_path),
                "file_type": "image",
                "extraction_method": method,
                "file_name": image_path.name,
                "file_size": image_path.stat().st_size if image_path.exists() else 0
            }
            
            return Document(
                page_content=text_content,
                metadata=metadata
            )
            
        except Exception as e:
            print(f"❌ 圖片處理失敗 {image_path}: {e}")
            return None
    
    def get_supported_formats(self) -> List[str]:
        """取得支援的圖片格式"""
        return ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']


def process_images_in_directory(directory_path: Path, method: str = "easyocr") -> List[Document]:
    """處理目錄中的所有圖片檔案
    
    Args:
        directory_path: 目錄路徑
        method: 文字提取方法
    
    Returns:
        Document 物件列表
    """
    processor = ImageProcessor()
    documents = []
    supported_formats = processor.get_supported_formats()
    
    print(f"🔍 正在掃描目錄: {directory_path}")
    
    for file_path in directory_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in supported_formats:
            print(f"📷 正在處理圖片: {file_path.name}")
            
            doc = processor.process_image_to_document(file_path, method)
            if doc:
                documents.append(doc)
                print(f"✅ 成功提取文字: {len(doc.page_content)} 字元")
            else:
                print(f"❌ 處理失敗: {file_path.name}")
    
    print(f"📊 圖片處理完成，共處理 {len(documents)} 個檔案")
    return documents
