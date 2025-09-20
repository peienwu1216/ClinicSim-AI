"""
ClinicSim-AI 新版本 Streamlit 應用程式入口
"""

import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from src.frontend import create_streamlit_app


def main():
    """主函式"""
    print("🚀 啟動 ClinicSim-AI 新版本前端...")
    print("📍 請確保後端伺服器正在運行 (python main.py)")
    print("=" * 50)
    
    app = create_streamlit_app()
    app.run()


if __name__ == "__main__":
    main()
