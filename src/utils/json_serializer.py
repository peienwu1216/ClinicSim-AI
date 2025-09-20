"""
JSON 序列化工具
處理 numpy 類型和其他不可序列化對象的轉換
"""

import numpy as np
from typing import Any, Dict, List, Union


def convert_to_json_serializable(obj: Any) -> Any:
    """
    將對象轉換為 JSON 可序列化的格式
    
    Args:
        obj: 要轉換的對象
    
    Returns:
        JSON 可序列化的對象
    """
    if isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, 'item'):  # numpy scalar
        return obj.item()
    elif hasattr(obj, 'dtype'):  # 其他 numpy 類型
        try:
            return float(obj)
        except (ValueError, TypeError):
            return str(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    else:
        return obj


def safe_model_dump(model_instance) -> Dict[str, Any]:
    """
    安全地將 Pydantic 模型轉換為字典，確保 JSON 可序列化
    
    Args:
        model_instance: Pydantic 模型實例
    
    Returns:
        JSON 可序列化的字典
    """
    if hasattr(model_instance, 'model_dump'):
        raw_dict = model_instance.model_dump()
    elif hasattr(model_instance, 'dict'):
        raw_dict = model_instance.dict()
    else:
        raw_dict = model_instance
    
    return convert_to_json_serializable(raw_dict)


def safe_jsonify_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    安全地準備 JSON 數據，確保所有值都是可序列化的
    
    Args:
        data: 要序列化的數據字典
    
    Returns:
        安全的 JSON 數據字典
    """
    return convert_to_json_serializable(data)
