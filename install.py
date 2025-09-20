#!/usr/bin/env python3
"""
ClinicSim-AI 環境安裝腳本
支持多平台環境設置
"""

import os
import sys
import subprocess
import platform

def detect_environment():
    """檢測當前環境"""
    system = platform.system().lower()
    python_version = sys.version_info
    
    print(f"🔍 檢測到環境: {system} (Python {python_version.major}.{python_version.minor})")
    
    return system, python_version

def install_requirements(env_type):
    """安裝指定環境的依賴"""
    requirements_file = f"requirements-{env_type}.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ 找不到 {requirements_file}")
        return False
    
    print(f"📦 安裝 {env_type} 環境依賴...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ], check=True)
        print(f"✅ {env_type} 環境安裝完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 安裝失敗: {e}")
        return False

def main():
    """主函式"""
    print("🚀 ClinicSim-AI 環境安裝器")
    print("=" * 50)
    
    # 檢測環境
    system, python_version = detect_environment()
    
    # 推薦安裝方案
    if system == "windows":
        print("💡 檢測到 Windows 環境")
        print("📋 推薦安裝選項:")
        print("   1. 開發環境 (包含所有開發工具)")
        print("   2. Windows 優化環境 (解決兼容性問題)")
        print("   3. 基礎環境 (僅核心依賴)")
        
        choice = input("請選擇 (1/2/3): ").strip()
        
        if choice == "1":
            install_requirements("dev")
        elif choice == "2":
            install_requirements("windows")
        elif choice == "3":
            install_requirements("base")
        else:
            print("❌ 無效選擇")
            return False
            
    elif system == "darwin":  # macOS
        print("💡 檢測到 macOS 環境")
        install_requirements("dev")
        
    else:  # Linux (可能是 Lemonade)
        print("💡 檢測到 Linux 環境")
        print("📋 推薦安裝選項:")
        print("   1. 生產環境 (Lemonade Server)")
        print("   2. 基礎環境 (僅核心依賴)")
        
        choice = input("請選擇 (1/2): ").strip()
        
        if choice == "1":
            install_requirements("lemonade")
        elif choice == "2":
            install_requirements("base")
        else:
            print("❌ 無效選擇")
            return False
    
    print("\n🎉 安裝完成！")
    print("📍 下一步:")
    print("   - 測試系統: python quick_test.py")
    print("   - 啟動服務器: python main.py")
    print("   - 啟動前端: streamlit run app_new.py")
    
    return True

if __name__ == "__main__":
    main()
