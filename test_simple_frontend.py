#!/usr/bin/env python3
"""
簡化的前端測試 - 避免 Streamlit 上下文問題
"""

import requests
import json
import time

def test_simple_chat():
    """測試簡單的對話功能"""
    print("🚀 測試簡單對話功能")
    print("=" * 50)
    
    # 測試後端連接
    try:
        response = requests.get("http://127.0.0.1:5001/health", timeout=5)
        if response.status_code == 200:
            print("✅ 後端服務正常")
        else:
            print("❌ 後端服務異常")
            return
    except Exception as e:
        print(f"❌ 無法連接到後端: {e}")
        return
    
    # 模擬對話
    messages = []
    
    # 第一輪對話
    print("\n👤 用戶: 你好")
    messages.append({"role": "user", "content": "你好"})
    
    try:
        response = requests.post("http://127.0.0.1:5001/ask_patient", 
                               json={"history": messages, "case_id": "case_1"}, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            ai_reply = data.get("reply", "")
            coverage = data.get("coverage", 0)
            
            print(f"🤖 AI: {ai_reply}")
            print(f"📊 覆蓋率: {coverage}%")
            
            messages.append({"role": "assistant", "content": ai_reply})
        else:
            print(f"❌ API 錯誤: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 對話失敗: {e}")
        return
    
    # 第二輪對話
    print("\n👤 用戶: 你哪裡不舒服？")
    messages.append({"role": "user", "content": "你哪裡不舒服？"})
    
    try:
        response = requests.post("http://127.0.0.1:5001/ask_patient", 
                               json={"history": messages, "case_id": "case_1"}, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            ai_reply = data.get("reply", "")
            coverage = data.get("coverage", 0)
            
            print(f"🤖 AI: {ai_reply}")
            print(f"📊 覆蓋率: {coverage}%")
            
            messages.append({"role": "assistant", "content": ai_reply})
        else:
            print(f"❌ API 錯誤: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 對話失敗: {e}")
        return
    
    print("\n✅ 對話測試完成！")
    print("💡 如果這個測試成功，說明後端工作正常")
    print("💡 前端問題可能是 Streamlit 的上下文管理問題")

if __name__ == "__main__":
    test_simple_chat()
