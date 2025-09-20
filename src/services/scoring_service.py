"""
基於 scoring_sys.json 的結構化評分服務
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

from ..config.settings import get_settings
from ..models.conversation import Conversation
from .rubric_parser import RubricParser


@dataclass
class CriterionScore:
    """評分項目結果"""
    criterion_id: str
    description: str
    max_score: float
    achieved_score: float
    evidence: List[str]  # 支持該評分的證據（匹配的關鍵字或內容）
    is_penalty: bool = False


@dataclass
class SectionScore:
    """評分類別結果"""
    section_id: str
    title: str
    weight: float
    max_score: float
    achieved_score: float
    criteria_scores: List[CriterionScore]
    penalties: List[CriterionScore]


@dataclass
class OverallScore:
    """總體評分結果"""
    total_score: float
    max_score: float
    percentage: float
    grade: str
    grade_description: str
    section_scores: List[SectionScore]
    detailed_feedback: str


class ScoringService:
    """結構化評分服務"""
    
    def __init__(self, settings=None):
        self.settings = settings or get_settings()
        self.rubric_data = self._load_rubric()
        self.rubric_parser = RubricParser(self.rubric_data)
    
    def _load_rubric(self) -> Dict[str, Any]:
        """載入評分標準"""
        rubric_path = Path(self.settings.project_root) / "scoring_sys.json"
        
        if not rubric_path.exists():
            raise FileNotFoundError(f"評分標準文件不存在: {rubric_path}")
        
        with open(rubric_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('rubric', {})
    
    def score_conversation(self, conversation: Conversation) -> OverallScore:
        """對對話進行結構化評分"""
        conversation_text = conversation.get_conversation_text().lower()
        user_messages = [msg.content for msg in conversation.messages if msg.role.value == 'user']
        
        section_scores = []
        total_achieved = 0.0
        total_max = 0.0
        
        # 評分各個類別
        for section in self.rubric_parser.sections:
            section_score = self._score_section(section, conversation_text, user_messages)
            section_scores.append(section_score)
            
            # 計算加權分數
            weighted_score = section_score.achieved_score * (section_score.weight / 100)
            total_achieved += weighted_score
            total_max += section_score.max_score * (section_score.weight / 100)
        
        # 計算總分和等級
        percentage = (total_achieved / total_max * 100) if total_max > 0 else 0
        grade, grade_description = self._determine_grade(percentage)
        
        # 生成詳細反饋
        detailed_feedback = self._generate_detailed_feedback(section_scores, percentage)
        
        return OverallScore(
            total_score=total_achieved,
            max_score=total_max,
            percentage=percentage,
            grade=grade,
            grade_description=grade_description,
            section_scores=section_scores,
            detailed_feedback=detailed_feedback
        )
    
    def _score_section(self, section: Any, conversation_text: str, user_messages: List[str]) -> SectionScore:
        """評分單一類別"""
        criteria_scores = []
        penalties = []
        
        # 評分各項標準
        for criterion in section.criteria:
            criterion_score = self._score_criterion(criterion, conversation_text, user_messages)
            criteria_scores.append(criterion_score)
        
        # 處理懲罰項目
        for penalty in section.penalties:
            penalty_score = self._score_penalty(penalty, conversation_text, user_messages)
            penalties.append(penalty_score)
        
        # 計算該類別總分
        achieved_score = sum(cs.achieved_score for cs in criteria_scores)
        max_score = sum(cs.max_score for cs in criteria_scores)
        
        # 扣除懲罰分數
        penalty_deduction = sum(p.achieved_score for p in penalties)
        achieved_score = max(0, achieved_score - penalty_deduction)
        
        return SectionScore(
            section_id=section.id,
            title=section.title,
            weight=section.weight,
            max_score=max_score,
            achieved_score=achieved_score,
            criteria_scores=criteria_scores,
            penalties=penalties
        )
    
    def _score_criterion(self, criterion: Any, conversation_text: str, user_messages: List[str]) -> CriterionScore:
        """評分單一標準"""
        criterion_id = criterion.id
        description = criterion.description
        max_score = criterion.max_score
        
        # 根據不同的標準使用不同的評分邏輯
        achieved_score, evidence = self._evaluate_criterion(criterion_id, description, conversation_text, user_messages)
        
        return CriterionScore(
            criterion_id=criterion_id,
            description=description,
            max_score=max_score,
            achieved_score=achieved_score,
            evidence=evidence
        )
    
    def _score_penalty(self, penalty: Any, conversation_text: str, user_messages: List[str]) -> CriterionScore:
        """評分懲罰項目"""
        penalty_id = penalty.id
        description = penalty.description
        deduct_score = penalty.deduct_score
        
        # 檢查是否觸發懲罰
        penalty_triggered, evidence = self._evaluate_penalty(penalty_id, description, conversation_text, user_messages)
        
        return CriterionScore(
            criterion_id=penalty_id,
            description=description,
            max_score=0,  # 懲罰項目沒有最高分
            achieved_score=deduct_score if penalty_triggered else 0,
            evidence=evidence,
            is_penalty=True
        )
    
    def _evaluate_criterion(self, criterion_id: str, description: str, conversation_text: str, user_messages: List[str]) -> Tuple[float, List[str]]:
        """評估單一標準的達成情況"""
        evidence = []
        
        # 獲取該標準的定義
        criterion_def = self.rubric_parser.get_criterion_by_id(criterion_id)
        if not criterion_def:
            return 0.0, []
        
        # 使用解析器提供的關鍵字和模式
        keywords = criterion_def.keywords
        patterns = criterion_def.patterns
        required_elements = criterion_def.required_elements
        optional_elements = criterion_def.optional_elements
        
        if criterion_id == "intro":
            # 自我介紹、確認舒適、取得同意
            matched = [kw for kw in keywords if kw in conversation_text]
            required_matched = [elem for elem in required_elements if elem in conversation_text]
            
            if len(required_matched) >= 2 and len(matched) >= 3:
                evidence = matched
                return 2.0, evidence
            elif len(required_matched) >= 1 and len(matched) >= 2:
                evidence = matched
                return 1.0, evidence
        
        elif criterion_id == "opqrst":
            # OPQRST 六要素 - 使用模式匹配
            covered_aspects = 0
            for pattern in patterns:
                if re.search(pattern, conversation_text):
                    covered_aspects += 1
                    evidence.append(pattern)
            
            # 每項 2 分，共 12 分
            score = min(covered_aspects * 2, 12)
            return score, evidence
        
        # 使用通用評分邏輯
        return self._generic_criterion_evaluation(criterion_def, conversation_text, user_messages)
    
    def _evaluate_penalty(self, penalty_id: str, description: str, conversation_text: str, user_messages: List[str]) -> Tuple[bool, List[str]]:
        """評估是否觸發懲罰"""
        evidence = []
        
        if penalty_id == "irrelevant":
            # 與診斷無關的問題
            irrelevant_keywords = ["天氣", "政治", "娛樂", "運動", "美食", "旅遊"]
            matched = [kw for kw in irrelevant_keywords if kw in conversation_text]
            if len(matched) >= 2:
                evidence = matched
                return True, evidence
        
        elif penalty_id == "repeated":
            # 重複問相同問題
            # 簡單檢查：統計相同問題的出現次數
            question_patterns = [r"哪裡.*痛", r"什麼時候.*開始", r"什麼樣.*痛"]
            for pattern in question_patterns:
                matches = re.findall(pattern, conversation_text)
                if len(matches) >= 3:  # 同一個問題問了3次以上
                    evidence.append(f"重複詢問: {pattern}")
                    return True, evidence
        
        elif penalty_id == "missed_red_flag":
            # 忽略紅旗症狀
            red_flag_keywords = ["胸痛", "壓迫", "放射", "冷汗", "噁心"]
            if not any(kw in conversation_text for kw in red_flag_keywords):
                evidence.append("未詢問關鍵紅旗症狀")
                return True, evidence
        
        return False, evidence
    
    def _generic_criterion_evaluation(self, criterion_def: Any, conversation_text: str, user_messages: List[str]) -> Tuple[float, List[str]]:
        """通用標準評估"""
        evidence = []
        max_score = criterion_def.max_score
        
        # 檢查必需元素
        required_matched = [elem for elem in criterion_def.required_elements if elem in conversation_text]
        optional_matched = [elem for elem in criterion_def.optional_elements if elem in conversation_text]
        
        # 檢查關鍵字匹配
        keyword_matched = [kw for kw in criterion_def.keywords if kw in conversation_text]
        
        # 檢查模式匹配
        pattern_matched = []
        for pattern in criterion_def.patterns:
            if re.search(pattern, conversation_text):
                pattern_matched.append(pattern)
        
        # 計算分數
        score = 0.0
        
        # 必需元素權重最高
        if len(required_matched) == len(criterion_def.required_elements):
            score += max_score * 0.6  # 必需元素佔60%
        elif len(required_matched) > 0:
            score += max_score * 0.3  # 部分必需元素佔30%
        
        # 關鍵字匹配
        if len(keyword_matched) >= 3:
            score += max_score * 0.3
        elif len(keyword_matched) >= 2:
            score += max_score * 0.2
        elif len(keyword_matched) >= 1:
            score += max_score * 0.1
        
        # 模式匹配
        if len(pattern_matched) >= 2:
            score += max_score * 0.2
        elif len(pattern_matched) >= 1:
            score += max_score * 0.1
        
        # 可選元素加分
        if len(optional_matched) >= 2:
            score += max_score * 0.1
        
        # 確保不超過最高分
        score = min(score, max_score)
        
        # 收集證據
        evidence.extend(required_matched)
        evidence.extend(keyword_matched[:3])  # 最多3個關鍵字
        evidence.extend(pattern_matched[:2])  # 最多2個模式
        
        return score, evidence
    
    def _determine_grade(self, percentage: float) -> Tuple[str, str]:
        """確定等級"""
        grading_scale = self.rubric_data.get('grading_scale', {})
        
        if percentage >= 90:
            return "excellent", grading_scale.get('excellent', "90-100 分：問診完整、精準，有臨床決策。")
        elif percentage >= 75:
            return "good", grading_scale.get('good', "75-89 分：大致完整，少部分缺漏或無關問題。")
        elif percentage >= 60:
            return "pass", grading_scale.get('pass', "60-74 分：有結構但關鍵診斷線索漏太多。")
        else:
            return "fail", grading_scale.get('fail', "<60 分：核心問診未完成或誤導性問題過多。")
    
    def _generate_detailed_feedback(self, section_scores: List[SectionScore], percentage: float) -> str:
        """生成詳細反饋"""
        feedback_parts = []
        
        # 總體評分
        feedback_parts.append(f"## 總體評分: {percentage:.1f}%")
        
        # 各類別評分
        for section in section_scores:
            section_percentage = (section.achieved_score / section.max_score * 100) if section.max_score > 0 else 0
            feedback_parts.append(f"\n### {section.title} ({section_percentage:.1f}%)")
            
            # 詳細項目
            for criterion in section.criteria_scores:
                if criterion.achieved_score > 0:
                    feedback_parts.append(f"- ✅ {criterion.description}: {criterion.achieved_score:.1f}/{criterion.max_score}")
                    if criterion.evidence:
                        feedback_parts.append(f"  證據: {', '.join(criterion.evidence[:3])}")
                else:
                    feedback_parts.append(f"- ❌ {criterion.description}: 0/{criterion.max_score}")
            
            # 懲罰項目
            for penalty in section.penalties:
                if penalty.achieved_score > 0:
                    feedback_parts.append(f"- ⚠️ {penalty.description}: -{penalty.achieved_score}")
        
        return "\n".join(feedback_parts)
