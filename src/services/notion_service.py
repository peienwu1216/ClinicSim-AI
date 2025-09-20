"""
Notion API 整合服務
"""

import requests
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

from ..config.settings import get_settings
from ..exceptions.notion_exceptions import NotionAPIError, NotionAuthError, NotionDatabaseError


class NotionService:
    """Notion API 整合服務"""
    
    def __init__(self, settings=None):
        self.settings = settings or get_settings()
        self.api_base_url = "https://api.notion.com/v1"
        self.api_key = getattr(self.settings, 'notion_api_key', None)
        self.database_id = getattr(self.settings, 'notion_database_id', None)
        
        # API 請求標頭
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def is_configured(self) -> bool:
        """檢查是否已配置 Notion API"""
        return bool(self.api_key and self.database_id)
    
    def test_connection(self) -> Tuple[bool, str]:
        """測試 Notion API 連線"""
        if not self.is_configured():
            return False, "Notion API 未配置，請先設定 API Key 和 Database ID"
        
        try:
            # 測試 API Key 有效性
            response = requests.get(
                f"{self.api_base_url}/users/me",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 401:
                return False, "Notion API Key 無效，請檢查設定"
            elif response.status_code == 200:
                # 測試 Database 存取權限
                db_response = requests.get(
                    f"{self.api_base_url}/databases/{self.database_id}",
                    headers=self.headers,
                    timeout=10
                )
                
                if db_response.status_code == 404:
                    return False, "Notion Database 不存在或無存取權限"
                elif db_response.status_code == 200:
                    return True, "連線成功"
                else:
                    return False, f"Database 存取錯誤: {db_response.status_code}"
            else:
                return False, f"API 連線錯誤: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"網路連線錯誤: {str(e)}"
    
    def create_learning_record(self, report_path: str, case_data: Dict[str, Any]) -> Tuple[bool, str]:
        """創建學習記錄到 Notion Database"""
        try:
            # 解析報告內容
            parsed_report = self._parse_report_file(report_path)
            
            # 轉換為 Notion 格式
            notion_data = self._format_for_notion(parsed_report, case_data)
            
            # 發送到 Notion
            response = requests.post(
                f"{self.api_base_url}/pages",
                headers=self.headers,
                json=notion_data,
                timeout=30
            )
            
            if response.status_code == 200:
                page_data = response.json()
                page_url = page_data.get('url', '')
                return True, f"學習記錄已成功創建到 Notion！\n頁面連結: {page_url}"
            else:
                error_msg = response.json().get('message', '未知錯誤')
                return False, f"創建失敗: {error_msg}"
                
        except Exception as e:
            return False, f"處理報告時發生錯誤: {str(e)}"
    
    def _parse_report_file(self, report_path: str) -> Dict[str, Any]:
        """解析報告檔案內容"""
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取基本資訊
            parsed = {
                'case_id': self._extract_field(content, r'案例 ID\*\*: (.+)'),
                'report_type': self._extract_field(content, r'報告類型\*\*: (.+)'),
                'generated_time': self._extract_field(content, r'生成時間\*\*: (.+)'),
                'coverage': self._extract_field(content, r'問診覆蓋率\*\*: (.+)'),
                'message_count': self._extract_field(content, r'對話長度\*\*: (.+)'),
                'citation_count': self._extract_field(content, r'引註數量\*\*: (.+)'),
                'rag_queries': self._extract_field(content, r'RAG 查詢\*\*: (.+)'),
                'full_content': content
            }
            
            # 提取評分資訊
            scores = self._extract_scores(content)
            parsed.update(scores)
            
            # 提取建議內容
            suggestions = self._extract_suggestions(content)
            parsed.update(suggestions)
            
            return parsed
            
        except Exception as e:
            raise NotionAPIError(f"解析報告檔案失敗: {str(e)}")
    
    def _extract_field(self, content: str, pattern: str) -> str:
        """使用正則表達式提取欄位值"""
        match = re.search(pattern, content)
        return match.group(1).strip() if match else ""
    
    def _extract_scores(self, content: str) -> Dict[str, Any]:
        """提取評分資訊"""
        scores = {}
        
        # 提取各項評分
        score_patterns = {
            'interview_score': r'問診表現評估：(\d+(?:\.\d+)?)/10',
            'decision_score': r'臨床決策分析：(\d+(?:\.\d+)?)/10',
            'knowledge_score': r'知識應用評估：(\d+(?:\.\d+)?)/10',
            'total_score': r'總體評價為 (\d+(?:\.\d+)?)/10'
        }
        
        for key, pattern in score_patterns.items():
            match = re.search(pattern, content)
            if match:
                try:
                    scores[key] = float(match.group(1))
                except ValueError:
                    scores[key] = 0.0
            else:
                scores[key] = 0.0
        
        return scores
    
    def _extract_suggestions(self, content: str) -> Dict[str, str]:
        """提取學習建議"""
        suggestions = {}
        
        # 提取改進建議
        improvement_match = re.search(r'\*\*4\. 改進建議\*\*\n\n(.*?)\n\n\*\*5\.', content, re.DOTALL)
        if improvement_match:
            suggestions['improvement_suggestions'] = improvement_match.group(1).strip()
        
        # 提取總結建議
        summary_match = re.search(r'\*\*建議\*\*\n\n(.*?)\n\n總結', content, re.DOTALL)
        if summary_match:
            suggestions['summary_suggestions'] = summary_match.group(1).strip()
        
        return suggestions
    
    def _format_for_notion(self, parsed_report: Dict[str, Any], case_data: Dict[str, Any]) -> Dict[str, Any]:
        """將解析的報告資料轉換為 Notion API 格式"""
        
        # 構建 Notion 頁面資料
        notion_data = {
            "parent": {
                "database_id": self.database_id
            },
            "properties": {
                # 標題欄位
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": case_data.get('case_title', f"學習記錄 - {parsed_report['case_id']}")
                            }
                        }
                    ]
                },
                
                # 日期欄位
                "學習日期": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                },
                
                # 案例類型
                "案例類型": {
                    "select": {
                        "name": self._extract_case_type(case_data)
                    }
                },
                
                # 評分欄位
                "問診表現": {
                    "number": parsed_report.get('interview_score', 0)
                },
                
                "臨床決策": {
                    "number": parsed_report.get('decision_score', 0)
                },
                
                "知識應用": {
                    "number": parsed_report.get('knowledge_score', 0)
                },
                
                "總體評價": {
                    "number": parsed_report.get('total_score', 0)
                },
                
                # 複習狀態
                "複習狀態": {
                    "select": {
                        "name": "待複習"
                    }
                }
            },
            
            # 頁面內容
            "children": [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "📊 學習表現摘要"
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"問診覆蓋率: {parsed_report.get('coverage', 'N/A')}"
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"對話長度: {parsed_report.get('message_count', 'N/A')} 條訊息"
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"引註來源: {parsed_report.get('citation_count', 'N/A')} 個"
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        # 添加改進建議
        if parsed_report.get('improvement_suggestions'):
            notion_data["children"].extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "🎯 改進建議"
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": parsed_report['improvement_suggestions']
                                }
                            }
                        ]
                    }
                }
            ])
        
        # 添加完整報告內容（分段處理以避免長度限制）
        notion_data["children"].extend([
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "📋 完整學習報告"
                            }
                        }
                    ]
                }
            }
        ])
        
        # 將長內容分段處理
        full_content = parsed_report['full_content']
        content_chunks = self._split_content_by_length(full_content, 1800)  # 留一些緩衝
        
        for i, chunk in enumerate(content_chunks):
            notion_data["children"].append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": chunk
                            }
                        }
                    ]
                }
            })
        
        return notion_data
    
    def _split_content_by_length(self, content: str, max_length: int) -> List[str]:
        """將內容按長度分段，避免超出 Notion API 限制"""
        if len(content) <= max_length:
            return [content]
        
        chunks = []
        current_chunk = ""
        
        # 按段落分割
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs:
            # 如果單個段落就超過限制，需要進一步分割
            if len(paragraph) > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                
                # 按句子分割長段落
                sentences = paragraph.split('。')
                for sentence in sentences:
                    if len(current_chunk + sentence + '。') <= max_length:
                        current_chunk += sentence + '。'
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence + '。'
            else:
                # 檢查添加這個段落是否會超出限制
                if len(current_chunk + '\n\n' + paragraph) <= max_length:
                    if current_chunk:
                        current_chunk += '\n\n' + paragraph
                    else:
                        current_chunk = paragraph
                else:
                    # 保存當前塊並開始新塊
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph
        
        # 添加最後一塊
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _extract_case_type(self, case_data: Dict[str, Any]) -> str:
        """從案例資料中提取案例類型"""
        if not isinstance(case_data, dict):
            return '其他'
            
        station_info = case_data.get('station_info', {})
        station_type = station_info.get('type', '')
        
        if '內科' in station_type:
            return '內科'
        elif '外科' in station_type:
            return '外科'
        elif '急診' in station_type:
            return '急診'
        elif '兒科' in station_type:
            return '兒科'
        else:
            return '其他'
    
    def get_database_schema(self) -> Dict[str, Any]:
        """獲取 Database 結構資訊"""
        if not self.is_configured():
            return {}
        
        try:
            response = requests.get(
                f"{self.api_base_url}/databases/{self.database_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception:
            return {}
