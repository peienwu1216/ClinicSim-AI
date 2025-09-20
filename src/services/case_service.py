"""
案例管理服務
"""

import json
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
        return [f.stem for f in case_files]
    
    def clear_cache(self) -> None:
        """清除案例緩存"""
        self._case_cache.clear()
    
    def reload_case(self, case_id: str) -> Case:
        """重新載入案例"""
        if case_id in self._case_cache:
            del self._case_cache[case_id]
        return self.load_case(case_id)
