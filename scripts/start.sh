#!/bin/bash

# ClinicSim-AI 啟動腳本

echo "🧑‍⚕️ ClinicSim-AI - 臨床技能教練"
echo "=================================="

# 檢查Python環境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安裝，請先安裝Python3"
    exit 1
fi

# 檢查依賴
echo "📦 檢查依賴..."
if ! python3 -c "import streamlit, requests" &> /dev/null; then
    echo "⚠️  缺少必要依賴，正在安裝..."
    pip install streamlit requests
fi

# 檢查後端服務
echo "🔍 檢查後端服務..."
if ! curl -s http://127.0.0.1:5001/health &> /dev/null; then
    echo "⚠️  後端服務未運行"
    echo "💡 請在另一個終端運行: python main.py"
    echo "⏳ 等待5秒後繼續啟動前端..."
    sleep 5
fi

# 啟動前端
echo "🚀 啟動ClinicSim-AI前端..."
echo "📍 瀏覽器將自動開啟: http://localhost:8501"
echo "🛑 按 Ctrl+C 停止服務"
echo ""

streamlit run app.py
