@echo off
echo 🚀 啟動 ClinicSim-AI 後端服務
echo =====================================

REM 檢查 Python 是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安裝或未添加到 PATH
    pause
    exit /b 1
)

REM 檢查依賴項
echo 📦 檢查依賴項...
python -c "import flask, requests, streamlit" >nul 2>&1
if errorlevel 1 (
    echo ❌ 缺少必要的依賴項
    echo 請運行: pip install -r requirements.txt
    pause
    exit /b 1
)

REM 啟動後端服務
echo ✅ 啟動後端服務...
echo 📍 後端將在 http://127.0.0.1:5001 運行
echo 💡 按 Ctrl+C 停止服務
echo =====================================

python main.py

pause
