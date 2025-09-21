@echo off
echo 🧑‍⚕️ ClinicSim-AI NPU 加速啟動器
echo ================================================

REM 檢查 Python 是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安裝或不在 PATH 中
    pause
    exit /b 1
)

REM 設定環境變數
set AI_PROVIDER=lemonade_npu
set LEMONADE_BASE_URL=http://localhost:8000/api/v1
set LEMONADE_NPU_MODEL=Qwen-2.5-7B-Instruct-Hybrid
set LEMONADE_API_KEY=lemonade

echo ✅ 環境變數設定完成
echo    AI_PROVIDER: %AI_PROVIDER%
echo    LEMONADE_BASE_URL: %LEMONADE_BASE_URL%
echo    LEMONADE_NPU_MODEL: %LEMONADE_NPU_MODEL%
echo    LEMONADE_API_KEY: %LEMONADE_API_KEY%

echo.
echo 🚀 啟動 ClinicSim-AI (NPU 加速模式)...
echo.

REM 啟動應用程式
python main.py

pause
