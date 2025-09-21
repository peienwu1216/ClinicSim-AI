@echo off
echo 🚀 ClinicSim-AI 完整啟動腳本
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
    echo 正在安裝依賴項...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依賴項安裝失敗
        pause
        exit /b 1
    )
)

REM 運行診斷
echo 🔍 運行連接診斷...
python diagnose_connection.py
if errorlevel 1 (
    echo ❌ 診斷失敗
    pause
    exit /b 1
)

echo.
echo ✅ 診斷完成，系統正常
echo.
echo 請選擇啟動方式:
echo 1. 只啟動後端服務
echo 2. 只啟動前端服務  
echo 3. 同時啟動後端和前端 (推薦)
echo 4. 退出
echo.
set /p choice=請輸入選項 (1-4): 

if "%choice%"=="1" (
    echo 啟動後端服務...
    start "ClinicSim-AI Backend" cmd /k "python main.py"
    echo ✅ 後端服務已啟動
    echo 📍 後端地址: http://127.0.0.1:5001
) else if "%choice%"=="2" (
    echo 啟動前端服務...
    start "ClinicSim-AI Frontend" cmd /k "streamlit run src/frontend/app.py --server.port 8501 --server.address 0.0.0.0"
    echo ✅ 前端服務已啟動
    echo 📍 前端地址: http://localhost:8501
) else if "%choice%"=="3" (
    echo 同時啟動後端和前端...
    start "ClinicSim-AI Backend" cmd /k "python main.py"
    timeout /t 3 /nobreak >nul
    start "ClinicSim-AI Frontend" cmd /k "streamlit run src/frontend/app.py --server.port 8501 --server.address 0.0.0.0"
    echo ✅ 後端和前端服務已啟動
    echo 📍 後端地址: http://127.0.0.1:5001
    echo 📍 前端地址: http://localhost:8501
) else if "%choice%"=="4" (
    echo 👋 再見！
    exit /b 0
) else (
    echo ❌ 無效選項
    pause
    exit /b 1
)

echo.
echo 💡 提示:
echo - 後端服務必須先啟動才能使用前端
echo - 如果遇到連接問題，請運行 diagnose_connection.py
echo - 按 Ctrl+C 可以停止服務
echo.
pause
