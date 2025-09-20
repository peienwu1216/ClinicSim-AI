#!/usr/bin/env python3
"""
測試運行腳本
提供不同類型的測試運行選項
"""

import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, description):
    """運行命令並顯示結果"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"執行命令: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.stdout:
            print("📤 標準輸出:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️ 錯誤輸出:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} 成功完成")
            return True
        else:
            print(f"❌ {description} 失敗 (退出碼: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ {description} 執行錯誤: {e}")
        return False

def run_unit_tests():
    """運行單元測試"""
    cmd = ["python", "-m", "pytest", "tests/test_basic_functionality.py", "-v", "--tb=short"]
    return run_command(cmd, "單元測試")

def run_integration_tests():
    """運行集成測試"""
    cmd = ["python", "-m", "pytest", "tests/test_api_endpoints.py", "-v", "--tb=short"]
    return run_command(cmd, "集成測試")

def run_all_tests():
    """運行所有測試"""
    cmd = ["python", "-m", "pytest", "tests/", "-v", "--tb=short"]
    return run_command(cmd, "所有測試")

def run_tests_with_coverage():
    """運行測試並生成覆蓋率報告"""
    cmd = ["python", "-m", "pytest", "tests/", "--cov=src", "--cov-report=html", "--cov-report=term"]
    return run_command(cmd, "測試覆蓋率分析")

def run_linting():
    """運行代碼檢查"""
    commands = [
        (["python", "-m", "flake8", "src/", "--max-line-length=120"], "Flake8 代碼檢查"),
        (["python", "-m", "black", "--check", "src/"], "Black 代碼格式檢查"),
        (["python", "-m", "mypy", "src/"], "MyPy 類型檢查")
    ]
    
    results = []
    for cmd, description in commands:
        results.append(run_command(cmd, description))
    
    return all(results)

def run_quick_tests():
    """運行快速測試（跳過慢速測試）"""
    cmd = ["python", "-m", "pytest", "tests/", "-v", "-m", "not slow", "--tb=short"]
    return run_command(cmd, "快速測試")

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="ClinicSim-AI 測試運行器")
    parser.add_argument("--type", choices=["unit", "integration", "all", "coverage", "lint", "quick"], 
                       default="all", help="測試類型")
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細輸出")
    
    args = parser.parse_args()
    
    print("🧪 ClinicSim-AI 測試運行器")
    print("=" * 60)
    
    success = False
    
    if args.type == "unit":
        success = run_unit_tests()
    elif args.type == "integration":
        success = run_integration_tests()
    elif args.type == "all":
        success = run_all_tests()
    elif args.type == "coverage":
        success = run_tests_with_coverage()
    elif args.type == "lint":
        success = run_linting()
    elif args.type == "quick":
        success = run_quick_tests()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 所有測試完成！")
        sys.exit(0)
    else:
        print("💥 測試失敗！")
        sys.exit(1)

if __name__ == "__main__":
    main()
