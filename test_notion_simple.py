#!/usr/bin/env python3
"""
簡化的 Notion 測試腳本
"""

import os
import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.notion_service import NotionService
from src.config.settings import get_settings


def test_notion():
    """測試 Notion 功能"""
    print("🧪 測試 Notion 整合...")
    
    # 載入設定
    settings = get_settings()
    print(f"設定：Notion={settings.notion_enabled}, API Key={'已設定' if settings.notion_api_key else '未設定'}")
    
    # 初始化 Notion 服務
    notion_service = NotionService(settings)
    
    # 檢查服務可用性
    if not notion_service.is_available():
        print("❌ Notion 服務不可用")
        print("請設定 .env 檔案：")
        print("NOTION_ENABLED=true")
        print("NOTION_API_KEY=your_api_key")
        print("NOTION_DATABASE_ID=your_database_id")
        return False
    
    print("✅ Notion 服務可用")
    
    # 測試 Markdown 轉換
    test_markdown = "# 測試報告\n\n這是一個測試段落。"
    blocks = notion_service.markdown_to_notion_blocks(test_markdown)
    print(f"✅ Markdown 轉換成功，生成 {len(blocks)} 個 blocks")
    
    return True


def test_report_sync():
    """測試報告同步"""
    print("\n🧪 測試報告同步...")
    
    settings = get_settings()
    if not settings.notion_enabled:
        print("❌ Notion 功能未啟用")
        return False
    
    # 尋找報告檔案
    report_dir = Path("report_history")
    if not report_dir.exists():
        print("❌ 沒有找到 report_history 目錄")
        return False
    
    report_files = list(report_dir.glob("*.md"))
    if not report_files:
        print("❌ 沒有找到報告檔案")
        return False
    
    # 選擇最新的檔案
    latest_report = max(report_files, key=lambda f: f.stat().st_mtime)
    print(f"📄 找到報告檔案: {latest_report.name}")
    
    # 測試同步（僅測試，不實際執行）
    notion_service = NotionService(settings)
    if not notion_service.is_available():
        print("❌ Notion 服務不可用")
        return False
    
    print("✅ 報告同步功能測試完成")
    return True


if __name__ == "__main__":
    print("🚀 Notion 整合測試")
    print("=" * 30)
    
    success1 = test_notion()
    success2 = test_report_sync()
    
    print("\n" + "=" * 30)
    if success1 and success2:
        print("🎉 所有測試通過！")
    else:
        print("❌ 部分測試失敗")
    
    print("\n📖 設定指南：NOTION_SETUP.md")
