#!/bin/bash

# ClinicSim-AI 新版本啟動腳本

echo "🚀 啟動 ClinicSim-AI 新版本架構..."
echo "=================================="

# 檢查 Python 版本
python_version=$(python3 --version 2>&1)
echo "Python 版本: $python_version"

# 檢查虛擬環境
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 虛擬環境已啟用: $VIRTUAL_ENV"
else
    echo "⚠️  建議在虛擬環境中運行"
    echo "   啟動虛擬環境: source venv/bin/activate"
fi

# 檢查依賴
echo ""
echo "📦 檢查依賴套件..."
if python3 -c "import streamlit, flask, pydantic, langchain" 2>/dev/null; then
    echo "✅ 核心依賴已安裝"
else
    echo "❌ 缺少依賴套件，請執行: pip install -r requirements.txt"
    exit 1
fi

# 檢查 RAG 索引
echo ""
echo "🔍 檢查 RAG 索引..."
if [ -d "faiss_index" ] && [ -f "faiss_index/index.faiss" ]; then
    echo "✅ RAG 索引已存在"
else
    echo "⚠️  RAG 索引不存在，正在建立..."
    python3 build_index.py
fi

# 檢查配置文件
echo ""
echo "⚙️  檢查配置文件..."
if [ -f ".env" ]; then
    echo "✅ 找到 .env 配置文件"
else
    echo "⚠️  未找到 .env 文件，將使用預設配置"
fi

# 啟動後端
echo ""
echo "🔧 啟動後端服務..."
echo "   後端將在 http://localhost:5001 運行"
python3 main.py &
BACKEND_PID=$!

# 等待後端啟動
sleep 3

# 檢查後端是否正常啟動
if curl -s http://localhost:5001/health > /dev/null; then
    echo "✅ 後端服務已啟動"
else
    echo "❌ 後端服務啟動失敗"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# 啟動前端
echo ""
echo "🎨 啟動前端應用程式..."
echo "   前端將在 http://localhost:8501 運行"
echo "   按 Ctrl+C 停止服務"
echo ""

# 清理函數
cleanup() {
    echo ""
    echo "🛑 正在停止服務..."
    kill $BACKEND_PID 2>/dev/null
    echo "✅ 服務已停止"
    exit 0
}

# 設定信號處理
trap cleanup SIGINT SIGTERM

# 啟動前端
streamlit run app_new.py --server.port 8501 --server.address localhost

# 如果前端停止，也停止後端
cleanup
