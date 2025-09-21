#!/usr/bin/env python3
"""
Lemonade Server API 測試腳本
測試 Lemonade Server 的 OpenAI 兼容 API
"""

import requests
import json
import sys
import time
from pathlib import Path

def test_server_connection(base_url: str):
    """測試伺服器連接"""
    print(f"測試 Lemonade Server 連接: {base_url}")
    
    try:
        # 直接測試 /api/v1/models 端點
        response = requests.get(f"{base_url}/models", timeout=5)
        if response.status_code == 200:
            print("伺服器連接成功")
            return True
        else:
            print(f"伺服器回應狀態碼: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"無法連接到伺服器: {e}")
        return False

def test_models_endpoint(base_url: str):
    """測試模型列表端點"""
    print(f"\n📋 測試模型列表端點...")
    
    try:
        response = requests.get(f"{base_url}/models", timeout=10)
        if response.status_code == 200:
            models_data = response.json()
            print("✅ 模型列表獲取成功")
            print(f"📊 可用模型數量: {len(models_data.get('data', []))}")
            
            for model in models_data.get('data', []):
                print(f"   - {model.get('id', 'Unknown')}")
            
            return True
        else:
            print(f"❌ 模型列表獲取失敗: {response.status_code}")
            print(f"回應內容: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 模型列表請求失敗: {e}")
        return False

def test_chat_completions(base_url: str, model_name: str):
    """測試聊天完成端點"""
    print(f"\n💬 測試聊天完成端點...")
    print(f"使用模型: {model_name}")
    
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": "你好，說明一下Hybrid是怎麼跑的？"
            }
        ],
        "stream": False,
        "max_tokens": 100
    }
    
    try:
        print("🚀 發送請求...")
        start_time = time.time()
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天完成請求成功")
            print(f"⏱️ 回應時間: {response_time:.2f} 秒")
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"💬 回應內容: {content}")
                print(f"📊 回應長度: {len(content)} 字元")
                print(f"🚀 生成速度: {len(content) / response_time:.1f} 字元/秒")
                return True
            else:
                print("❌ 回應格式不正確")
                return False
        else:
            print(f"❌ 聊天完成請求失敗: {response.status_code}")
            print(f"錯誤內容: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 聊天完成請求失敗: {e}")
        return False

def test_clinical_scenario(base_url: str, model_name: str):
    """測試臨床場景"""
    print(f"\n🏥 測試臨床場景...")
    
    clinical_payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": "患者主訴胸痛，請列出需要詢問的關鍵問題。"
            }
        ],
        "stream": False,
        "max_tokens": 200
    }
    
    try:
        print("🚀 發送臨床場景請求...")
        start_time = time.time()
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={"Content-Type": "application/json"},
            json=clinical_payload,
            timeout=30
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 臨床場景請求成功")
            print(f"⏱️ 回應時間: {response_time:.2f} 秒")
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"💬 臨床回應: {content}")
                return True
            else:
                print("❌ 臨床場景回應格式不正確")
                return False
        else:
            print(f"❌ 臨床場景請求失敗: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 臨床場景請求失敗: {e}")
        return False

def test_clinicsim_integration():
    """測試 ClinicSim 整合"""
    print(f"\n🔗 測試 ClinicSim 整合...")
    
    try:
        # 添加 src 目錄到 Python 路徑
        project_root = Path(__file__).parent
        src_path = project_root / "src"
        sys.path.insert(0, str(src_path))
        
        from src.config import get_settings
        from src.services.ai_service import AIServiceFactory, AIProvider
        
        # 載入設定
        settings = get_settings()
        print(f"📋 AI 提供者: {settings.ai_provider}")
        print(f"🌐 伺服器 URL: {settings.lemonade_base_url}")
        print(f"🤖 NPU 模型: {settings.lemonade_npu_model}")
        
        # 創建 Lemonade AI 服務
        ai_service = AIServiceFactory.create_service(
            AIProvider.LEMONADE,
            config=settings
        )
        
        print("✅ AI 服務創建成功")
        
        # 測試服務可用性
        if ai_service.is_available():
            print("✅ AI 服務可用")
            return True
        else:
            print("❌ AI 服務不可用")
            return False
            
    except Exception as e:
        print(f"❌ ClinicSim 整合測試失敗: {e}")
        return False

def main():
    """主測試函式"""
    print("Lemonade Server API 測試")
    print("=" * 50)
    
    # 設定
    base_url = "http://localhost:8000/api/v1"
    model_name = "Qwen-2.5-7B-Instruct-Hybrid"
    
    # 1. 測試伺服器連接
    if not test_server_connection(base_url):
        print("\n❌ 伺服器連接失敗，請確認 Lemonade Server 正在運行")
        return False
    
    # 2. 測試模型列表
    if not test_models_endpoint(base_url):
        print("\n❌ 模型列表獲取失敗")
        return False
    
    # 3. 測試聊天完成
    if not test_chat_completions(base_url, model_name):
        print("\n❌ 聊天完成測試失敗")
        return False
    
    # 4. 測試臨床場景
    if not test_clinical_scenario(base_url, model_name):
        print("\n⚠️ 臨床場景測試失敗，但基本功能正常")
    
    # 5. 測試 ClinicSim 整合
    if not test_clinicsim_integration():
        print("\n❌ ClinicSim 整合測試失敗")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Lemonade Server API 測試完成！")
    print("💡 現在可以啟動 ClinicSim-AI 使用 NPU 加速")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
