#!/usr/bin/env python3
"""
簡單的 Streamlit 啟動器
"""

import os
import sys
from pathlib import Path

# 設置環境變數
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

# 添加路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# 導入並運行應用
if __name__ == "__main__":
    import streamlit as st
    from src.frontend.app import main
    main()
