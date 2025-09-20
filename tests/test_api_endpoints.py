"""
API端點測試
測試後端API的基本功能
"""

import pytest
import requests
import time
import sys
from pathlib import Path

# 添加src目錄到路徑
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

class TestAPIEndpoints:
    """API端點測試類"""
    
    @pytest.fixture(scope="class")
    def base_url(self):
        """測試基礎URL"""
        return "http://127.0.0.1:5001"
    
    def test_health_endpoint(self, base_url):
        """測試健康檢查端點"""
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert data["status"] == "healthy"
            print("✅ 健康檢查端點測試通過")
        except requests.exceptions.ConnectionError:
            pytest.skip("後端服務未運行，跳過API測試")
        except Exception as e:
            pytest.fail(f"健康檢查端點測試失敗: {e}")
    
    def test_ask_patient_endpoint(self, base_url):
        """測試問診端點"""
        try:
            test_data = {
                "conversation": "患者說：我胸口很痛",
                "case_id": "test_case_001"
            }
            
            response = requests.post(
                f"{base_url}/ask_patient",
                json=test_data,
                timeout=10
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert isinstance(data["response"], str)
            assert len(data["response"]) > 0
            print("✅ 問診端點測試通過")
        except requests.exceptions.ConnectionError:
            pytest.skip("後端服務未運行，跳過API測試")
        except Exception as e:
            pytest.fail(f"問診端點測試失敗: {e}")
    
    def test_get_cases_endpoint(self, base_url):
        """測試獲取病例端點"""
        try:
            response = requests.get(f"{base_url}/cases", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            print("✅ 獲取病例端點測試通過")
        except requests.exceptions.ConnectionError:
            pytest.skip("後端服務未運行，跳過API測試")
        except Exception as e:
            pytest.fail(f"獲取病例端點測試失敗: {e}")
    
    def test_get_case_by_id_endpoint(self, base_url):
        """測試根據ID獲取病例端點"""
        try:
            # 先獲取病例列表
            cases_response = requests.get(f"{base_url}/cases", timeout=5)
            if cases_response.status_code == 200:
                cases = cases_response.json()
                if cases:
                    case_id = cases[0]["case_id"]
                    
                    # 測試獲取特定病例
                    response = requests.get(f"{base_url}/cases/{case_id}", timeout=5)
                    assert response.status_code == 200
                    data = response.json()
                    assert "case_id" in data
                    assert data["case_id"] == case_id
                    print("✅ 根據ID獲取病例端點測試通過")
                else:
                    pytest.skip("沒有可用病例，跳過測試")
            else:
                pytest.skip("無法獲取病例列表，跳過測試")
        except requests.exceptions.ConnectionError:
            pytest.skip("後端服務未運行，跳過API測試")
        except Exception as e:
            pytest.fail(f"根據ID獲取病例端點測試失敗: {e}")
    
    def test_invalid_endpoint(self, base_url):
        """測試無效端點"""
        try:
            response = requests.get(f"{base_url}/invalid_endpoint", timeout=5)
            assert response.status_code == 404
            print("✅ 無效端點測試通過")
        except requests.exceptions.ConnectionError:
            pytest.skip("後端服務未運行，跳過API測試")
        except Exception as e:
            pytest.fail(f"無效端點測試失敗: {e}")

class TestAPIErrorHandling:
    """API錯誤處理測試"""
    
    @pytest.fixture(scope="class")
    def base_url(self):
        return "http://127.0.0.1:5001"
    
    def test_malformed_request(self, base_url):
        """測試格式錯誤的請求"""
        try:
            # 發送格式錯誤的JSON
            response = requests.post(
                f"{base_url}/ask_patient",
                data="invalid json",
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            assert response.status_code == 400
            print("✅ 格式錯誤請求測試通過")
        except requests.exceptions.ConnectionError:
            pytest.skip("後端服務未運行，跳過API測試")
        except Exception as e:
            pytest.fail(f"格式錯誤請求測試失敗: {e}")
    
    def test_missing_required_fields(self, base_url):
        """測試缺少必需字段的請求"""
        try:
            # 發送缺少必需字段的請求
            test_data = {
                "conversation": "測試對話"
                # 缺少 case_id
            }
            
            response = requests.post(
                f"{base_url}/ask_patient",
                json=test_data,
                timeout=5
            )
            assert response.status_code == 400
            print("✅ 缺少必需字段測試通過")
        except requests.exceptions.ConnectionError:
            pytest.skip("後端服務未運行，跳過API測試")
        except Exception as e:
            pytest.fail(f"缺少必需字段測試失敗: {e}")

def test_backend_startup():
    """測試後端服務啟動"""
    try:
        # 嘗試導入後端模組
        from src.api.routes import create_app
        from src.config.settings import Settings
        
        # 創建測試應用
        settings = Settings()
        app = create_app(settings)
        
        assert app is not None
        print("✅ 後端服務啟動測試通過")
    except ImportError as e:
        pytest.skip(f"後端模組導入失敗: {e}")
    except Exception as e:
        pytest.fail(f"後端服務啟動測試失敗: {e}")

if __name__ == "__main__":
    # 如果直接運行此文件，執行所有測試
    pytest.main([__file__, "-v"])
