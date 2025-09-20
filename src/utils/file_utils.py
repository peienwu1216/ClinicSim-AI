"""
檔案處理工具函式
"""

import os
from pathlib import Path
from typing import List, Optional


def ensure_directory_exists(directory_path: Path) -> bool:
    """確保目錄存在，如果不存在則創建"""
    try:
        directory_path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"無法創建目錄 {directory_path}: {e}")
        return False


def get_file_size(file_path: Path) -> Optional[int]:
    """取得檔案大小（位元組）"""
    try:
        if file_path.exists() and file_path.is_file():
            return file_path.stat().st_size
        return None
    except Exception as e:
        print(f"無法取得檔案大小 {file_path}: {e}")
        return None


def list_files_in_directory(directory_path: Path, extensions: List[str] = None) -> List[Path]:
    """列出目錄中的檔案"""
    if not directory_path.exists() or not directory_path.is_dir():
        return []
    
    files = []
    for file_path in directory_path.iterdir():
        if file_path.is_file():
            if extensions is None or file_path.suffix.lower() in extensions:
                files.append(file_path)
    
    return sorted(files)


def get_relative_path(file_path: Path, base_path: Path) -> str:
    """取得相對路徑"""
    try:
        return str(file_path.relative_to(base_path))
    except ValueError:
        return str(file_path)


def is_safe_path(file_path: Path, base_path: Path) -> bool:
    """檢查路徑是否安全（防止路徑遍歷攻擊）"""
    try:
        resolved_path = file_path.resolve()
        resolved_base = base_path.resolve()
        return resolved_path.is_relative_to(resolved_base)
    except Exception:
        return False


def create_backup(file_path: Path, backup_suffix: str = ".bak") -> Optional[Path]:
    """創建檔案備份"""
    try:
        if not file_path.exists():
            return None
        
        backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
        import shutil
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        print(f"創建備份失敗 {file_path}: {e}")
        return None


def cleanup_old_files(directory_path: Path, pattern: str = "*.tmp", max_age_hours: int = 24) -> int:
    """清理舊的臨時檔案"""
    if not directory_path.exists():
        return 0
    
    import time
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    cleaned_count = 0
    
    try:
        for file_path in directory_path.glob(pattern):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    file_path.unlink()
                    cleaned_count += 1
    except Exception as e:
        print(f"清理檔案失敗 {directory_path}: {e}")
    
    return cleaned_count
