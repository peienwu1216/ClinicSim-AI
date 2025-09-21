@echo off
echo 🎨 啟動 ClinicSim-AI 前端服務
echo =====================================

REM 檢查 Python 是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安裝或未添加到 PATH
    pause
    exit /b 1
)

REM 檢查 Streamlit 是否安裝
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ❌ Streamlit 未安裝
    echo 請運行: pip install streamlit
    pause
    exit /b 1
)

REM 檢查後端是否運行
echo 🔍 檢查後端服務...
python -c "import requests; requests.get('http://127.0.0.1:5001/health', timeout=5)" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 後端服務未運行
    echo 請先運行 start_backend.bat 啟動後端服務
    echo 或手動運行: python main.py
    echo.
    echo 是否繼續啟動前端？(y/n)
    set /p choice=
    if /i not "%choice%"=="y" exit /b 1
)

REM 啟動前端服務
echo ✅ 啟動前端服務...
echo 📍 前端將在瀏覽器中自動打開
echo 💡 按 Ctrl+C 停止服務
echo =====================================

streamlit run src/frontend/app.py --server.port 8501 --server.address 0.0.0.0

pause
