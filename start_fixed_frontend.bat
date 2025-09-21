@echo off
echo 🎨 啟動修復版 ClinicSim-AI 前端
echo =====================================

REM 檢查後端是否運行
echo 🔍 檢查後端服務...
python -c "import requests; requests.get('http://127.0.0.1:5001/health', timeout=5)" >nul 2>&1
if errorlevel 1 (
    echo ❌ 後端服務未運行
    echo 請先運行: python main.py
    pause
    exit /b 1
)

echo ✅ 後端服務正常

REM 啟動修復版前端
echo 🚀 啟動修復版前端...
echo 📍 前端將在瀏覽器中自動打開
echo 💡 按 Ctrl+C 停止服務
echo =====================================

streamlit run src/frontend/app_fixed.py --server.port 8502 --server.address 0.0.0.0

pause
