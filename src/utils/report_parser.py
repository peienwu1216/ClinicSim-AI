"""
報告解析工具
"""

import re
from typing import Dict, List, Any, Optional
from pathlib import Path


class ReportParser:
    """報告內容解析器"""
    
    @staticmethod
    def parse_markdown_report(report_path: str) -> Dict[str, Any]:
        """解析 Markdown 格式的報告檔案"""
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parser = ReportParser()
            return parser._parse_content(content)
            
        except Exception as e:
            raise ValueError(f"解析報告檔案失敗: {str(e)}")
    
    def _parse_content(self, content: str) -> Dict[str, Any]:
        """解析報告內容"""
        parsed = {
            'metadata': self._extract_metadata(content),
            'scores': self._extract_scores(content),
            'suggestions': self._extract_suggestions(content),
            'citations': self._extract_citations(content),
            'rag_queries': self._extract_rag_queries(content),
            'full_content': content
        }
        
        return parsed
    
    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """提取報告元資料"""
        metadata = {}
        
        patterns = {
            'case_id': r'案例 ID\*\*: (.+)',
            'report_type': r'報告類型\*\*: (.+)',
            'generated_time': r'生成時間\*\*: (.+)',
            'coverage': r'問診覆蓋率\*\*: (.+)',
            'message_count': r'對話長度\*\*: (.+)',
            'citation_count': r'引註數量\*\*: (.+)',
            'rag_queries_text': r'RAG 查詢\*\*: (.+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            metadata[key] = match.group(1).strip() if match else ""
        
        return metadata
    
    def _extract_scores(self, content: str) -> Dict[str, float]:
        """提取評分資訊"""
        scores = {}
        
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
        
        # 提取改進建議段落
        improvement_match = re.search(
            r'\*\*4\. 改進建議\*\*\n\n(.*?)\n\n\*\*5\.', 
            content, 
            re.DOTALL
        )
        if improvement_match:
            suggestions['improvement'] = improvement_match.group(1).strip()
        
        # 提取總結建議段落
        summary_match = re.search(
            r'\*\*建議\*\*\n\n(.*?)\n\n總結', 
            content, 
            re.DOTALL
        )
        if summary_match:
            suggestions['summary'] = summary_match.group(1).strip()
        
        # 提取評分總結段落
        score_summary_match = re.search(
            r'\*\*5\. 評分總結\*\*\n\n(.*?)\n\n\*\*建議\*\*', 
            content, 
            re.DOTALL
        )
        if score_summary_match:
            suggestions['score_summary'] = score_summary_match.group(1).strip()
        
        return suggestions
    
    def _extract_citations(self, content: str) -> List[Dict[str, str]]:
        """提取引註資訊"""
        citations = []
        
        # 尋找詳細引註區段
        citations_section = re.search(
            r'## 詳細引註\n\n(.*?)\n\n---', 
            content, 
            re.DOTALL
        )
        
        if not citations_section:
            return citations
        
        citations_text = citations_section.group(1)
        
        # 分割每個引註
        citation_blocks = re.split(r'\n\n### 引註 \d+', citations_text)
        
        for i, block in enumerate(citation_blocks[1:], 1):  # 跳過第一個空塊
            citation = self._parse_single_citation(block, i)
            if citation:
                citations.append(citation)
        
        return citations
    
    def _parse_single_citation(self, block: str, citation_id: int) -> Optional[Dict[str, str]]:
        """解析單個引註"""
        try:
            # 提取查詢
            query_match = re.search(r'- \*\*查詢\*\*: (.+)', block)
            query = query_match.group(1) if query_match else ""
            
            # 提取來源
            source_match = re.search(r'- \*\*來源\*\*: (.+)', block)
            source = source_match.group(1) if source_match else ""
            
            # 提取內容
            content_match = re.search(r'- \*\*內容\*\*: \n```(.*?)```', block, re.DOTALL)
            content = content_match.group(1).strip() if content_match else ""
            
            return {
                'id': citation_id,
                'query': query,
                'source': source,
                'content': content
            }
            
        except Exception:
            return None
    
    def _extract_rag_queries(self, content: str) -> List[str]:
        """提取 RAG 查詢列表"""
        rag_queries_text = self._extract_metadata(content).get('rag_queries_text', '')
        
        if not rag_queries_text:
            return []
        
        # 分割查詢字符串
        queries = [q.strip() for q in rag_queries_text.split(',')]
        return [q for q in queries if q]
    
    @staticmethod
    def extract_case_data_from_filename(filename: str) -> Dict[str, str]:
        """從檔案名稱提取案例資訊"""
        # 檔案格式: case_chest_pain_acs_01_detailed_20250920_171121.md
        parts = filename.replace('.md', '').split('_')
        
        if len(parts) >= 4:
            case_id = '_'.join(parts[:-3])  # 案例ID部分
            report_type = parts[-3]  # 報告類型
            date_part = parts[-2]  # 日期
            time_part = parts[-1]  # 時間
            
            return {
                'case_id': case_id,
                'report_type': report_type,
                'date': date_part,
                'time': time_part,
                'filename': filename
            }
        
        return {'filename': filename}
