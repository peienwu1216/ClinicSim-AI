"""
Map-Reduce 服務 - 優化大上下文處理，確保 NPU 高效使用
"""

from typing import List, Dict, Any, Optional
from ..models.conversation import Conversation, Message, MessageRole
from ..models.report import Citation
from ..services.ai_service import get_ai_service
from ..config.settings import get_settings
from ..config.npu_optimization import get_npu_config, estimate_processing_time


class MapReduceService:
    """Map-Reduce 服務，用於優化大上下文處理"""
    
    def __init__(self, settings=None, ai_service=None, npu_config=None):
        self.settings = settings or get_settings()
        self.ai_service = ai_service or get_ai_service(self.settings)
        self.npu_config = npu_config or get_npu_config("balanced")
        self.max_context_length = self.npu_config.max_context_length
        self.batch_size = self.npu_config.batch_size
    
    def process_large_context(self, conversation: Conversation, citations: List[Citation]) -> str:
        """
        使用 Map-Reduce 策略處理大上下文
        
        Args:
            conversation: 對話對象
            citations: 引註列表
            
        Returns:
            處理後的濃縮內容
        """
        print("[Map-Reduce] 開始處理大上下文...")
        
        # 第一步：Map 階段 - 濃縮文檔片段
        summaries = self._map_phase(conversation, citations)
        
        # 第二步：Reduce 階段 - 合併摘要
        final_summary = self._reduce_phase(summaries)
        
        print(f"[Map-Reduce] 處理完成，原始文檔: {len(citations)}, 濃縮後長度: {len(final_summary)}")
        return final_summary
    
    def _map_phase(self, conversation: Conversation, citations: List[Citation]) -> List[str]:
        """Map 階段：將文檔片段分批濃縮"""
        if not citations:
            print("[Map-Reduce] 沒有文檔需要處理")
            return []
        
        summaries = []
        conversation_text = conversation.get_conversation_text()
        
        # 將 citations 分成小批次
        citation_batches = [
            citations[i:i + self.batch_size] 
            for i in range(0, len(citations), self.batch_size)
        ]
        
        print(f"[Map-Reduce] 將 {len(citations)} 個文檔分成 {len(citation_batches)} 個批次處理")
        
        for batch_idx, citation_batch in enumerate(citation_batches):
            print(f"[Map-Reduce] 處理批次 {batch_idx + 1}/{len(citation_batches)}")
            
            try:
                batch_summary = self._summarize_batch(conversation_text, citation_batch, batch_idx + 1)
                summaries.append(batch_summary)
                print(f"[Map-Reduce] 批次 {batch_idx + 1} 處理完成")
            except Exception as e:
                print(f"[Map-Reduce] 批次 {batch_idx + 1} 處理失敗: {e}")
                # 備用方案：使用簡化版本
                fallback = self._create_fallback_summary(citation_batch, batch_idx + 1)
                summaries.append(fallback)
        
        return summaries
    
    def _summarize_batch(self, conversation_text: str, citation_batch: List[Citation], batch_num: int) -> str:
        """濃縮單個批次的文檔"""
        # 限制對話歷史長度，避免上下文過大
        truncated_conversation = conversation_text[:self.max_context_length // 2]
        
        # 構建批次文檔內容
        batch_content = "\n\n".join([
            f"### 文檔 {citation.id}: {citation.query}\n{citation.content}"
            for citation in citation_batch
        ])
        
        # 創建濃縮提示詞（小任務，適合 NPU）
        summarize_prompt = f"""
你是一位臨床指引專家。請根據以下對話歷史，總結這些臨床指引文檔的核心觀點。

### 對話歷史摘要
{truncated_conversation}

### 臨床指引文檔
{batch_content}

### 任務
請用繁體中文總結這些文檔的核心觀點，重點關注：
1. 與胸痛診斷相關的關鍵指引
2. 問診技巧和檢查順序  
3. 臨床決策要點
4. 重要的檢查項目和時機

總結要求：
- 每個文檔的核心觀點控制在 100-150 字內
- 突出與當前對話最相關的內容
- 使用專業但易懂的醫學術語
- 保持結構清晰
- **必須使用繁體中文，絕對不能使用簡體中文**
- **禁止包含任何簽名欄位或表單元素**

請直接提供總結內容，不需要額外的格式說明。
"""
        
        # 使用 AI 服務進行濃縮（這個小任務應該能在 NPU 上運行）
        messages = [Message(role=MessageRole.SYSTEM, content=summarize_prompt)]
        summary = self.ai_service.chat(messages)
        
        return f"**批次 {batch_num} 臨床指引摘要：**\n{summary}"
    
    def _create_fallback_summary(self, citation_batch: List[Citation], batch_num: int) -> str:
        """創建備用摘要（當 AI 處理失敗時）"""
        fallback_items = []
        for citation in citation_batch:
            # 截取文檔的前 200 字作為摘要
            content_preview = citation.content[:200] + "..." if len(citation.content) > 200 else citation.content
            fallback_items.append(f"- **{citation.query}**: {content_preview}")
        
        return f"**批次 {batch_num} 文檔摘要：**\n" + "\n".join(fallback_items)
    
    def _reduce_phase(self, summaries: List[str]) -> str:
        """Reduce 階段：合併所有摘要"""
        if not summaries:
            return "未找到相關臨床指引"
        
        if len(summaries) == 1:
            return summaries[0]
        
        # 如果有多個摘要，可以選擇直接合併或進一步濃縮
        # 這裡選擇直接合併，因為已經是小任務了
        combined_summary = "\n\n".join(summaries)
        
        # 如果合併後的內容仍然很長，可以進一步濃縮
        if len(combined_summary) > self.max_context_length:
            print("[Map-Reduce] 合併後內容過長，進行二次濃縮...")
            return self._further_condense(combined_summary)
        
        return combined_summary
    
    def _further_condense(self, content: str) -> str:
        """進一步濃縮內容"""
        condense_prompt = f"""
你是一位臨床指引專家。請將以下臨床指引摘要進一步濃縮，保留最核心的內容。

### 原始摘要
{content}

### 任務
請用繁體中文創建一個簡潔的臨床指引摘要，要求：
1. 保留與胸痛診斷最相關的關鍵點
2. 突出重要的檢查順序和時機
3. 總長度控制在 500 字以內
4. 保持結構清晰，易於閱讀
5. **必須使用繁體中文，絕對不能使用簡體中文**
6. **禁止包含任何簽名欄位或表單元素**

請直接提供濃縮後的摘要，不需要額外的格式說明。
"""
        
        try:
            messages = [Message(role=MessageRole.SYSTEM, content=condense_prompt)]
            condensed = self.ai_service.chat(messages)
            return f"**臨床指引摘要（已濃縮）：**\n{condensed}"
        except Exception as e:
            print(f"[Map-Reduce] 二次濃縮失敗: {e}")
            # 備用方案：簡單截取
            return f"**臨床指引摘要：**\n{content[:500]}..."
    
    def estimate_context_size(self, conversation: Conversation, citations: List[Citation]) -> Dict[str, Any]:
        """估算上下文大小和處理策略"""
        conversation_length = len(conversation.get_conversation_text())
        citations_length = sum(len(citation.content) for citation in citations)
        total_length = conversation_length + citations_length
        
        # 使用 NPU 配置獲取優化策略
        strategy = self.npu_config.get_optimization_strategy(total_length)
        time_estimate = estimate_processing_time(total_length, len(citations), self.npu_config)
        
        return {
            "conversation_length": conversation_length,
            "citations_length": citations_length,
            "total_length": total_length,
            "estimated_tokens": total_length // 4,  # 粗略估算：4個字符約等於1個token
            "needs_map_reduce": strategy["needs_map_reduce"],
            "strategy": strategy["strategy"],
            "description": strategy["description"],
            "estimated_batches": strategy["estimated_batches"],
            "time_estimate": time_estimate,
            "should_use_npu": self.npu_config.should_use_npu(total_length)
        }
    
    def get_processing_strategy(self, context_size: Dict[str, Any]) -> str:
        """根據上下文大小推薦處理策略"""
        return context_size.get("description", "未知策略")
