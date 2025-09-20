"""
Pytest 配置文件
定義測試的共用fixtures和配置
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys

# 添加src目錄到路徑
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

@pytest.fixture(scope="session")
def project_root():
    """專案根目錄"""
    return Path(__file__).parent.parent

@pytest.fixture(scope="session")
def temp_dir():
    """臨時目錄"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)

@pytest.fixture(scope="session")
def test_data():
    """測試數據"""
    return {
        "test_case": {
            "case_id": "test_case_001",
            "title": "測試病例",
            "description": "這是一個測試病例",
            "patient_info": {"age": 30, "gender": "male"},
            "symptoms": ["胸痛", "呼吸困難"],
            "diagnosis": "急性胸痛"
        },
        "test_conversation": {
            "conversation_id": "test_conv_001",
            "case_id": "test_case_001",
            "messages": [
                {"role": "user", "content": "你好"},
                {"role": "assistant", "content": "您好，我是您的AI醫生助手"}
            ]
        }
    }

@pytest.fixture(scope="function")
def mock_ai_service():
    """模擬AI服務"""
    class MockAIService:
        def __init__(self):
            self.responses = [
                "我了解您的症狀，請詳細描述一下胸痛的性質。",
                "根據您的描述，我建議進行進一步檢查。",
                "請告訴我疼痛的持續時間和強度。"
            ]
            self.response_index = 0
        
        def generate_response(self, conversation, case_id=None):
            response = self.responses[self.response_index % len(self.responses)]
            self.response_index += 1
            return response
    
    return MockAIService()

@pytest.fixture(scope="function")
def mock_rag_service():
    """模擬RAG服務"""
    class MockRAGService:
        def __init__(self):
            self.mock_results = [
                {
                    "content": "急性胸痛的診斷需要考慮多種因素...",
                    "source": "clinical_guidelines.pdf",
                    "score": 0.95
                },
                {
                    "content": "ECG檢查是胸痛診斷的重要工具...",
                    "source": "ecg_guidelines.pdf", 
                    "score": 0.88
                }
            ]
        
        def search(self, query, k=3):
            return self.mock_results[:k]
        
        def is_available(self):
            return True
    
    return MockRAGService()

# Pytest配置
def pytest_configure(config):
    """Pytest配置"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )

def pytest_collection_modifyitems(config, items):
    """修改測試收集"""
    for item in items:
        # 自動標記測試類型
        if "test_api" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "test_basic" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        
        # 標記慢速測試
        if "slow" in item.keywords or "integration" in item.keywords:
            item.add_marker(pytest.mark.slow)
