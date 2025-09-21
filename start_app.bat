@echo off
echo 🚀 啟動 ClinicSim-AI 應用程式...
echo.

REM 激活虛擬環境
call venv\Scripts\activate

echo 📡 啟動後端服務 (端口 8000)...
start "ClinicSim-AI Backend" cmd /k "python main.py"

echo ⏳ 等待後端服務啟動...
timeout /t 3 /nobreak > nul

echo 🖥️ 啟動前端應用 (端口 8501)...
start "ClinicSim-AI Frontend" cmd /k "streamlit run src/frontend/app.py"

echo.
echo ✅ 應用程式已啟動！
echo 📍 後端 API: http://localhost:8000
echo 🌐 前端應用: http://localhost:8501
echo.
echo 按任意鍵關閉此視窗...
pause > nul
