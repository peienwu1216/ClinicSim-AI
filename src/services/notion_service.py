"""
Notion 整合服務
提供將報告同步到 Notion 的功能
"""

import os
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from notion_client import Client
from notion_client.errors import APIResponseError

from ..config.settings import get_settings
from ..utils.file_utils import read_file_content


class NotionService:
    """Notion 整合服務"""
    
    def __init__(self, settings=None):
        self.settings = settings or get_settings()
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化 Notion 客戶端"""
        try:
            notion_token = os.getenv('NOTION_API_KEY')
            if not notion_token:
                print("⚠️ NOTION_API_KEY 環境變數未設定，Notion 功能將不可用")
                return
            
            self.client = Client(auth=notion_token)
            print("✅ Notion 客戶端初始化成功")
        except Exception as e:
            print(f"❌ 無法初始化 Notion 客戶端: {e}")
            self.client = None
    
    def is_available(self) -> bool:
        """檢查 Notion 服務是否可用"""
        return self.client is not None
    
    def markdown_to_notion_blocks(self, markdown_text: str) -> List[Dict[str, Any]]:
        """
        將 Markdown 文字轉換為 Notion Blocks
        
        Args:
            markdown_text: Markdown 格式的文字
            
        Returns:
            Notion Blocks 列表
        """
        notion_blocks = []
        lines = markdown_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # 忽略空行
            if not line:
                continue
            
            # 處理標題
            if line.startswith('### '):
                notion_blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {"rich_text": [{"type": "text", "text": {"content": line[4:]}}]}
                })
            elif line.startswith('## '):
                notion_blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:]}}]}
                })
            elif line.startswith('# '):
                notion_blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}
                })
            
            # 處理無序列表
            elif line.startswith('- ') or line.startswith('* '):
                notion_blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}
                })
            
            # 處理有序列表
            elif re.match(r'^\d+\. ', line):
                notion_blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": re.sub(r'^\d+\. ', '', line)}}]}
                })
            
            # 處理程式碼區塊
            elif line.startswith('```'):
                # 簡化處理，將程式碼區塊視為段落
                notion_blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": line}}]}
                })
            
            # 其他內容視為段落
            else:
                notion_blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": line}}]}
                })
        
        return notion_blocks
    
    def create_page(self, parent_id: str, title: str, properties: Dict[str, Any] = None) -> Optional[str]:
        """
        在 Notion 中創建新頁面
        
        Args:
            parent_id: 父頁面或資料庫 ID
            title: 頁面標題
            properties: 頁面屬性
            
        Returns:
            創建的頁面 ID，失敗時返回 None
        """
        if not self.client:
            print("❌ Notion 客戶端未初始化")
            return None
        
        try:
            page_data = {
                "parent": {"page_id": parent_id} if not parent_id.startswith('db-') else {"database_id": parent_id},
                "properties": {
                    "title": {
                        "title": [{"text": {"content": title}}]
                    }
                }
            }
            
            if properties:
                page_data["properties"].update(properties)
            
            response = self.client.pages.create(**page_data)
            page_id = response["id"]
            print(f"✅ 成功創建 Notion 頁面: {title} (ID: {page_id})")
            return page_id
            
        except APIResponseError as e:
            print(f"❌ 創建 Notion 頁面失敗: {e}")
            return None
        except Exception as e:
            print(f"❌ 創建 Notion 頁面時發生錯誤: {e}")
            return None
    
    def add_content_to_page(self, page_id: str, content: str) -> bool:
        """
        將內容添加到 Notion 頁面
        
        Args:
            page_id: 目標頁面 ID
            content: 要添加的內容（Markdown 格式）
            
        Returns:
            是否成功添加內容
        """
        if not self.client:
            print("❌ Notion 客戶端未初始化")
            return False
        
        try:
            # 將 Markdown 轉換為 Notion Blocks
            blocks = self.markdown_to_notion_blocks(content)
            
            if not blocks:
                print("⚠️ 沒有內容可以添加")
                return False
            
            # 分批添加內容（Notion API 限制每次最多 100 個 blocks）
            for i in range(0, len(blocks), 100):
                chunk = blocks[i:i+100]
                self.client.blocks.children.append(
                    block_id=page_id,
                    children=chunk
                )
                print(f"✅ 成功添加 {len(chunk)} 個區塊到頁面")
            
            return True
            
        except APIResponseError as e:
            print(f"❌ 添加內容到 Notion 頁面失敗: {e}")
            return False
        except Exception as e:
            print(f"❌ 添加內容時發生錯誤: {e}")
            return False
    
    def sync_report_to_notion(self, report_file_path: str, page_title: str, parent_id: str = None) -> Optional[str]:
        """
        將報告檔案同步到 Notion
        
        Args:
            report_file_path: 報告檔案路徑
            page_title: Notion 頁面標題
            parent_id: 父頁面 ID（可選）
            
        Returns:
            創建的頁面 ID，失敗時返回 None
        """
        if not self.is_available():
            print("❌ Notion 服務不可用")
            return None
        
        try:
            # 讀取報告檔案
            report_content = read_file_content(Path(report_file_path))
            if not report_content:
                print(f"❌ 無法讀取報告檔案: {report_file_path}")
                return None
            
            # 如果沒有指定父頁面，使用預設的資料庫 ID
            if not parent_id:
                parent_id = os.getenv('NOTION_DATABASE_ID')
                if not parent_id:
                    print("❌ 未設定 NOTION_DATABASE_ID 環境變數")
                    return None
            
            # 創建頁面
            page_id = self.create_page(parent_id, page_title)
            if not page_id:
                return None
            
            # 添加內容
            if self.add_content_to_page(page_id, report_content):
                print(f"✅ 成功將報告同步到 Notion: {page_title}")
                return page_id
            else:
                print(f"❌ 添加報告內容到 Notion 失敗")
                return None
                
        except Exception as e:
            print(f"❌ 同步報告到 Notion 時發生錯誤: {e}")
            return None
    
    def find_page_by_title(self, title: str, parent_id: str = None) -> Optional[str]:
        """
        根據標題查找 Notion 頁面
        
        Args:
            title: 頁面標題
            parent_id: 父頁面 ID（可選）
            
        Returns:
            找到的頁面 ID，未找到時返回 None
        """
        if not self.client:
            return None
        
        try:
            # 如果沒有指定父頁面，使用預設的資料庫 ID
            if not parent_id:
                parent_id = os.getenv('NOTION_DATABASE_ID')
                if not parent_id:
                    return None
            
            # 查詢頁面
            response = self.client.databases.query(
                database_id=parent_id,
                filter={
                    "property": "title",
                    "title": {"equals": title}
                }
            )
            
            if response["results"]:
                page_id = response["results"][0]["id"]
                print(f"✅ 找到 Notion 頁面: {title} (ID: {page_id})")
                return page_id
            else:
                print(f"⚠️ 未找到標題為 '{title}' 的 Notion 頁面")
                return None
                
        except Exception as e:
            print(f"❌ 查找 Notion 頁面時發生錯誤: {e}")
            return None
