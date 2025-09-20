"""
ClinicSim-AI 主應用程式入口
"""

import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from src.api import create_app
from src.config import get_settings


def main():
    """主函式"""
    # 載入設定
    settings = get_settings()
    
    # 創建 Flask 應用程式
    app = create_app()
    
    # 啟動伺服器
    print(f"🚀 ClinicSim-AI v{settings.app_version} 正在啟動...")
    print(f"📍 伺服器地址: http://{settings.host}:{settings.port}")
    print(f"🔧 除錯模式: {'啟用' if settings.debug else '停用'}")
    print(f"🤖 AI 提供者: {settings.ai_provider}")
    
    if settings.ai_provider == "ollama":
        print(f"   Ollama 主機: {settings.ollama_host}")
        print(f"   Ollama 模型: {settings.ollama_model}")
    
    print("=" * 50)
    
    try:
        app.run(
            host=settings.host,
            port=settings.port,
            debug=settings.debug
        )
    except KeyboardInterrupt:
        print("\n👋 ClinicSim-AI 已停止")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
