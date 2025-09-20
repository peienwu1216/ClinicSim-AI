#!/usr/bin/env python3
"""
Notion 同步使用範例
展示如何使用 Notion 整合功能
"""

import os
import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.report_service import ReportService
from src.config.settings import get_settings


def example_auto_sync():
    """範例：自動同步報告到 Notion"""
    print("📝 自動同步範例")
    
    # 初始化服務
    settings = get_settings()
    report_service = ReportService(settings)
    
    # 檢查 Notion 功能是否啟用
    if not settings.notion_enabled:
        print("❌ Notion 功能未啟用 - 請設定 .env 檔案")
        return
    
    print("✅ 自動同步功能已整合到報告生成流程中")


def example_manual_sync():
    """範例：手動同步現有報告到 Notion"""
    print("\n📝 手動同步範例")
    
    # 初始化服務
    settings = get_settings()
    report_service = ReportService(settings)
    
    # 檢查 Notion 功能是否啟用
    if not settings.notion_enabled:
        print("❌ Notion 功能未啟用 - 請設定 .env 檔案")
        return
    
    # 尋找現有的報告檔案
    report_dir = Path("report_history")
    if not report_dir.exists():
        print("❌ 沒有找到 report_history 目錄")
        return
    
    report_files = list(report_dir.glob("*.md"))
    if not report_files:
        print("❌ 沒有找到報告檔案")
        return
    
    # 選擇最新的檔案
    latest_report = max(report_files, key=lambda f: f.stat().st_mtime)
    print(f"📄 找到報告檔案: {latest_report.name}")
    
    # 手動同步到 Notion
    page_id = report_service.sync_existing_report_to_notion(
        file_path=str(latest_report),
        page_title="手動同步測試報告"
    )
    
    if page_id:
        print(f"✅ 同步成功！頁面 ID: {page_id}")
    else:
        print("❌ 同步失敗")


def example_api_usage():
    """範例：使用 API 端點同步報告"""
    print("\n📝 API 使用範例")
    print("🌐 端點：POST /sync_report_to_notion")
    print("📋 請求：{\"file_path\": \"report_history/xxx.md\", \"page_title\": \"標題\"}")
    print("🔧 測試：curl -X POST http://localhost:5001/sync_report_to_notion -H \"Content-Type: application/json\" -d '{\"file_path\": \"report_history/xxx.md\", \"page_title\": \"測試\"}'")


def main():
    """主函式"""
    print("🚀 ClinicSim-AI Notion 整合範例")
    
    # 顯示設定狀態
    settings = get_settings()
    print(f"📋 設定狀態：Notion={settings.notion_enabled}, API Key={'已設定' if settings.notion_api_key else '未設定'}")
    
    # 執行範例
    example_auto_sync()
    example_manual_sync()
    example_api_usage()
    
    print("\n📖 詳細設定請參考 NOTION_SETUP.md")


if __name__ == "__main__":
    main()
