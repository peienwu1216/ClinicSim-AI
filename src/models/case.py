"""
案例相關數據模型
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class PatientProfile(BaseModel):
    """病人基本資料"""
    name: str
    age: int
    gender: str
    occupation: str


class AIInstructions(BaseModel):
    """AI 病人指令"""
    persona: str
    core_principles: List[str]
    behavioral_guidelines: Dict[str, Any]


class FeedbackSystem(BaseModel):
    """回饋系統配置"""
    checklist: List[Dict[str, Any]]
    critical_actions: List[str]


class CaseData(BaseModel):
    """案例數據"""
    case_id: str
    case_title: str
    station_info: Dict[str, Any]
    patient_profile: PatientProfile
    ai_instructions: AIInstructions
    patient_story_data: Dict[str, Any]
    feedback_system: Optional[FeedbackSystem] = None


class Case(BaseModel):
    """案例模型"""
    data: CaseData
    is_loaded: bool = False
    
    def get_system_prompt(self) -> str:
        """生成系統提示詞"""
        return f"""
        你是一位模擬病人（標準化病人）。你的所有輸出必須使用『繁體中文』。
        【角色設定與回應規則】
        1. 僅回答學生（user）直接詢問的內容，不主動透露未被詢問的資訊。
        2. 回覆格式需為「[動作/情緒] 對話內容」。
        3. 嚴格依據下方個案資料作答。
        【個案行為規範】: {self.data.ai_instructions.model_dump_json(by_alias=False)}
        【個案資料】: {self.data.patient_story_data}
        請根據以上資訊和對話歷史，作為病人，以「繁體中文」回覆下一句話。切記絕對規則：所有輸出文字都要是繁體中文！！
        """
    
    def get_feedback_checklist(self) -> List[Dict[str, Any]]:
        """取得回饋檢查清單"""
        # 優先使用 feedback_system 中的檢查清單
        if self.data.feedback_system and self.data.feedback_system.checklist:
            return self.data.feedback_system.checklist
        
        # 如果沒有，嘗試從 patient_story_data 中獲取
        if "checklist" in self.data.patient_story_data:
            return self.data.patient_story_data["checklist"]
        
        return []
    
    def get_critical_actions(self) -> List[str]:
        """取得關鍵行動清單"""
        if self.data.feedback_system:
            return self.data.feedback_system.critical_actions
        return []
