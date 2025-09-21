#!/usr/bin/env python3
"""
ClinicSim-AI NPU 加速啟動腳本
自動設定環境變數並啟動 NPU 加速版本
"""

import os
import sys
import subprocess
from pathlib import Path

def set_npu_environment():
    """設定 NPU 環境變數"""
    print("🔧 設定 NPU 環境變數...")
    
    # 設定 NPU 相關環境變數
    os.environ["AI_PROVIDER"] = "lemonade_npu"
    os.environ["LEMONADE_BASE_URL"] = "http://localhost:8000/api/v1"
    os.environ["LEMONADE_NPU_MODEL"] = "Qwen-2.5-7B-Instruct-Hybrid"
    os.environ["LEMONADE_API_KEY"] = "lemonade"
    
    print("✅ NPU 環境變數設定完成")
    print(f"   AI_PROVIDER: {os.environ.get('AI_PROVIDER')}")
    print(f"   LEMONADE_BASE_URL: {os.environ.get('LEMONADE_BASE_URL')}")
    print(f"   LEMONADE_NPU_MODEL: {os.environ.get('LEMONADE_NPU_MODEL')}")
    print(f"   LEMONADE_API_KEY: {os.environ.get('LEMONADE_API_KEY')}")

def check_dependencies():
    """檢查依賴項"""
    print("\n🔍 檢查依賴項...")
    
    try:
        import lemonade
        print("✅ lemonade-sdk 已安裝")
        return True
    except ImportError:
        print("❌ lemonade-sdk 未安裝")
        print("請執行: pip install lemonade-sdk")
        return False

def run_npu_test():
    """運行 NPU 測試"""
    print("\n🧪 運行 NPU 加速測試...")
    
    try:
        result = subprocess.run([
            sys.executable, "test_npu_simple.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        print(result.stdout)
        if result.stderr:
            print("錯誤輸出:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 測試執行失敗: {e}")
        return False

def start_application():
    """啟動應用程式"""
    print("\n🚀 啟動 ClinicSim-AI (NPU 加速模式)...")
    
    try:
        # 啟動主應用程式
        subprocess.run([sys.executable, "main.py"], cwd=Path(__file__).parent)
    except KeyboardInterrupt:
        print("\n👋 應用程式已停止")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")

def main():
    """主函式"""
    print("🧑‍⚕️ ClinicSim-AI NPU 加速啟動器")
    print("=" * 50)
    
    # 1. 設定環境變數
    set_npu_environment()
    
    # 2. 檢查依賴項
    if not check_dependencies():
        print("\n❌ 依賴項檢查失敗，請先安裝 lemonade-sdk")
        return False
    
    # 3. 運行測試
    print("\n是否要運行 NPU 加速測試？(y/n): ", end="")
    if input().lower().startswith('y'):
        if not run_npu_test():
            print("\n❌ NPU 測試失敗，請檢查設定")
            return False
        print("\n✅ NPU 測試通過")
    
    # 4. 啟動應用程式
    print("\n是否要啟動應用程式？(y/n): ", end="")
    if input().lower().startswith('y'):
        start_application()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
