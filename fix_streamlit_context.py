#!/usr/bin/env python3
"""
修復 Streamlit 上下文問題
"""

import os
import sys
from pathlib import Path

def fix_streamlit_warnings():
    """修復 Streamlit 警告"""
    print("🔧 修復 Streamlit 上下文警告...")
    
    # 設置環境變數來抑制警告
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    
    # 創建 .streamlit 配置目錄
    streamlit_dir = Path.home() / '.streamlit'
    streamlit_dir.mkdir(exist_ok=True)
    
    # 創建配置文件
    config_content = """[browser]
gatherUsageStats = false

[server]
headless = true
enableCORS = false
enableXsrfProtection = false

[logger]
level = "error"
"""
    
    config_file = streamlit_dir / 'config.toml'
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"✅ 配置文件已創建: {config_file}")
    print("✅ Streamlit 警告已抑制")

def create_simple_launcher():
    """創建簡單的啟動器"""
    launcher_content = '''#!/usr/bin/env python3
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
'''
    
    with open('launch_app.py', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ 簡單啟動器已創建: launch_app.py")

def main():
    """主函式"""
    print("🚀 Streamlit 修復工具")
    print("=" * 50)
    
    fix_streamlit_warnings()
    create_simple_launcher()
    
    print("\n✅ 修復完成！")
    print("\n💡 現在您可以:")
    print("   1. 運行: python launch_app.py")
    print("   2. 或運行: streamlit run launch_app.py")
    print("   3. 或運行: start_fixed_frontend.bat")

if __name__ == "__main__":
    main()
