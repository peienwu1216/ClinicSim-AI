#!/usr/bin/env python3
"""
快速測試腳本 - 測試 ClinicSim-AI 基本功能
使用方法: python quick_test.py
"""

import requests
import json

def test_server():
    """測試服務器基本功能"""
    base_url = "http://127.0.0.1:5001"
    
    print("🔍 測試 ClinicSim-AI 系統...")
    
    # 1. 健康檢查
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 服務器健康檢查: 正常")
        else:
            print(f"❌ 服務器健康檢查: 失敗 ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ 服務器連接失敗: {e}")
        print("💡 請確保服務器正在運行: python main.py")
        return False
    
    # 2. 測試對話功能
    try:
        response = requests.post(
            f"{base_url}/ask_patient",
            json={
                "history": [{"role": "user", "content": "你好，請問你哪裡不舒服？"}],
                "case_id": "case_chest_pain_acs_01"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_reply = data.get("reply", "")
            coverage = data.get("coverage", 0)
            print(f"✅ AI 對話功能: 正常 (覆蓋率: {coverage}%)")
            print(f"   AI 回應: {ai_reply[:50]}...")
        else:
            print(f"❌ AI 對話功能: 失敗 ({response.status_code})")
    except Exception as e:
        print(f"❌ AI 對話功能: 錯誤 - {e}")
    
    # 3. 測試報告生成
    try:
        test_conversation = [
            {"role": "user", "content": "你好，請問你哪裡不舒服？"},
            {"role": "assistant", "content": "我胸口很痛，痛了一個小時了"},
            {"role": "user", "content": "什麼時候開始的？"},
            {"role": "assistant", "content": "今天下午開車時突然開始的"}
        ]
        
        response = requests.post(
            f"{base_url}/get_feedback_report",
            json={
                "full_conversation": test_conversation,
                "case_id": "case_chest_pain_acs_01"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            report = data.get("report_text", "")
            print(f"✅ 報告生成功能: 正常 (報告長度: {len(report)} 字)")
        else:
            print(f"❌ 報告生成功能: 失敗 ({response.status_code})")
    except Exception as e:
        print(f"❌ 報告生成功能: 錯誤 - {e}")
    
    print("\n🎉 測試完成！")
    print("📍 前端界面: http://127.0.0.1:8502")
    print("📍 API 端點: http://127.0.0.1:5001")
    
    return True

if __name__ == "__main__":
    test_server()
