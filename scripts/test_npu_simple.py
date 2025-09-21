#!/usr/bin/env python3
"""
簡化的 NPU 測試腳本（無 emoji）
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

def test_chat_completion(base_url: str, model_name: str):
    """測試聊天完成功能"""
    print(f"\n測試聊天完成功能...")
    print(f"使用模型: {model_name}")
    
    try:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": "你好，請簡短介紹一下自己"}
            ],
            "stream": False
        }
        
        print("發送請求...")
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
            content = result['choices'][0]['message']['content']
            print(f"聊天完成請求成功")
            print(f"回應時間: {response_time:.2f} 秒")
            # 安全地處理中文字符
            try:
                safe_content = content[:100].encode('utf-8', errors='ignore').decode('utf-8')
                print(f"回應內容: {safe_content}...")
            except:
                print("回應內容: [包含特殊字符，已省略顯示]")
            return True
        else:
            print(f"聊天完成請求失敗: {response.status_code}")
            print(f"回應內容: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"聊天完成請求失敗: {e}")
        return False

def main():
    """主測試函式"""
    print("NPU 測試")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api/v1"
    model_name = "Qwen-2.5-7B-Instruct-Hybrid"
    
    # 測試伺服器連接
    if not test_server_connection(base_url):
        print("伺服器連接失敗，請確認 Lemonade Server 正在運行")
        return False
    
    # 測試聊天功能
    if not test_chat_completion(base_url, model_name):
        print("聊天功能測試失敗")
        return False
    
    print("\nNPU 測試完成！")
    print("現在可以啟動 ClinicSim-AI 使用 NPU 加速")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
