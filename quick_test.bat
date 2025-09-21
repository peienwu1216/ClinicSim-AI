@echo off
echo 🧪 ClinicSim-AI 快速測試
echo =====================================

echo 1. 測試後端連接...
python test_simple_frontend.py

echo.
echo 2. 如果上述測試成功，請嘗試:
echo    - 運行修復版前端: start_fixed_frontend.bat
echo    - 或運行原始前端: streamlit run src/frontend/app.py
echo.
echo 3. 如果仍有問題，請檢查:
echo    - 瀏覽器控制台是否有錯誤
echo    - 防火牆設定
echo    - 清除瀏覽器快取

pause
