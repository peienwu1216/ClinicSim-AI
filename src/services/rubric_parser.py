"""
評分標準解析器
用於解析和處理 scoring_sys.json 中的評分標準
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class CriterionDefinition:
    """評分標準定義"""
    id: str
    description: str
    max_score: float
    keywords: List[str]
    patterns: List[str]  # 正則表達式模式
    required_elements: List[str]  # 必需元素
    optional_elements: List[str]  # 可選元素


@dataclass
class PenaltyDefinition:
    """懲罰項目定義"""
    id: str
    description: str
    deduct_score: float
    keywords: List[str]
    patterns: List[str]
    threshold: int  # 觸發閾值


@dataclass
class SectionDefinition:
    """評分類別定義"""
    id: str
    title: str
    weight: float
    criteria: List[CriterionDefinition]
    penalties: List[PenaltyDefinition]


class RubricParser:
    """評分標準解析器"""
    
    def __init__(self, rubric_data: Dict[str, Any]):
        self.rubric_data = rubric_data
        self.sections = self._parse_sections()
    
    def _parse_sections(self) -> List[SectionDefinition]:
        """解析評分類別"""
        sections = []
        
        for section_data in self.rubric_data.get('sections', []):
            section = SectionDefinition(
                id=section_data['id'],
                title=section_data['title'],
                weight=section_data['weight'],
                criteria=self._parse_criteria(section_data.get('criteria', [])),
                penalties=self._parse_penalties(section_data.get('penalties', []))
            )
            sections.append(section)
        
        return sections
    
    def _parse_criteria(self, criteria_data: List[Dict[str, Any]]) -> List[CriterionDefinition]:
        """解析評分標準"""
        criteria = []
        
        for criterion_data in criteria_data:
            criterion = CriterionDefinition(
                id=criterion_data['id'],
                description=criterion_data['desc'],
                max_score=criterion_data['score'],
                keywords=self._extract_keywords(criterion_data['desc']),
                patterns=self._generate_patterns(criterion_data['id'], criterion_data['desc']),
                required_elements=self._get_required_elements(criterion_data['id']),
                optional_elements=self._get_optional_elements(criterion_data['id'])
            )
            criteria.append(criterion)
        
        return criteria
    
    def _parse_penalties(self, penalties_data: List[Dict[str, Any]]) -> List[PenaltyDefinition]:
        """解析懲罰項目"""
        penalties = []
        
        for penalty_data in penalties_data:
            penalty = PenaltyDefinition(
                id=penalty_data['id'],
                description=penalty_data['desc'],
                deduct_score=penalty_data['deduct'],
                keywords=self._extract_keywords(penalty_data['desc']),
                patterns=self._generate_penalty_patterns(penalty_data['id']),
                threshold=self._get_penalty_threshold(penalty_data['id'])
            )
            penalties.append(penalty)
        
        return penalties
    
    def _extract_keywords(self, description: str) -> List[str]:
        """從描述中提取關鍵字"""
        # 基於描述內容提取相關關鍵字
        keyword_mapping = {
            "intro": ["自我介紹", "我是", "醫生", "同意", "隱私", "舒服", "可以嗎", "確認"],
            "opqrst": ["什麼時候", "發作", "開始", "突然", "誘發", "什麼會讓", "活動", "深呼吸", 
                      "什麼樣", "壓", "悶", "刺痛", "性質", "延伸", "放射", "肩膀", "下巴",
                      "幾分", "多痛", "嚴重", "程度", "多久", "持續", "間歇", "時間"],
            "associated_symptoms": ["喘", "呼吸困難", "冷汗", "盜汗", "噁心", "想吐", "嘔吐", "咳嗽", "發燒"],
            "ice": ["想法", "擔心", "期待", "希望", "害怕", "擔憂", "你覺得", "你認為"],
            "acs": ["胸痛", "壓迫", "悶", "放射", "肩膀", "下巴", "菸", "抽菸", "高血壓", "糖尿病", 
                   "家族史", "心臟病", "膽固醇", "風險因子", "既往史"],
            "aortic_dissection": ["撕裂", "撕開", "高血壓", "馬凡", "馬凡氏症", "主動脈"],
            "pe": ["久坐", "長途", "飛機", "開車", "下肢", "腫", "咳血", "肺栓塞"],
            "pericarditis": ["體位", "姿勢", "坐起來", "往前傾", "心包炎"],
            "gerd": ["進食", "吃飯", "火燒心", "胃食道", "逆流"],
            "costochondritis": ["胸壁", "壓痛", "肌肉", "骨骼", "按壓"],
            "ecg": ["心電圖", "ECG", "12導程", "12導", "立刻", "馬上", "立即", "10分", "十分"],
            "troponin": ["troponin", "心肌鈣蛋白", "心肌酵素", "抽血", "檢驗", "血液"],
            "cxr_ct": ["胸部X光", "CXR", "CT", "電腦斷層", "影像"],
            "list_3": ["鑑別", "診斷", "可能", "考慮", "懷疑", "排除"],
            "acs_first": ["急性冠心症", "ACS", "AMI", "心肌梗塞", "首要", "優先"],
            "non_cardiac": ["胃食道", "肌肉", "骨骼", "非心因性", "非心臟"],
            "tests": ["檢查", "檢驗", "ECG", "心電圖", "抽血", "X光"],
            "empathy": ["理解", "同理", "安撫", "安慰", "別擔心", "會好的"],
            "summary": ["總結", "回顧", "整理", "歸納", "剛才"],
            "safety": ["安全", "叮嚀", "注意", "小心", "下一步", "安排"]
        }
        
        # 根據描述內容匹配關鍵字
        keywords = []
        description_lower = description.lower()
        
        for key, words in keyword_mapping.items():
            if any(word in description_lower for word in words):
                keywords.extend(words)
        
        # 如果沒有匹配到特定關鍵字，使用通用關鍵字
        if not keywords:
            keywords = self._extract_generic_keywords(description)
        
        return list(set(keywords))  # 去重
    
    def _extract_generic_keywords(self, description: str) -> List[str]:
        """提取通用關鍵字"""
        import re
        # 提取中文詞彙
        chinese_words = re.findall(r'[\u4e00-\u9fff]+', description)
        return chinese_words
    
    def _generate_patterns(self, criterion_id: str, description: str) -> List[str]:
        """生成正則表達式模式"""
        patterns = []
        
        if criterion_id == "opqrst":
            patterns = [
                r"什麼時候.*開始",
                r"什麼時候.*發作",
                r"什麼.*誘發",
                r"什麼.*緩解",
                r"什麼樣.*痛",
                r"痛.*哪裡",
                r"幾分.*痛",
                r"多.*痛",
                r"持續.*多久"
            ]
        elif criterion_id == "ecg":
            patterns = [
                r"心電圖.*立刻",
                r"ECG.*立即",
                r"12導程.*馬上",
                r"立刻.*心電圖",
                r"立即.*ECG"
            ]
        elif criterion_id == "acs":
            patterns = [
                r"胸痛.*放射",
                r"壓迫.*悶",
                r"家族.*心臟",
                r"抽菸.*年",
                r"高血壓.*糖尿病"
            ]
        
        return patterns
    
    def _generate_penalty_patterns(self, penalty_id: str) -> List[str]:
        """生成懲罰項目的正則表達式模式"""
        patterns = []
        
        if penalty_id == "repeated":
            patterns = [
                r"哪裡.*痛.*哪裡.*痛",  # 重複詢問疼痛位置
                r"什麼時候.*什麼時候",  # 重複詢問時間
                r"什麼樣.*什麼樣"  # 重複詢問性質
            ]
        elif penalty_id == "irrelevant":
            patterns = [
                r"天氣|政治|娛樂|運動|美食|旅遊"
            ]
        
        return patterns
    
    def _get_required_elements(self, criterion_id: str) -> List[str]:
        """獲取必需元素"""
        required_mapping = {
            "intro": ["自我介紹", "同意"],
            "opqrst": ["位置", "時間", "性質"],
            "ecg": ["心電圖", "立即", "時間"],
            "troponin": ["抽血", "檢驗"],
            "acs": ["胸痛", "放射", "風險因子"]
        }
        
        return required_mapping.get(criterion_id, [])
    
    def _get_optional_elements(self, criterion_id: str) -> List[str]:
        """獲取可選元素"""
        optional_mapping = {
            "intro": ["隱私", "舒服"],
            "opqrst": ["誘發", "緩解", "嚴重程度"],
            "ecg": ["12導程", "10分鐘"],
            "troponin": ["心肌鈣蛋白", "心肌酵素"],
            "acs": ["家族史", "既往史", "用藥史"]
        }
        
        return optional_mapping.get(criterion_id, [])
    
    def _get_penalty_threshold(self, penalty_id: str) -> int:
        """獲取懲罰觸發閾值"""
        threshold_mapping = {
            "repeated": 3,  # 重複3次以上
            "irrelevant": 2,  # 2個以上無關問題
            "missed_red_flag": 1  # 1個紅旗症狀未詢問
        }
        
        return threshold_mapping.get(penalty_id, 1)
    
    def get_section_by_id(self, section_id: str) -> Optional[SectionDefinition]:
        """根據ID獲取評分類別"""
        for section in self.sections:
            if section.id == section_id:
                return section
        return None
    
    def get_criterion_by_id(self, criterion_id: str) -> Optional[CriterionDefinition]:
        """根據ID獲取評分標準"""
        for section in self.sections:
            for criterion in section.criteria:
                if criterion.id == criterion_id:
                    return criterion
        return None
    
    def get_all_criteria(self) -> List[CriterionDefinition]:
        """獲取所有評分標準"""
        all_criteria = []
        for section in self.sections:
            all_criteria.extend(section.criteria)
        return all_criteria
    
    def get_all_penalties(self) -> List[PenaltyDefinition]:
        """獲取所有懲罰項目"""
        all_penalties = []
        for section in self.sections:
            all_penalties.extend(section.penalties)
        return all_penalties
