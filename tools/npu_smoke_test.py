#!/usr/bin/env python3
"""
NPU 煙霧測試腳本
測試 Lemonade OGA 在不同設備上的執行情況
"""

import sys
import time
import os
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config.settings import get_settings
from src.services.ai_service import AIServiceFactory, AIProvider

def test_device_info():
    """測試設備信息檢測"""
    print("=" * 60)
    print("🔍 設備信息檢測")
    print("=" * 60)
    
    try:
        from lemonade.api import get_device_info
        device_info = get_device_info()
        print(f"設備信息: {device_info}")
        
        # 檢查 NPU 可用性
        device_str = str(device_info).lower()
        has_npu = any(keyword in device_str for keyword in ["npu", "ryzen", "amd", "hybrid"])
        print(f"NPU 可用: {'是' if has_npu else '否'}")
        
        return device_info, has_npu
    except ImportError:
        print("❌ lemonade-sdk 未安裝")
        return None, False
    except Exception as e:
        print(f"❌ 無法獲取設備信息: {e}")
        return None, False

def test_sdk_mode():
    """測試 SDK 模式"""
    print("\n" + "=" * 60)
    print("🧪 SDK 模式測試")
    print("=" * 60)
    
    try:
        from lemonade.api import from_pretrained, get_device_info
        
        settings = get_settings()
        print(f"模型檢查點: {settings.lemonade_model_checkpoint}")
        print(f"Recipe: {settings.lemonade_recipe}")
        
        # 載入模型
        print("\n載入模型中...")
        t0 = time.time()
        model, tokenizer = from_pretrained(
            checkpoint=settings.lemonade_model_checkpoint,
            recipe=settings.lemonade_recipe
        )
        load_time = time.time() - t0
        print(f"載入時間: {load_time:.2f} 秒")
        
        # 獲取設備信息
        device_info = get_device_info()
        print(f"載入後設備信息: {device_info}")
        
        # 測試推理
        prompt = "You are a concise assistant. In one sentence, explain why recipes control device selection."
        print(f"\n測試提示: {prompt}")
        
        t0 = time.time()
        response = model.generate(prompt, max_new_tokens=80)
        infer_time = time.time() - t0
        
        print(f"推理時間: {infer_time:.2f} 秒")
        print(f"回應: {response[:200]}{'...' if len(response) > 200 else ''}")
        
        return True
        
    except Exception as e:
        print(f"❌ SDK 模式測試失敗: {e}")
        return False

def test_server_mode():
    """測試 Server 模式"""
    print("\n" + "=" * 60)
    print("🌐 Server 模式測試")
    print("=" * 60)
    
    try:
        settings = get_settings()
        if not settings.is_lemonade_server_mode():
            print("⚠️ 未配置 Server 模式，跳過測試")
            return True
        
        print(f"Server URL: {settings.lemonade_base_url}")
        print(f"API Key: {settings.lemonade_api_key}")
        print(f"模型名稱: {settings.get_effective_model_name()}")
        
        # 創建 AI 服務
        ai_service = AIServiceFactory.create_from_config(settings)
        
        # 測試可用性
        if ai_service.is_available():
            print("✅ Server 模式連接成功")
            
            # 測試聊天
            from src.models.conversation import Message, MessageRole
            messages = [
                Message(role=MessageRole.USER, content="Hello, can you confirm you're running on NPU/Hybrid?")
            ]
            
            t0 = time.time()
            response = ai_service.chat(messages, max_tokens=100)
            infer_time = time.time() - t0
            
            print(f"推理時間: {infer_time:.2f} 秒")
            print(f"回應: {response[:200]}{'...' if len(response) > 200 else ''}")
            
            return True
        else:
            print("❌ Server 模式連接失敗")
            return False
            
    except Exception as e:
        print(f"❌ Server 模式測試失敗: {e}")
        return False

def test_ai_service():
    """測試統一的 AI 服務"""
    print("\n" + "=" * 60)
    print("🤖 AI 服務測試")
    print("=" * 60)
    
    try:
        settings = get_settings()
        print(f"AI Provider: {settings.ai_provider}")
        print(f"模型檢查點: {settings.lemonade_model_checkpoint}")
        print(f"Recipe: {settings.lemonade_recipe}")
        print(f"Server 模式: {'是' if settings.is_lemonade_server_mode() else '否'}")
        
        # 創建 AI 服務
        ai_service = AIServiceFactory.create_from_config(settings)
        print(f"服務類型: {type(ai_service).__name__}")
        
        # 測試可用性
        if ai_service.is_available():
            print("✅ AI 服務可用")
            
            # 測試聊天
            from src.models.conversation import Message, MessageRole
            messages = [
                Message(role=MessageRole.USER, content="Test NPU inference with a short response.")
            ]
            
            t0 = time.time()
            response = ai_service.chat(messages, max_tokens=50)
            infer_time = time.time() - t0
            
            print(f"推理時間: {infer_time:.2f} 秒")
            print(f"回應: {response[:150]}{'...' if len(response) > 150 else ''}")
            
            return True
        else:
            print("❌ AI 服務不可用")
            return False
            
    except Exception as e:
        print(f"❌ AI 服務測試失敗: {e}")
        return False

def main():
    """主測試函式"""
    print("🚀 Lemonade OGA NPU 煙霧測試")
    print("=" * 60)
    
    # 顯示設定
    settings = get_settings()
    print(f"設定摘要:")
    print(f"  AI Provider: {settings.ai_provider}")
    print(f"  模型檢查點: {settings.lemonade_model_checkpoint}")
    print(f"  Recipe: {settings.lemonade_recipe}")
    print(f"  Server 模式: {'是' if settings.is_lemonade_server_mode() else '否'}")
    if settings.is_lemonade_server_mode():
        print(f"  Server URL: {settings.lemonade_base_url}")
    
    # 執行測試
    tests = [
        ("設備信息檢測", test_device_info),
        ("AI 服務測試", test_ai_service),
    ]
    
    # 根據模式添加特定測試
    if not settings.is_lemonade_server_mode():
        tests.insert(1, ("SDK 模式測試", test_sdk_mode))
    else:
        tests.insert(1, ("Server 模式測試", test_server_mode))
    
    results = []
    for test_name, test_func in tests:
        print(f"\n執行測試: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"結果: {'✅ 通過' if result else '❌ 失敗'}")
        except Exception as e:
            print(f"結果: ❌ 錯誤 - {e}")
            results.append((test_name, False))
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 測試總結")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {test_name}: {status}")
    
    print(f"\n總計: {passed}/{total} 測試通過")
    
    if passed == total:
        print("🎉 所有測試通過！NPU 配置正確。")
        return 0
    else:
        print("⚠️ 部分測試失敗，請檢查配置。")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
