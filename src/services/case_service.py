"""
案例管理服務
"""

import json
import random
from typing import Optional, Dict, Any
from pathlib import Path

from ..config.settings import get_settings
from ..models.case import Case, CaseData
from ..exceptions import CaseNotFoundError, CaseLoadError


class CaseService:
    """案例管理服務"""
    
    def __init__(self, settings=None):
        self.settings = settings or get_settings()
        self._case_cache: Dict[str, Case] = {}
    
    def load_case(self, case_id: str) -> Case:
        """載入案例"""
        # 檢查緩存
        if case_id in self._case_cache:
            return self._case_cache[case_id]
        
        # 載入案例檔案
        case_path = self.settings.get_case_path(case_id)
        
        if not case_path.exists():
            raise CaseNotFoundError(f"Case file not found: {case_path}")
        
        try:
            with open(case_path, 'r', encoding='utf-8') as f:
                case_data = json.load(f)
            
            # 驗證和轉換數據
            case = Case(
                data=CaseData(**case_data),
                is_loaded=True
            )
            
            # 緩存案例
            self._case_cache[case_id] = case
            return case
            
        except json.JSONDecodeError as e:
            raise CaseLoadError(f"Failed to parse case file {case_path}: {e}")
        except Exception as e:
            raise CaseLoadError(f"Failed to load case {case_id}: {e}")
    
    def get_case(self, case_id: str) -> Optional[Case]:
        """取得案例（不拋出異常）"""
        try:
            return self.load_case(case_id)
        except (CaseNotFoundError, CaseLoadError):
            return None
    
    def list_available_cases(self) -> list[str]:
        """列出所有可用的案例 ID"""
        if not self.settings.cases_dir.exists():
            return []
        
        case_files = list(self.settings.cases_dir.glob("*.json"))
        case_ids = []
        
        for case_file in case_files:
            try:
                # 讀取文件內容獲取實際的case_id
                with open(case_file, 'r', encoding='utf-8') as f:
                    case_data = json.load(f)
                    actual_case_id = case_data.get('case_id')
                    if actual_case_id:
                        case_ids.append(actual_case_id)
                    else:
                        # 如果沒有case_id，使用文件名
                        case_ids.append(case_file.stem)
            except Exception as e:
                print(f"⚠️ 無法讀取案例文件 {case_file}: {e}")
                # 如果讀取失敗，使用文件名
                case_ids.append(case_file.stem)
        
        return case_ids
    
    def clear_cache(self) -> None:
        """清除案例緩存"""
        self._case_cache.clear()
    
    def get_random_case(self) -> Optional[Case]:
        """隨機選擇一個可用的案例"""
        available_cases = self.list_available_cases()
        if not available_cases:
            return None
        
        random_case_id = random.choice(available_cases)
        return self.get_case(random_case_id)
    
    def get_random_case_id(self) -> Optional[str]:
        """隨機選擇一個可用的案例 ID"""
        available_cases = self.list_available_cases()
        if not available_cases:
            return None
        
        return random.choice(available_cases)
    
    def reload_case(self, case_id: str) -> Case:
        """重新載入案例"""
        if case_id in self._case_cache:
            del self._case_cache[case_id]
        return self.load_case(case_id)
