#!/bin/bash

# ClinicSim-AI Docker 啟動腳本

echo "🧑‍⚕️ ClinicSim-AI - 臨床技能教練"
echo "=================================="

# 等待Ollama服務啟動
echo "⏳ 等待Ollama服務啟動..."
timeout=60
counter=0
while ! curl -s http://ollama:11434/api/tags &> /dev/null; do
    if [ $counter -eq $timeout ]; then
        echo "❌ Ollama服務啟動超時"
        echo "⚠️  將在沒有AI服務的情況下啟動應用"
        break
    fi
    echo "⏳ 等待Ollama服務... ($counter/$timeout)"
    sleep 2
    counter=$((counter + 2))
done

if curl -s http://ollama:11434/api/tags &> /dev/null; then
    echo "✅ Ollama服務已就緒"
    
    # 下載模型（如果不存在）
    echo "📥 檢查並下載AI模型..."
    curl -X POST http://ollama:11434/api/pull -d '{"name": "llama3:8b"}' || echo "⚠️  模型下載失敗，將使用現有模型"
else
    echo "⚠️  Ollama服務不可用，將在有限功能模式下運行"
fi

# 啟動後端服務（背景運行）
echo "🚀 啟動後端服務..."
python main.py &
BACKEND_PID=$!

# 等待後端服務啟動
echo "⏳ 等待後端服務啟動..."
timeout=30
counter=0
while ! curl -s http://localhost:5001/health &> /dev/null; do
    if [ $counter -eq $timeout ]; then
        echo "❌ 後端服務啟動超時"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    echo "⏳ 等待後端服務... ($counter/$timeout)"
    sleep 1
    counter=$((counter + 1))
done

echo "✅ 後端服務已就緒"

# 啟動前端服務
echo "🚀 啟動前端服務..."
echo "📍 應用將在以下地址可用:"
echo "   - 前端界面: http://localhost:8501"
echo "   - 後端API: http://localhost:5001"
echo "🛑 按 Ctrl+C 停止服務"
echo ""

# 設置信號處理
cleanup() {
    echo ""
    echo "🛑 正在停止服務..."
    kill $BACKEND_PID 2>/dev/null
    echo "✅ 服務已停止"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 啟動Streamlit
streamlit run app.py --server.port=8501 --server.address=0.0.0.0