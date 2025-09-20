# 🔧 故障排除

> **常見問題解決方案** | 快速診斷和修復 ClinicSim-AI 問題

## 🚨 緊急問題

### 系統無法啟動

#### 問題：Python 版本不符
```bash
# 錯誤訊息
Python 3.7.0 is not supported. Please use Python 3.8 or higher.

# 解決方案
# 檢查 Python 版本
python --version

# 升級 Python（使用 pyenv）
pyenv install 3.11.0
pyenv global 3.11.0
```

#### 問題：依賴安裝失敗
```bash
# 錯誤訊息
ERROR: Could not find a version that satisfies the requirement

# 解決方案
# 更新 pip
python -m pip install --upgrade pip

# 清理快取
pip cache purge

# 重新安裝
pip install -r requirements-dev.txt --force-reinstall
```

#### 問題：端口被佔用
```bash
# 錯誤訊息
Address already in use: Port 5001 is in use

# 解決方案
# 查找佔用端口的程序
lsof -i:5001  # macOS/Linux
netstat -ano | findstr :5001  # Windows

# 終止程序
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# 或修改端口
# 編輯 .env 檔案
PORT=5002
```

## 🤖 AI 服務問題

### Ollama 連接問題

#### 問題：Ollama 服務未啟動
```bash
# 錯誤訊息
Connection refused: Ollama service not running

# 解決方案
# 啟動 Ollama
ollama serve

# 檢查狀態
ollama list

# 下載模型
ollama pull llama3:8b
```

#### 問題：模型載入失敗
```bash
# 錯誤訊息
Model 'llama3:8b' not found

# 解決方案
# 查看可用模型
ollama list

# 下載模型
ollama pull llama3:8b

# 或使用其他模型
ollama pull llama3:7b
```

#### 問題：AI 回應很慢
```bash
# 可能原因和解決方案

# 1. 模型太大
ollama pull llama3:7b  # 使用較小的模型

# 2. 硬體不足
# 檢查記憶體使用
free -h  # Linux
vm_stat  # macOS

# 3. 網路問題
# 檢查網路連線
ping google.com
```

### Lemonade AI 問題

#### 問題：Lemonade 環境未檢測到
```bash
# 錯誤訊息
Lemonade environment not detected

# 解決方案
# 檢查環境變數
echo $LEMONADE_HOST
echo $LEMONADE_MODEL

# 設置環境變數
export LEMONADE_HOST="http://lemonade-server:8080"
export LEMONADE_MODEL="qwen3-1.7b"
```

## 📚 RAG 系統問題

### 索引問題

#### 問題：RAG 索引載入失敗
```bash
# 錯誤訊息
RAG index loading failed: File not found

# 解決方案
# 檢查索引檔案
ls -la faiss_index/

# 重新建立索引
rm -rf faiss_index/
python build_index.py
```

#### 問題：索引建立失敗
```bash
# 錯誤訊息
Failed to build RAG index: Memory error

# 解決方案
# 1. 減少文件大小
# 編輯 build_index.py
chunk_size = 500  # 預設 1000

# 2. 分批處理
# 將大文件分割成小文件

# 3. 增加記憶體
# 關閉其他應用程式
```

#### 問題：搜尋結果為空
```bash
# 錯誤訊息
No relevant documents found

# 解決方案
# 1. 檢查索引狀態
curl http://localhost:5001/rag/status

# 2. 重新建立索引
python build_index.py

# 3. 調整搜尋參數
# 編輯 rag_handler.py
k = 5  # 增加搜尋結果數量
```

### 文檔處理問題

#### 問題：PDF 讀取失敗
```bash
# 錯誤訊息
Failed to read PDF file

# 解決方案
# 1. 安裝依賴
pip install pymupdf

# 2. 檢查檔案格式
file document.pdf

# 3. 轉換為文字格式
# 使用其他工具轉換 PDF 為 TXT
```

## 🌐 網路和連接問題

### 前端連接問題

#### 問題：前端無法連接後端
```bash
# 錯誤訊息
Failed to connect to backend API

# 解決方案
# 1. 檢查後端是否運行
curl http://localhost:5001/health

# 2. 檢查防火牆設置
# 允許端口 5001

# 3. 檢查 CORS 設置
# 編輯 server.py
CORS(app, origins=["http://localhost:8501"])
```

#### 問題：API 請求超時
```bash
# 錯誤訊息
Request timeout after 30 seconds

# 解決方案
# 1. 增加超時時間
# 編輯前端代碼
timeout = 60

# 2. 檢查後端性能
# 查看後端日誌
python main.py --log-level debug

# 3. 優化 AI 模型
# 使用較小的模型
```

### 瀏覽器問題

#### 問題：界面顯示異常
```bash
# 可能原因和解決方案

# 1. 瀏覽器快取
# 清除瀏覽器快取
# Ctrl+Shift+Delete (Windows/Linux)
# Cmd+Shift+Delete (macOS)

# 2. JavaScript 錯誤
# 開啟開發者工具 (F12)
# 查看 Console 錯誤

# 3. Streamlit 版本問題
pip install --upgrade streamlit
```

## 💾 數據和存儲問題

### 案例數據問題

#### 問題：案例載入失敗
```bash
# 錯誤訊息
Case 'case_chest_pain_acs_01' not found

# 解決方案
# 1. 檢查案例檔案
ls -la cases/

# 2. 驗證 JSON 格式
python -m json.tool cases/case_chest_pain_acs_01.json

# 3. 檢查檔案權限
chmod 644 cases/*.json
```

#### 問題：對話記錄丟失
```bash
# 可能原因和解決方案

# 1. 會話超時
# 增加會話時間
# 編輯 Streamlit 配置

# 2. 瀏覽器關閉
# 實現自動保存功能

# 3. 服務器重啟
# 實現持久化存儲
```

### 配置問題

#### 問題：環境變數未載入
```bash
# 錯誤訊息
Environment variable not found

# 解決方案
# 1. 檢查 .env 檔案
cat .env

# 2. 檢查檔案位置
# .env 應該在專案根目錄

# 3. 檢查檔案格式
# 確保沒有空格和引號問題
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3:8b
```

## 🔍 診斷工具

### 系統檢查腳本

```python
# check_system.py
import sys
import importlib
import requests

def check_python_version():
    """檢查 Python 版本"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print("✅ Python 版本符合要求")
        return True
    else:
        print(f"❌ Python 版本不符: {version.major}.{version.minor}")
        return False

def check_dependencies():
    """檢查依賴套件"""
    required_packages = [
        'flask', 'streamlit', 'langchain', 
        'faiss', 'ollama', 'pydantic'
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} 已安裝")
        except ImportError:
            print(f"❌ {package} 未安裝")
            missing.append(package)
    
    return len(missing) == 0

def check_services():
    """檢查服務狀態"""
    services = [
        ("後端 API", "http://localhost:5001/health"),
        ("前端界面", "http://localhost:8501")
    ]
    
    for name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} 正常運行")
            else:
                print(f"⚠️ {name} 狀態異常: {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"❌ {name} 無法連接")

def main():
    """主檢查函數"""
    print("🔍 ClinicSim-AI 系統檢查")
    print("=" * 40)
    
    checks = [
        check_python_version(),
        check_dependencies(),
    ]
    
    check_services()
    
    if all(checks):
        print("\n🎉 系統檢查通過！")
    else:
        print("\n⚠️ 發現問題，請查看上述錯誤訊息")

if __name__ == "__main__":
    main()
```

### 日誌分析

#### 查看錯誤日誌
```bash
# 後端日誌
python main.py --log-level debug 2>&1 | tee backend.log

# 前端日誌
streamlit run app_new.py --logger.level debug 2>&1 | tee frontend.log

# 分析日誌
grep "ERROR" backend.log
grep "WARNING" backend.log
```

#### 性能監控
```bash
# 監控資源使用
top -p $(pgrep -f "python main.py")

# 監控網路連接
netstat -an | grep :5001

# 監控磁碟使用
df -h
du -sh faiss_index/
```

## 🆘 獲取幫助

### 自助診斷

1. **運行系統檢查**
   ```bash
   python check_system.py
   ```

2. **查看日誌**
   ```bash
   tail -f backend.log
   ```

3. **測試 API**
   ```bash
   curl http://localhost:5001/health
   ```

### 收集診斷資訊

當回報問題時，請提供：

1. **系統資訊**
   ```bash
   python --version
   pip list | grep -E "(flask|streamlit|langchain)"
   ```

2. **錯誤日誌**
   ```bash
   # 複製完整的錯誤訊息
   ```

3. **環境配置**
   ```bash
   cat .env  # 移除敏感資訊
   ```

4. **重現步驟**
   - 詳細描述問題重現步驟
   - 預期行為 vs 實際行為

### 聯絡方式

- 📧 **技術支援**: support@clinicsim-ai.com
- 💬 **討論區**: [GitHub Discussions](https://github.com/your-username/ClinicSim-AI/discussions)
- 🐛 **問題回報**: [GitHub Issues](https://github.com/your-username/ClinicSim-AI/issues)

### 社群支援

- 🌟 **GitHub Star**: 給我們一個 Star
- 👀 **Watch 專案**: 關注最新更新
- 🍴 **Fork 專案**: 貢獻您的改進

---

**希望這個故障排除指南能幫助您解決問題！** 🎉

如果問題仍未解決，請查看 [API 文檔](api-documentation.md) 或 [開發者指南](developer-guide.md)。
