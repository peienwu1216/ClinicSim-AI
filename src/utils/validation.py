"""
數據驗證工具函式
"""

import re
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..models.case import CaseData
from ..models.conversation import Message, MessageRole


def validate_case_data(data: Dict[str, Any]) -> bool:
    """驗證案例數據格式"""
    required_fields = [
        'case_id', 'case_title', 'station_info', 
        'patient_profile', 'ai_instructions', 'patient_story_data'
    ]
    
    for field in required_fields:
        if field not in data:
            return False
    
    # 驗證 patient_profile
    patient_profile = data.get('patient_profile', {})
    required_patient_fields = ['name', 'age', 'gender', 'occupation']
    for field in required_patient_fields:
        if field not in patient_profile:
            return False
    
    # 驗證 ai_instructions
    ai_instructions = data.get('ai_instructions', {})
    required_ai_fields = ['persona', 'core_principles', 'behavioral_guidelines']
    for field in required_ai_fields:
        if field not in ai_instructions:
            return False
    
    return True


def validate_conversation_data(messages: List[Dict[str, Any]]) -> bool:
    """驗證對話數據格式"""
    if not isinstance(messages, list):
        return False
    
    for message in messages:
        if not isinstance(message, dict):
            return False
        
        if 'role' not in message or 'content' not in message:
            return False
        
        role = message['role']
        if role not in ['user', 'assistant', 'system']:
            return False
        
        content = message['content']
        if not isinstance(content, str) or len(content.strip()) == 0:
            return False
    
    return True


def validate_vital_signs_data(data: Dict[str, Any]) -> bool:
    """驗證生命體徵數據格式"""
    if not isinstance(data, dict):
        return False
    
    # 檢查是否包含任何生命體徵數據
    vital_signs_fields = ['HR_bpm', 'SpO2_room_air', 'BP_mmHg', 'RR_bpm', 'Temperature']
    
    has_any_vital_sign = any(field in data for field in vital_signs_fields)
    
    if not has_any_vital_sign:
        return False
    
    # 驗證數值類型
    for field, value in data.items():
        if field in ['HR_bpm', 'SpO2_room_air', 'RR_bpm'] and value is not None:
            if not isinstance(value, (int, float)) or value < 0:
                return False
        elif field == 'Temperature' and value is not None:
            if not isinstance(value, (int, float)) or value < 20 or value > 50:
                return False
        elif field == 'BP_mmHg' and value is not None:
            if not isinstance(value, str):
                return False
    
    return True


def validate_file_path(file_path: Path, expected_extension: str = None) -> bool:
    """驗證檔案路徑"""
    if not isinstance(file_path, Path):
        return False
    
    if not file_path.exists():
        return False
    
    if not file_path.is_file():
        return False
    
    if expected_extension and file_path.suffix != expected_extension:
        return False
    
    return True


def validate_case_id(case_id: str) -> bool:
    """驗證案例 ID 格式"""
    if not isinstance(case_id, str):
        return False
    
    if len(case_id.strip()) == 0:
        return False
    
    # 檢查是否包含非法字符
    if re.search(r'[<>:"/\\|?*]', case_id):
        return False
    
    return True


def validate_report_content(content: str) -> bool:
    """驗證報告內容"""
    if not isinstance(content, str):
        return False
    
    if len(content.strip()) == 0:
        return False
    
    if len(content) > 50000:  # 限制報告長度
        return False
    
    return True
