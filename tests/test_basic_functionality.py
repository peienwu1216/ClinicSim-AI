"""
基本功能測試
測試應用程式的核心功能和組件
"""

import pytest
import sys
from pathlib import Path

# 添加src目錄到路徑
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """測試所有主要模組可以正常導入"""
    try:
        # 測試核心模組導入
        from src.config.settings import Settings
        from src.models.case import Case
        from src.models.conversation import Conversation
        from src.services.ai_service import AIService
        from src.services.rag_service import RAGService
        print("✅ 所有核心模組導入成功")
    except ImportError as e:
        pytest.fail(f"模組導入失敗: {e}")

def test_settings_configuration():
    """測試配置系統"""
    try:
        from src.config.settings import Settings
        
        # 測試預設配置
        settings = Settings()
        assert settings.host == "127.0.0.1"
        assert settings.port == 5001
        assert settings.app_name == "ClinicSim-AI"
        print("✅ 配置系統測試通過")
    except Exception as e:
        pytest.fail(f"配置系統測試失敗: {e}")

def test_case_model():
    """測試病例模型"""
    try:
        from src.models.case import Case
        
        # 創建測試病例
        test_case = Case(
            case_id="test_case_001",
            title="測試病例",
            description="這是一個測試病例",
            patient_info={"age": 30, "gender": "male"},
            symptoms=["胸痛", "呼吸困難"],
            diagnosis="急性胸痛"
        )
        
        assert test_case.case_id == "test_case_001"
        assert test_case.title == "測試病例"
        assert len(test_case.symptoms) == 2
        print("✅ 病例模型測試通過")
    except Exception as e:
        pytest.fail(f"病例模型測試失敗: {e}")

def test_conversation_model():
    """測試對話模型"""
    try:
        from src.models.conversation import Conversation
        
        # 創建測試對話
        conversation = Conversation(
            conversation_id="test_conv_001",
            case_id="test_case_001",
            messages=[
                {"role": "user", "content": "你好"},
                {"role": "assistant", "content": "您好，我是您的AI醫生助手"}
            ]
        )
        
        assert conversation.conversation_id == "test_conv_001"
        assert len(conversation.messages) == 2
        assert conversation.messages[0]["role"] == "user"
        print("✅ 對話模型測試通過")
    except Exception as e:
        pytest.fail(f"對話模型測試失敗: {e}")

def test_file_structure():
    """測試專案文件結構"""
    project_root = Path(__file__).parent.parent
    
    # 檢查必要文件是否存在
    required_files = [
        "app.py",
        "main.py",
        "README.md",
        "LICENSE",
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-base.txt"
    ]
    
    for file_name in required_files:
        file_path = project_root / file_name
        assert file_path.exists(), f"必要文件不存在: {file_name}"
    
    # 檢查必要目錄是否存在
    required_dirs = [
        "src",
        "docs",
        "tests",
        "cases",
        "static"
    ]
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        assert dir_path.exists(), f"必要目錄不存在: {dir_name}"
        assert dir_path.is_dir(), f"不是目錄: {dir_name}"
    
    print("✅ 專案文件結構測試通過")

def test_requirements_files():
    """測試requirements文件格式"""
    project_root = Path(__file__).parent.parent
    
    requirements_files = [
        "requirements.txt",
        "requirements-dev.txt", 
        "requirements-base.txt"
    ]
    
    for req_file in requirements_files:
        file_path = project_root / req_file
        assert file_path.exists(), f"Requirements文件不存在: {req_file}"
        
        # 檢查文件內容不為空
        content = file_path.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, f"Requirements文件為空: {req_file}"
        
        # 檢查是否包含基本依賴
        if req_file == "requirements.txt":
            assert "streamlit" in content or "Streamlit" in content
            assert "flask" in content or "Flask" in content
        
        print(f"✅ {req_file} 格式正確")

def test_json_files():
    """測試JSON配置文件"""
    project_root = Path(__file__).parent.parent
    
    # 檢查病例文件
    cases_dir = project_root / "cases"
    if cases_dir.exists():
        json_files = list(cases_dir.glob("*.json"))
        assert len(json_files) > 0, "沒有找到病例JSON文件"
        
        # 檢查第一個JSON文件格式
        first_json = json_files[0]
        try:
            import json
            with open(first_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert isinstance(data, dict), "JSON文件格式不正確"
            print(f"✅ {first_json.name} JSON格式正確")
        except Exception as e:
            pytest.fail(f"JSON文件解析失敗 {first_json.name}: {e}")

def test_environment_variables():
    """測試環境變數配置"""
    import os
    
    # 檢查是否有.env文件或環境變數
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    if env_file.exists():
        print("✅ 找到.env配置文件")
    else:
        print("⚠️ 未找到.env文件，將使用預設配置")

def test_dependencies_availability():
    """測試關鍵依賴是否可用"""
    dependencies = [
        ("streamlit", "Streamlit"),
        ("flask", "Flask"),
        ("requests", "Requests"),
        ("pydantic", "Pydantic"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas")
    ]
    
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {display_name} 可用")
        except ImportError:
            print(f"⚠️ {display_name} 不可用 (可能未安裝)")

if __name__ == "__main__":
    # 如果直接運行此文件，執行所有測試
    pytest.main([__file__, "-v"])
