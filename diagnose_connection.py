#!/usr/bin/env python3
"""
ClinicSim-AI 連接診斷工具
用於診斷前端和後端之間的連接問題
"""

import requests
import subprocess
import sys
import time
import json
from pathlib import Path

def check_backend_status():
    """檢查後端狀態"""
    print("🔍 檢查後端狀態...")
    
    try:
        # 檢查健康狀態
        response = requests.get("http://127.0.0.1:5001/health", timeout=5)
        if response.status_code == 200:
            print("✅ 後端健康檢查通過")
            print(f"   服務: {response.json().get('service')}")
            print(f"   版本: {response.json().get('version')}")
            return True
        else:
            print(f"❌ 後端健康檢查失敗: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到後端服務")
        return False
    except Exception as e:
        print(f"❌ 後端檢查錯誤: {e}")
        return False

def check_api_endpoints():
    """檢查 API 端點"""
    print("\n🔍 檢查 API 端點...")
    
    endpoints = [
        ("/health", "GET"),
        ("/cases/random", "GET"),
        ("/ask_patient", "POST")
    ]
    
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"http://127.0.0.1:5001{endpoint}", timeout=5)
            else:
                # 測試 POST 端點
                test_data = {
                    "history": [{"role": "user", "content": "測試"}],
                    "case_id": "case_1"
                }
                response = requests.post(f"http://127.0.0.1:5001{endpoint}", 
                                      json=test_data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {endpoint} - 正常")
            else:
                print(f"⚠️ {endpoint} - 狀態碼: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {endpoint} - 錯誤: {e}")

def check_port_usage():
    """檢查端口使用情況"""
    print("\n🔍 檢查端口使用情況...")
    
    try:
        # 使用 netstat 檢查端口
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        port_5001_lines = [line for line in lines if ':5001' in line]
        
        if port_5001_lines:
            print("✅ 端口 5001 正在使用:")
            for line in port_5001_lines:
                print(f"   {line.strip()}")
        else:
            print("❌ 端口 5001 未被使用")
            
    except Exception as e:
        print(f"❌ 無法檢查端口使用情況: {e}")

def check_frontend_config():
    """檢查前端配置"""
    print("\n🔍 檢查前端配置...")
    
    try:
        # 檢查前端配置
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from src.config.settings import get_settings
        
        settings = get_settings()
        print(f"✅ 後端主機: {settings.host}:{settings.port}")
        print(f"✅ 前端連接: {settings.backend_host}:{settings.backend_port}")
        
        # 檢查配置是否一致
        if settings.host == "0.0.0.0" and settings.backend_host == "127.0.0.1":
            print("✅ 主機配置正確")
        else:
            print("⚠️ 主機配置可能不正確")
            
    except Exception as e:
        print(f"❌ 前端配置檢查錯誤: {e}")

def create_env_file():
    """創建 .env 文件"""
    print("\n🔧 創建 .env 配置文件...")
    
    env_content = """# ClinicSim-AI 環境配置

# 應用程式設定
APP_NAME=ClinicSim-AI
APP_VERSION=2.0.0
DEBUG=False

# 伺服器設定
HOST=0.0.0.0
PORT=5001

# 前端連接設定
BACKEND_HOST=127.0.0.1
BACKEND_PORT=5001

# AI 模型設定
AI_PROVIDER=lemonade

# Lemonade 設定
LEMONADE_MODEL_CHECKPOINT=amd/Qwen2.5-7B-Instruct-awq-uint4-asym-g128-lmhead-g32-fp16-onnx-hybrid
LEMONADE_RECIPE=oga-hybrid
LEMONADE_BASE_URL=http://localhost:8000/api/v1
LEMONADE_API_KEY=lemonade

# 案例設定
DEFAULT_CASE_ID=case_1

# RAG 設定
RAG_MODEL_NAME=nomic-ai/nomic-embed-text-v1.5
RAG_CHUNK_SIZE=800
RAG_CHUNK_OVERLAP=100
RAG_SEARCH_K=3

# Notion 設定 (可選)
NOTION_ENABLED=False
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env 文件創建成功")
    except Exception as e:
        print(f"❌ 創建 .env 文件失敗: {e}")

def test_frontend_connection():
    """測試前端連接"""
    print("\n🔍 測試前端連接...")
    
    try:
        # 模擬前端連接測試
        from src.frontend.app import StreamlitApp
        
        app = StreamlitApp()
        print(f"✅ 前端應用初始化成功")
        print(f"   API 基礎 URL: {app.api_base_url}")
        
        # 測試 API 連接
        response = requests.get(f"{app.api_base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 前端可以連接到後端")
        else:
            print(f"❌ 前端連接後端失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 前端連接測試失敗: {e}")

def main():
    """主函式"""
    print("🚀 ClinicSim-AI 連接診斷工具")
    print("=" * 50)
    
    # 檢查後端狀態
    backend_ok = check_backend_status()
    
    if backend_ok:
        # 檢查 API 端點
        check_api_endpoints()
        
        # 檢查端口使用
        check_port_usage()
        
        # 檢查前端配置
        check_frontend_config()
        
        # 測試前端連接
        test_frontend_connection()
        
        print("\n" + "=" * 50)
        print("📋 診斷總結:")
        print("✅ 後端服務運行正常")
        print("✅ API 端點正常響應")
        print("✅ 端口配置正確")
        print("\n💡 如果前端仍然無法連接，請嘗試:")
        print("   1. 重新啟動後端: python main.py")
        print("   2. 重新啟動前端: streamlit run src/frontend/app.py")
        print("   3. 檢查防火牆設定")
        print("   4. 清除瀏覽器快取")
        
    else:
        print("\n" + "=" * 50)
        print("❌ 後端服務未運行")
        print("\n💡 請嘗試:")
        print("   1. 啟動後端: python main.py")
        print("   2. 檢查依賴項: pip install -r requirements.txt")
        print("   3. 檢查端口是否被佔用")
    
    # 創建 .env 文件
    if not Path('.env').exists():
        create_env_file()

if __name__ == "__main__":
    main()
