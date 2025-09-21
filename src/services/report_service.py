"""
報告生成服務
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from ..models.conversation import Conversation, MessageRole
from ..models.case import Case
from ..models.report import Report, ReportType, Citation
from ..services.ai_service import get_ai_service
from ..services.rag_service import RAGService
from ..services.case_service import CaseService
from ..services.scoring_service import ScoringService
from ..services.notion_service import NotionService
from ..services.map_reduce_service import MapReduceService
from ..config.settings import get_settings
from ..utils.file_utils import save_report_to_file, generate_report_filename


class ReportService:
    """報告生成服務"""
    
    def __init__(self, settings=None, case_service=None, ai_service=None, rag_service=None, scoring_service=None, notion_service=None, map_reduce_service=None):
        self.settings = settings or get_settings()
        self.case_service = case_service or CaseService(self.settings)
        self.ai_service = ai_service or get_ai_service(self.settings)
        self.rag_service = rag_service or RAGService(self.settings)
        self.scoring_service = scoring_service or ScoringService(self.settings)
        self.notion_service = notion_service or NotionService(self.settings)
        self.map_reduce_service = map_reduce_service or MapReduceService(self.settings, self.ai_service)
    
    def generate_feedback_report(self, conversation: Conversation) -> Report:
        """生成即時回饋報告"""
        case = self.case_service.get_case(conversation.case_id)
        if not case:
            raise ValueError(f"Case not found: {conversation.case_id}")
        
        # 確保覆蓋率是最新的
        from ..services.conversation_service import ConversationService
        conversation_service = ConversationService(self.settings)
        conversation_service._update_conversation_metrics(conversation, case)
        
        # 使用新的結構化評分系統
        try:
            scoring_result = self.scoring_service.score_conversation(conversation)
            # 生成基本分析報告（包含新評分）
            report_content = self._generate_enhanced_analysis(conversation, case, scoring_result)
        except Exception as e:
            print(f"[ERROR] 評分系統錯誤，使用基本分析: {e}")
            # 如果評分系統出錯，使用基本分析
            report_content = self._generate_basic_analysis(conversation, case)
        
        # 即時回饋報告不包含 RAG 文獻摘要，保持簡潔
        
        report = Report(
            report_type=ReportType.FEEDBACK,
            content=report_content,
            case_id=conversation.case_id,
            coverage=conversation.coverage,
            metadata={
                "generated_at": datetime.now().isoformat(),
                "conversation_length": len(conversation.messages)
            }
        )
        
        conversation.mark_report_generated()
        
        # 儲存報告到檔案
        self._save_report_to_file(report)
        
        return report
    
    def generate_detailed_report(self, conversation: Conversation) -> Report:
        """生成詳細分析報告（使用 LLM + RAG）"""
        case = self.case_service.get_case(conversation.case_id)
        if not case:
            raise ValueError(f"Case not found: {conversation.case_id}")
        
        # 先生成初步分析報告
        initial_feedback = self._generate_basic_analysis(conversation, case)
        
        # 基於初步回饋內容生成更精準的 RAG 查詢
        rag_queries = self._generate_queries_from_feedback(initial_feedback)
        
        citations = []
        if self.rag_service.is_available():
            # 使用新的 search_with_citations 方法生成帶有完整來源資訊的引註
            citations = self.rag_service.search_with_citations(rag_queries, k=2)
        
        # 生成詳細報告內容
        report_content = self._generate_detailed_analysis_with_llm(
            conversation, case, citations
        )
        
        report = Report(
            report_type=ReportType.DETAILED,
            content=report_content,
            case_id=conversation.case_id,
            citations=citations,
            rag_queries=rag_queries,
            coverage=conversation.coverage,
            metadata={
                "generated_at": datetime.now().isoformat(),
                "conversation_length": len(conversation.messages),
                "rag_available": self.rag_service.is_available(),
                "citations_count": len(citations)
            }
        )
        
        conversation.mark_detailed_report_generated()
        
        # 儲存報告到檔案
        file_path = self._save_report_to_file(report)
        
        # 將檔案路徑添加到報告元資料
        if file_path:
            report.metadata['file_path'] = file_path
            report.metadata['filename'] = Path(file_path).name
        
        return report
    
    def _generate_basic_analysis(self, conversation: Conversation, case: Case) -> str:
        """生成基本分析報告（不使用 LLM）"""
        checklist = case.get_feedback_checklist()
        critical_actions = case.get_critical_actions()
        user_messages = conversation.get_user_messages()
        
        # 創建對話文字內容用於關鍵字匹配
        conversation_text = " ".join([msg.content for msg in user_messages if hasattr(msg, 'content')])
        
        # 使用對話服務中已經計算好的覆蓋項目
        covered_items = set(conversation.covered_items)
        partially_covered_items = set(conversation.partially_covered_items)
        
        report_items = []
        covered_count = len(covered_items)
        partial_count = len(partially_covered_items)
        
        for item in checklist:
            item_id = item.get('id', '')
            item_point = item.get('point', '')
            
            if item_id in covered_items:
                report_items.append(f"- ✅ {item_point}：學生已完整詢問此項目")
            elif item_id in partially_covered_items:
                report_items.append(f"- ⚠️ {item_point}：學生有相關提問，但可更深入")
            else:
                report_items.append(f"- ❌ {item_point}：學生未詢問此項目")
        
        # 分析關鍵行動
        critical_analysis = []
        for action in critical_actions:
            # 針對不同的關鍵行動使用不同的關鍵字匹配
            if "ECG" in action or "心電圖" in action:
                # ECG相關行動的關鍵字
                ecg_keywords = ["心電圖", "ECG", "12導程", "12導", "立刻", "馬上", "立即", "10分", "十分"]
                if any(keyword in conversation_text for keyword in ecg_keywords):
                    critical_analysis.append(f"- ✅ 關鍵決策：學生提及了「{action}」")
                else:
                    critical_analysis.append(f"- ❌ 關鍵決策：學生未提及「{action}」")
            elif "Troponin" in action or "心肌鈣蛋白" in action:
                # Troponin相關行動的關鍵字
                troponin_keywords = ["troponin", "心肌鈣蛋白", "心肌酵素", "抽血", "檢驗", "血液"]
                if any(keyword in conversation_text for keyword in troponin_keywords):
                    critical_analysis.append(f"- ✅ 關鍵決策：學生提及了「{action}」")
                else:
                    critical_analysis.append(f"- ❌ 關鍵決策：學生未提及「{action}」")
            else:
                # 其他關鍵行動的通用匹配
                if any(keyword in conversation_text for keyword in ["心電圖", "ECG", "12導程", "立刻", "馬上", "10分"]):
                    critical_analysis.append(f"- ✅ 關鍵決策：學生提及了「{action}」")
                else:
                    critical_analysis.append(f"- ❌ 關鍵決策：學生未提及「{action}」")
        
        coverage_percentage = conversation.coverage
        
        return f"""### 診後分析報告

**問診覆蓋率：{coverage_percentage}% ({covered_count + partial_count}/{len(checklist)})**
**完整項目：{covered_count} | 部分項目：{partial_count} | 未覆蓋：{len(checklist) - covered_count - partial_count}**

**詳細評估：**
{chr(10).join(report_items)}

**關鍵行動評估：**
{chr(10).join(critical_analysis)}

### 總結與建議

**優點：**
- 問診覆蓋率達 {coverage_percentage}%，共覆蓋 {covered_count + partial_count} 個項目
- 學生展現了基本的問診技巧
- 能夠與病人建立良好的溝通

**改進建議：**
1. **系統性問診**：建議按照 OPQRST 結構進行問診
2. **深入探索**：對於已觸及的主題，可以進一步深入詢問
3. **關鍵決策**：加強臨床決策能力，及時提出關鍵檢查
4. **完整性**：注意問診的全面性，避免遺漏重要項目

**具體建議：**
- 多練習標準化問診流程
- 加強對關鍵症狀的識別能力
- 提升臨床決策的時效性

*註：此為即時分析報告，詳細報告請點擊「生成完整報告」按鈕。*"""
    
    def _generate_detailed_analysis_with_llm(self, conversation: Conversation, case: Case, citations: List[Citation]) -> str:
        """使用 Map-Reduce 策略生成詳細分析報告（優化 NPU 使用）"""
        print("[Map-Reduce] 開始使用 Map-Reduce 策略生成報告...")
        
        # 估算上下文大小
        context_size = self.map_reduce_service.estimate_context_size(conversation, citations)
        print(f"[Map-Reduce] 上下文大小分析: {context_size}")
        
        # 使用 Map-Reduce 服務處理大上下文
        condensed_context = self.map_reduce_service.process_large_context(conversation, citations)
        
        # 構建最終的詳細提示詞
        conversation_text = conversation.get_conversation_text()
        checklist = case.get_feedback_checklist()
        critical_actions = case.get_critical_actions()
        
        final_prompt = f"""
你是一位資深的 OSCE 臨床教師和心臟科專家。請根據以下資訊生成一份詳細的診後分析報告。

### 學生問診表現
{conversation_text}

### 評估標準
**檢查清單：**
{chr(10).join([f"- {item['point']} (類別: {item['category']})" for item in checklist])}

**關鍵行動：**
{chr(10).join([f"- {action}" for action in critical_actions])}

### 相關臨床指引摘要 (已濃縮)
{condensed_context}

### 你的任務
請生成一份專業、詳細的分析報告，包含以下部分：

## 1. 問診表現評估
- 系統性分析學生的問診技巧
- 指出優點和不足之處
- 引用具體的對話內容作為依據

## 2. 臨床決策分析
- 評估學生的臨床思維過程
- 分析是否識別出關鍵症狀和危險因子
- 評估決策的時效性和準確性

## 3. 知識應用評估
- 評估學生對急性胸痛診斷流程的理解
- 分析是否遵循標準化問診程序
- 評估對關鍵檢查的認知

## 4. 改進建議
- 基於臨床指引摘要，給出具體建議
- 提供實用的學習資源和練習方向
- 建議下一步的學習重點

## 5. 評分總結
- 給出各項目的具體評分 (1-10分)
- 提供總體評價和等級
- 建議是否需要額外練習

### 重要要求：
1. **必須使用繁體中文撰寫整份報告，絕對不能使用簡體中文**
2. **禁止在報告中包含任何簽名欄位，如：[學生姓名]、[日期]、[評估者姓名]、[評估者簽名]等**
3. **報告內容應直接開始，不需要任何表單欄位或簽名區域**
4. 語氣專業但友善，適合醫學生學習使用
5. 確保所有醫學術語使用正確的繁體中文
6. 報告應結構清晰，易於閱讀
7. 直接提供分析內容，不要包含任何需要填寫的空白欄位
"""
        
        # 構建最終訊息
        from ..models.conversation import Message
        messages = [Message(role=MessageRole.SYSTEM, content=final_prompt)]
        
        try:
            print("[Map-Reduce] 正在生成最終報告（應該在 NPU 上運行）...")
            # 這個最終任務現在應該能在 NPU 上運行，因為上下文已經被大幅縮減
            report_content = self.ai_service.chat(messages)
            print("[Map-Reduce] 報告生成完成")
            
            # 添加 Map-Reduce 處理的元數據
            if isinstance(report_content, str):
                report_content += f"\n\n---\n*此報告使用 Map-Reduce 策略生成，優化了 NPU 使用效率*"
            
            return report_content
            
        except Exception as e:
            print(f"[Map-Reduce] 最終報告生成失敗: {e}")
            # 備用方案：使用基本分析 + 濃縮內容
            basic_analysis = self._generate_basic_analysis(conversation, case)
            return f"""
# 詳細診後分析報告

{basic_analysis}

---

## 臨床指引摘要

{condensed_context}

---

*註：此為備用詳細報告，使用 Map-Reduce 策略處理。AI 服務暫時無法使用。*
            """
    
    def _append_citation_suggestions(self, citations: List[Citation]) -> str:
        """在報告末尾添加基於引註的建議"""
        suggestions = "\n\n## 基於臨床指引的建議\n\n"
        
        for citation in citations:
            suggestions += f"**根據 [引註 {citation.id}] 的指引：**\n"
            
            content = citation.content
            if 'ECG' in content or '心電圖' in content:
                suggestions += "- ECG 心電圖檢查應在 10 分鐘內完成，這是急性胸痛評估的第一優先檢查\n"
            if 'STEMI' in content:
                suggestions += "- 疑似 STEMI 時應立即啟動心導管團隊，時間就是心肌\n"
            if 'OPQRST' in content:
                suggestions += "- 問診應遵循 OPQRST 結構：發作時間、誘發因子、疼痛性質、放射位置、嚴重程度、持續時間\n"
            
            suggestions += "\n"
        
        return suggestions
    
    def _generate_queries_from_feedback(self, feedback_content: str) -> List[str]:
        """基於AI回饋內容生成相關的RAG查詢"""
        queries = []
        content_lower = feedback_content.lower()
        
        # 根據回饋內容中的關鍵詞生成查詢
        if any(keyword in content_lower for keyword in ["問診", "病史", "osce", "覆蓋率"]):
            queries.append("OSCE 問診技巧和病史詢問指南")
            
        if any(keyword in content_lower for keyword in ["ecg", "心電圖", "12導程", "關鍵決策"]):
            queries.append("ECG 心電圖在胸痛評估中的重要性")
            
        if any(keyword in content_lower for keyword in ["鑑別", "診斷", "檢查", "stemi"]):
            queries.append("STEMI 和不穩定型心絞痛的診斷標準")
            queries.append("急性胸痛的鑑別診斷和檢查項目")
            
        if any(keyword in content_lower for keyword in ["opqrst", "疼痛", "性質", "位置", "放射"]):
            queries.append("胸痛問診的 OPQRST 技巧和重點")
            
        if any(keyword in content_lower for keyword in ["系統性", "流程", "順序"]):
            queries.append("急性胸痛診斷流程和檢查順序")
            
        if any(keyword in content_lower for keyword in ["改進", "建議", "練習"]):
            queries.append("臨床診斷技巧和最佳實踐")
            
        # 如果沒有找到特定關鍵詞，使用通用查詢
        if not queries:
            queries = [
                "急性胸痛診斷流程和檢查順序",
                "ECG 心電圖在胸痛評估中的重要性"
            ]
            
        return queries[:3]  # 返回最多3個查詢
    
    def _search_multiple_queries(self, queries: List[str], k: int = 2) -> str:
        """執行多個查詢並合併結果"""
        all_results = []
        
        for i, query in enumerate(queries, 1):
            try:
                result = self.rag_service.search(query, k=k)
                if result and "RAG 系統未初始化" not in result and "找不到相關資料" not in result:
                    # 添加查詢標識
                    formatted_result = f"📚 **{query}**\n\n{result}"
                    all_results.append(formatted_result)
            except Exception as e:
                print(f"查詢失敗: {query} - {e}")
                continue
                
        # 合併結果，避免重複
        if all_results:
            return "\n\n---\n\n".join(all_results[:2])  # 最多返回2個結果
        else:
            return ""
    
    def _save_report_to_file(self, report: Report) -> Optional[str]:
        """將報告儲存到本地 md 檔案"""
        try:
            # 生成檔案名稱
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = generate_report_filename(
                case_id=report.case_id,
                report_type=report.report_type.value,
                timestamp=timestamp
            )
            
            # 構建完整的報告內容（包含 metadata）
            full_report_content = self._format_report_for_file(report)
            
            # 儲存到檔案
            file_path = save_report_to_file(
                report_content=full_report_content,
                filename=filename,
                directory_path=self.settings.report_history_dir
            )
            
            if file_path:
                print(f"報告已儲存至: {file_path}")
                return str(file_path)
            else:
                print("報告儲存失敗")
                return None
                
        except Exception as e:
            print(f"儲存報告時發生錯誤: {e}")
            return None
    
    def _format_report_for_file(self, report: Report) -> str:
        """格式化報告內容用於檔案儲存"""
        # 報告標題
        report_title = "即時回饋報告" if report.report_type == ReportType.FEEDBACK else "詳細分析報告"
        
        # 基本資訊
        metadata_section = f"""# {report_title}

## 報告資訊
- **案例 ID**: {report.case_id}
- **報告類型**: {report.report_type.value}
- **生成時間**: {report.metadata.get('generated_at', 'N/A')}
- **問診覆蓋率**: {report.coverage}%
- **對話長度**: {report.metadata.get('conversation_length', 'N/A')} 條訊息

"""
        
        # 如果有引註，添加引註資訊
        citations_section = ""
        if report.citations:
            citations_section = f"""
## 引註資訊
- **引註數量**: {len(report.citations)}
- **RAG 查詢**: {', '.join(report.rag_queries) if report.rag_queries else 'N/A'}

"""
        
        # 報告內容
        content_section = f"""
## 報告內容

{report.content}
"""
        
        # 如果有引註，添加詳細引註
        detailed_citations = ""
        if report.citations:
            detailed_citations = f"""

## 詳細引註

"""
            for i, citation in enumerate(report.citations, 1):
                score_info = ""
                if hasattr(citation, 'score') and citation.score is not None:
                    score_info = f"- **相關性分數**: {citation.score:.3f}\n"
                
                detailed_citations += f"""### 引註 {citation.id}
- **查詢**: {citation.query}
- **來源**: {citation.source}
{score_info}- **內容**: 
```
{citation.content}
```

---
"""
        
        # 組合完整內容
        full_content = (
            metadata_section +
            citations_section +
            content_section +
            detailed_citations +
            f"""

---
*此報告由 ClinicSim-AI 系統自動生成於 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        )
        
        return full_content
    
    def _generate_enhanced_analysis(self, conversation: Conversation, case: Case, scoring_result) -> str:
        """生成增強分析報告（包含結構化評分）"""
        # 基本覆蓋率分析（保持向後兼容）
        checklist = case.get_feedback_checklist()
        conversation_text = conversation.get_conversation_text().lower()
        
        report_items = []
        covered_count = 0
        partial_count = 0
        
        for item in checklist:
            keywords = item.get('keywords', [])
            matched_keywords = [kw for kw in keywords if kw.lower() in conversation_text]
            
            if len(matched_keywords) >= 2:
                report_items.append(f"- ✅ {item['point']}：學生透過提問「{matched_keywords[0]}」等成功問診")
                covered_count += 1
            elif len(matched_keywords) == 1:
                report_items.append(f"- ⚠️ {item['point']}：學生有相關提問「{matched_keywords[0]}」，但可更深入")
                partial_count += 1
            else:
                report_items.append(f"- ❌ {item['point']}：學生未詢問此項目")
        
        # 結構化評分分析
        scoring_analysis = self._format_scoring_analysis(scoring_result)
        
        coverage_percentage = conversation.coverage
        
        return f"""### 診後分析報告

**總體評分：{scoring_result.percentage:.1f}% ({scoring_result.grade})**
**問診覆蓋率：{coverage_percentage}% ({covered_count + partial_count}/{len(checklist)})**

{scoring_analysis}

**詳細評估：**
{chr(10).join(report_items)}

### 總結與建議

**優點：**
- 總體評分達 {scoring_result.percentage:.1f}%，等級：{scoring_result.grade}
- 問診覆蓋率達 {coverage_percentage}%，共覆蓋 {covered_count + partial_count} 個項目
- 學生展現了基本的問診技巧

**改進建議：**
1. **系統性問診**：建議按照 OPQRST 結構進行問診
2. **深入探索**：對於已觸及的主題，可以進一步深入詢問
3. **關鍵決策**：加強臨床決策能力，及時提出關鍵檢查
4. **完整性**：注意問診的全面性，避免遺漏重要項目

**具體建議：**
- 多練習標準化問診流程
- 加強對關鍵症狀的識別能力
- 提升臨床決策的時效性

*註：此為即時分析報告，詳細報告請點擊「生成完整報告」按鈕。*"""
    
    def _format_scoring_analysis(self, scoring_result) -> str:
        """格式化評分分析 - 改進的顯示邏輯"""
        analysis_parts = []
        
        # 各類別評分
        for section in scoring_result.section_scores:
            section_percentage = (section.achieved_score / section.max_score * 100) if section.max_score > 0 else 0
            analysis_parts.append(f"**{section.title}**: {section_percentage:.1f}% ({section.achieved_score:.1f}/{section.max_score})")
            
            # 顯示所有評分項目的詳細狀態
            for criterion in section.criteria_scores:
                # 改進的顯示邏輯：根據分數比例決定顯示狀態
                score_ratio = criterion.achieved_score / criterion.max_score if criterion.max_score > 0 else 0
                
                if score_ratio >= 0.8:
                    status_icon = "✅"  # 80%以上為綠色勾勾
                    status_text = "優秀"
                elif score_ratio >= 0.5:
                    status_icon = "⚠️"  # 50-80%為黃色警告
                    status_text = "良好"
                elif score_ratio > 0:
                    status_icon = "🟡"  # 1-50%為黃色圓點
                    status_text = "部分完成"
                else:
                    status_icon = "❌"  # 0分為紅色叉叉
                    status_text = "未完成"
                
                analysis_parts.append(f"  - {status_icon} {criterion.description} ({status_text})")
            
            # 顯示懲罰項目
            penalties = [p for p in section.penalties if p.achieved_score > 0]
            if penalties:
                analysis_parts.append(f"  - 扣分項目: {', '.join([p.description for p in penalties])}")
        
        return "\n".join(analysis_parts)
    
    def sync_existing_report_to_notion(self, file_path: str, page_title: str = None) -> Optional[str]:
        """
        將現有的報告檔案同步到 Notion
        
        Args:
            file_path: 報告檔案路徑
            page_title: Notion 頁面標題（可選）
            
        Returns:
            創建的頁面 ID，失敗時返回 None
        """
        if not self.notion_service.is_available():
            print("❌ Notion 服務不可用")
            return None
        
        try:
            # 如果沒有提供標題，從檔案名生成
            if not page_title:
                file_path_obj = Path(file_path)
                page_title = f"學習報告 - {file_path_obj.stem}"
            
            # 使用 NotionService 同步報告
            page_id = self.notion_service.sync_report_to_notion(
                report_file_path=file_path,
                page_title=page_title
            )
            
            if page_id:
                print(f"✅ 成功同步報告到 Notion: {page_title}")
                return page_id
            else:
                print(f"❌ 同步報告到 Notion 失敗: {page_title}")
                return None
                
        except Exception as e:
            print(f"❌ 同步現有報告到 Notion 時發生錯誤: {e}")
            return None
