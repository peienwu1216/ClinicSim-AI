#!/usr/bin/env python3
"""
測試前端連接問題
"""

import requests
import json
import time

def test_api_connection():
    """測試 API 連接"""
    print("🔍 測試 API 連接...")
    
    try:
        # 測試健康檢查
        response = requests.get("http://127.0.0.1:5001/health", timeout=5)
        print(f"✅ 健康檢查: {response.status_code}")
        
        # 測試對話 API
        payload = {
            "history": [{"role": "user", "content": "你好"}],
            "case_id": "case_1"
        }
        
        print("📤 發送測試請求...")
        response = requests.post("http://127.0.0.1:5001/ask_patient", 
                               json=payload, 
                               timeout=30)
        
        print(f"📥 響應狀態: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 對話成功!")
            print(f"   覆蓋率: {data.get('coverage', 'N/A')}")
            print(f"   AI 回應: {data.get('reply', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ API 錯誤: {response.status_code}")
            print(f"   錯誤內容: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 請求超時")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 連接錯誤")
        return False
    except Exception as e:
        print(f"❌ 其他錯誤: {e}")
        return False

def test_streamlit_import():
    """測試 Streamlit 導入"""
    print("\n🔍 測試 Streamlit 導入...")
    
    try:
        import streamlit as st
        print(f"✅ Streamlit 版本: {st.__version__}")
        return True
    except Exception as e:
        print(f"❌ Streamlit 導入失敗: {e}")
        return False

def test_frontend_config():
    """測試前端配置"""
    print("\n🔍 測試前端配置...")
    
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        from src.config.settings import get_settings
        from src.frontend.app import StreamlitApp
        
        settings = get_settings()
        print(f"✅ 後端地址: {settings.backend_host}:{settings.backend_port}")
        
        app = StreamlitApp()
        print(f"✅ 前端 API URL: {app.api_base_url}")
        
        return True
    except Exception as e:
        print(f"❌ 前端配置錯誤: {e}")
        return False

def main():
    """主函式"""
    print("🚀 前端連接診斷工具")
    print("=" * 50)
    
    # 測試 API 連接
    api_ok = test_api_connection()
    
    # 測試 Streamlit
    streamlit_ok = test_streamlit_import()
    
    # 測試前端配置
    config_ok = test_frontend_config()
    
    print("\n" + "=" * 50)
    print("📋 診斷結果:")
    print(f"API 連接: {'✅ 正常' if api_ok else '❌ 異常'}")
    print(f"Streamlit: {'✅ 正常' if streamlit_ok else '❌ 異常'}")
    print(f"前端配置: {'✅ 正常' if config_ok else '❌ 異常'}")
    
    if api_ok and streamlit_ok and config_ok:
        print("\n✅ 所有測試通過！前端應該可以正常工作")
        print("💡 如果前端仍然沒有反應，請嘗試:")
        print("   1. 重新啟動前端: streamlit run src/frontend/app.py")
        print("   2. 清除瀏覽器快取")
        print("   3. 檢查瀏覽器控制台是否有錯誤")
    else:
        print("\n❌ 發現問題，請根據上述錯誤信息進行修復")

if __name__ == "__main__":
    main()
