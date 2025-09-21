"""
對話管理服務
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models.conversation import Conversation, Message, MessageRole, ConversationState
from ..models.case import Case
from ..models.vital_signs import VitalSigns
from ..services.ai_service import get_ai_service
from ..services.case_service import CaseService
from ..config.settings import get_settings


class ConversationService:
    """對話管理服務"""
    
    def __init__(self, settings=None, case_service=None, ai_service=None):
        self.settings = settings or get_settings()
        self.case_service = case_service or CaseService(self.settings)
        self.ai_service = ai_service or get_ai_service(self.settings)
        self._conversations: Dict[str, Conversation] = {}
    
    def create_conversation(self, case_id: str) -> tuple[Conversation, str]:
        """創建新對話"""
        conversation = Conversation(case_id=case_id)
        conversation_id = f"{case_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self._conversations[conversation_id] = conversation
        return conversation, conversation_id
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """取得對話"""
        return self._conversations.get(conversation_id)
    
    def add_message(self, conversation_id: str, role: MessageRole, content: str) -> Optional[Conversation]:
        """新增訊息到對話"""
        conversation = self._conversations.get(conversation_id)
        if not conversation:
            return None
        
        conversation.add_message(role, content)
        
        # 如果是用戶訊息，更新覆蓋率
        if role == MessageRole.USER:
            case = self.case_service.get_case(conversation.case_id)
            if case:
                self._update_conversation_metrics(conversation, case)
        
        return conversation
    
    def generate_ai_response(self, conversation_id: str) -> Optional[str]:
        """生成 AI 回應"""
        conversation = self._conversations.get(conversation_id)
        if not conversation:
            return None
        
        # 載入案例
        case = self.case_service.get_case(conversation.case_id)
        if not case:
            return "錯誤：找不到指定的案例檔案。"
        
        # 構建訊息列表
        messages = [Message(role=MessageRole.SYSTEM, content=case.get_system_prompt())]
        messages.extend(conversation.messages)
        
        # 生成回應
        try:
            response = self.ai_service.chat(messages)
            
            # 更新覆蓋率和生命體徵
            self._update_conversation_metrics(conversation, case)
            
            return response
        except Exception as e:
            return f"AI 服務錯誤：{str(e)}"
    
    def _update_conversation_metrics(self, conversation: Conversation, case: Case) -> None:
        """更新對話指標（覆蓋率、生命體徵等）"""
        # 計算覆蓋率
        coverage = self._calculate_coverage(conversation, case)
        conversation.coverage = coverage
        
        # 檢查是否需要更新生命體徵
        if self._should_update_vital_signs(conversation):
            conversation.vital_signs = self._generate_vital_signs(case)
    
    def _calculate_coverage(self, conversation: Conversation, case: Case) -> int:
        """計算問診覆蓋率（累加式）"""
        checklist = case.get_feedback_checklist()
        if not checklist:
            return 0
        
        # 取得最新的使用者訊息
        user_messages = conversation.get_user_messages()
        if not user_messages:
            return conversation.coverage
        
        # 只分析最新的使用者訊息
        latest_message = user_messages[-1].content.lower()
        
        # 檢查是否有新的覆蓋項目
        new_covered_items = []
        new_partially_covered_items = []
        
        for item in checklist:
            item_id = item.get('id', '')
            if not item_id:
                continue
            
            # 跳過已經完全覆蓋的項目
            if item_id in conversation.covered_items:
                continue
            
            keywords = item.get('keywords', [])
            # 如果沒有關鍵字，生成默認關鍵字
            if not keywords:
                keywords = self._generate_default_keywords(item_id, item.get('point', ''))
            
            matched_keywords = [kw for kw in keywords if kw.lower() in latest_message]
            
            # 完全覆蓋：匹配2個或以上關鍵字
            if len(matched_keywords) >= 2:
                new_covered_items.append(item_id)
            # 部分覆蓋：匹配1個關鍵字
            elif len(matched_keywords) == 1 and item_id not in conversation.partially_covered_items:
                new_partially_covered_items.append(item_id)
        
        # 更新對話的覆蓋項目（累加式）
        conversation.covered_items.extend(new_covered_items)
        conversation.partially_covered_items.extend(new_partially_covered_items)
        
        # 計算總覆蓋率：完全覆蓋項目 + 部分覆蓋項目
        # 使用 set 來避免重複計算
        unique_covered = len(set(conversation.covered_items))
        unique_partial = len(set(conversation.partially_covered_items))
        
        # 確保部分覆蓋的項目不會與完全覆蓋的項目重複
        partial_only = set(conversation.partially_covered_items) - set(conversation.covered_items)
        unique_partial = len(partial_only)
        
        total_covered = unique_covered + (unique_partial * 0.5)
        coverage_percentage = int((total_covered / len(checklist)) * 100) if checklist else 0
        
        # 更新對話的覆蓋率
        old_coverage = conversation.coverage
        conversation.coverage = min(coverage_percentage, 100)
        
        # 調試信息
        if new_covered_items or new_partially_covered_items or old_coverage != conversation.coverage:
            print(f"[DEBUG] 覆蓋率更新: {old_coverage}% -> {conversation.coverage}%")
            print(f"[DEBUG] 新增完全覆蓋項目: {new_covered_items}")
            print(f"[DEBUG] 新增部分覆蓋項目: {new_partially_covered_items}")
            print(f"[DEBUG] 計算詳情:")
            print(f"  - 總檢查清單項目: {len(checklist)}")
            print(f"  - 完全覆蓋項目數: {unique_covered}")
            print(f"  - 部分覆蓋項目數: {unique_partial}")
            print(f"  - 總覆蓋分數: {total_covered}")
            print(f"  - 覆蓋率計算: ({total_covered} / {len(checklist)}) * 100 = {coverage_percentage}%")
        
        return conversation.coverage
    
    def _generate_default_keywords(self, item_id: str, point: str) -> List[str]:
        """為檢查清單項目生成默認關鍵字"""
        keyword_mapping = {
            "intro": ["你好", "我是", "醫生", "同意", "可以嗎", "確認"],
            "site": ["哪裡", "位置", "部位", "痛"],
            "onset": ["什麼時候", "開始", "發作", "突然"],
            "provocation": ["誘發", "緩解", "什麼會", "活動", "休息"],
            "quality": ["什麼樣", "性質", "壓", "悶", "刺痛"],
            "radiation": ["放射", "延伸", "擴散", "肩膀", "手臂"],
            "severity": ["多痛", "幾分", "嚴重", "程度"],
            "timing": ["多久", "持續", "間歇", "頻率"],
            "associated_symptoms": ["伴隨", "其他", "症狀", "呼吸", "噁心"],
            "risk_factors": ["抽菸", "高血壓", "糖尿病", "家族史", "危險因子"],
            "past_history_meds_allergy": ["病史", "用藥", "過敏", "以前"],
            "differential_diagnosis": ["診斷", "可能", "懷疑", "考慮"],
            "ideas_concerns": ["擔心", "想法", "害怕", "期待"],
            "critical_action_ecg": ["心電圖", "ECG", "12導程", "立即", "馬上"],
            "summary_and_plan": ["總結", "計畫", "檢查", "安全"]
        }
        
        # 優先使用預定義的關鍵字
        if item_id in keyword_mapping:
            return keyword_mapping[item_id]
        
        # 如果沒有預定義的，從描述中提取關鍵字
        import re
        chinese_words = re.findall(r'[\u4e00-\u9fff]+', point)
        return chinese_words[:3]  # 最多返回3個關鍵字
    
    def _should_update_vital_signs(self, conversation: Conversation) -> bool:
        """檢查是否需要更新生命體徵"""
        last_message = conversation.messages[-1] if conversation.messages else None
        if not last_message:
            return False
        
        # 檢查是否包含生命體徵相關指令
        vital_signs_keywords = ["測量", "生命徵象", "vital", "心率", "血壓", "呼吸", "血氧"]
        return any(keyword in last_message.content for keyword in vital_signs_keywords)
    
    def _generate_vital_signs(self, case: Case) -> Dict[str, Any]:
        """生成生命體徵數據"""
        # 從案例數據中提取生命體徵，如果沒有則使用預設值
        patient_data = case.data.patient_story_data
        
        # 嘗試從案例中獲取生命體徵
        if "vital_signs" in patient_data:
            return patient_data["vital_signs"]
        
        # 預設生命體徵（基於急性胸痛案例）
        return {
            "HR_bpm": 95,
            "SpO2_room_air": 96,
            "BP_mmHg": "140/85",
            "RR_bpm": 22
        }
    
    def end_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """結束對話"""
        conversation = self._conversations.get(conversation_id)
        if conversation:
            conversation.end_conversation()
        return conversation
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """取得對話歷史（用於前端顯示）"""
        conversation = self._conversations.get(conversation_id)
        if not conversation:
            return []
        
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in conversation.messages
        ]
