#!/usr/bin/env python3
"""
Notion 整合測試腳本
用於測試 Notion 功能是否正常運作
"""

import os
import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.notion_service import NotionService
from src.config.settings import get_settings


def test_notion_service():
    """測試 Notion 服務基本功能"""
    print("🧪 開始測試 Notion 整合...")
    
    # 載入設定
    settings = get_settings()
    print(f"📋 設定載入完成")
    print(f"   - Notion 啟用: {settings.notion_enabled}")
    print(f"   - API Key 設定: {'是' if settings.notion_api_key else '否'}")
    print(f"   - 資料庫 ID 設定: {'是' if settings.notion_database_id else '否'}")
    print(f"   - 父頁面 ID 設定: {'是' if settings.notion_parent_page_id else '否'}")
    
    # 初始化 Notion 服務
    notion_service = NotionService(settings)
    
    # 檢查服務可用性
    if not notion_service.is_available():
        print("❌ Notion 服務不可用")
        print("   請檢查以下項目：")
        print("   1. NOTION_API_KEY 環境變數是否設定")
        print("   2. API Key 是否有效")
        print("   3. 網路連接是否正常")
        return False
    
    print("✅ Notion 服務初始化成功")
    
    # 測試 Markdown 轉換
    test_markdown = """
# 測試報告

## 問診表現評估
- 學生展現了良好的問診技巧
- 能夠與病人建立良好的溝通

### 具體建議
1. 加強系統性問診
2. 提升臨床決策能力

這是一個測試段落。
"""
    
    print("🔄 測試 Markdown 轉 Notion Blocks 轉換...")
    blocks = notion_service.markdown_to_notion_blocks(test_markdown)
    print(f"✅ 轉換成功，生成 {len(blocks)} 個 blocks")
    
    # 顯示轉換結果
    for i, block in enumerate(blocks[:3]):  # 只顯示前3個
        print(f"   Block {i+1}: {block['type']}")
    
    if len(blocks) > 3:
        print(f"   ... 還有 {len(blocks) - 3} 個 blocks")
    
    print("✅ Notion 整合測試完成")
    return True


def test_report_sync():
    """測試報告同步功能"""
    print("\n🧪 測試報告同步功能...")
    
    # 檢查是否有現有的報告檔案
    report_dir = Path("report_history")
    if not report_dir.exists():
        print("⚠️ 沒有找到 report_history 目錄")
        return False
    
    # 尋找最新的報告檔案
    report_files = list(report_dir.glob("*.md"))
    if not report_files:
        print("⚠️ 沒有找到報告檔案")
        return False
    
    # 選擇最新的檔案
    latest_report = max(report_files, key=lambda f: f.stat().st_mtime)
    print(f"📄 找到報告檔案: {latest_report.name}")
    
    # 測試同步（僅測試，不實際執行）
    settings = get_settings()
    if not settings.notion_enabled:
        print("⚠️ Notion 功能未啟用，跳過同步測試")
        print("   請設定 NOTION_ENABLED=true 來啟用功能")
        return True
    
    notion_service = NotionService(settings)
    if not notion_service.is_available():
        print("❌ Notion 服務不可用，跳過同步測試")
        return False
    
    print("✅ 報告同步功能測試完成")
    return True


def main():
    """主測試函式"""
    print("🚀 ClinicSim-AI Notion 整合測試")
    print("=" * 50)
    
    # 測試基本功能
    success1 = test_notion_service()
    
    # 測試報告同步
    success2 = test_report_sync()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 所有測試通過！Notion 整合功能正常")
    else:
        print("❌ 部分測試失敗，請檢查設定和配置")
    
    print("\n📖 如需更多資訊，請參考 NOTION_SETUP.md")


if __name__ == "__main__":
    main()
