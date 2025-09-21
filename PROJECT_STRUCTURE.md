# 📁 ClinicSim-AI 項目結構說明

## 🎯 目錄整理概述

按照標準業界實踐，我們重新組織了項目目錄結構，使其更加清晰、易於維護和擴展。

## 📋 標準目錄結構

```
ClinicSim-AI/
├── 📁 src/                          # 主要源代碼
│   ├── 📁 api/                      # API 相關代碼
│   ├── 📁 config/                   # 配置相關代碼
│   ├── 📁 exceptions/               # 異常處理
│   ├── 📁 frontend/                 # 前端代碼
│   ├── 📁 models/                   # 數據模型
│   ├── 📁 services/                 # 業務邏輯服務
│   └── 📁 utils/                    # 工具函數
├── 📁 assets/                       # 靜態資源
│   ├── 📁 images/                   # 圖片資源
│   │   ├── ECG-image.jpg           # 心電圖圖片
│   │   └── CXR-image.jpeg          # 胸部X光圖片
│   └── 📁 docs/                     # 項目文檔
│       ├── COVERAGE_UPDATE_FIX.md   # 覆蓋率修復文檔
│       ├── IMAGE_DISPLAY_UPDATE.md  # 圖片顯示更新文檔
│       └── ...                      # 其他項目文檔
├── 📁 config/                       # 配置文件
│   ├── requirements.txt             # 主要依賴
│   ├── requirements-dev.txt         # 開發依賴
│   ├── requirements-production.txt  # 生產環境依賴
│   └── scoring_sys.json            # 評分系統配置
├── 📁 scripts/                      # 腳本文件
│   ├── start_npu.py                # NPU 啟動腳本
│   ├── build_index.py              # 索引構建腳本
│   ├── test_*.py                   # 測試腳本
│   └── ...                         # 其他腳本
├── 📁 tests/                        # 測試文件（待擴展）
├── 📁 cases/                        # 病例數據
├── 📁 docs/                         # 官方文檔
├── 📁 documents/                    # 醫學文檔
├── 📁 static/                       # 靜態文件
├── 📁 faiss_index/                  # 向量索引
├── 📁 report_history/               # 報告歷史
├── 📁 tools/                        # 工具
├── 📁 examples/                     # 示例代碼
├── 📁 backups/                      # 備份文件
├── 📄 README.md                     # 項目說明
├── 📄 main.py                       # 主程序入口
└── 📄 app.py                        # Streamlit 應用入口
```

## 🔧 目錄功能說明

### 📁 src/ - 主要源代碼
- **api/**: REST API 路由和依賴注入
- **config/**: 配置管理、NPU 優化設置
- **exceptions/**: 自定義異常類
- **frontend/**: Streamlit 前端應用和組件
- **models/**: 數據模型定義
- **services/**: 業務邏輯服務（AI、RAG、評分等）
- **utils/**: 通用工具函數

### 📁 assets/ - 靜態資源
- **images/**: 應用使用的圖片資源
  - `ECG-image.jpg`: 心電圖示例圖片
  - `CXR-image.jpeg`: 胸部X光示例圖片
- **docs/**: 項目相關文檔和更新記錄

### 📁 config/ - 配置文件
- **requirements*.txt**: 不同環境的依賴配置
- **scoring_sys.json**: OSCE 評分系統配置

### 📁 scripts/ - 腳本文件
- **start_npu.py**: NPU 服務啟動腳本
- **build_index.py**: FAISS 向量索引構建
- **test_*.py**: 各種測試腳本
- **其他腳本**: 安裝、生成、改進等腳本

### 📁 其他重要目錄
- **cases/**: 醫學病例 JSON 文件
- **docs/**: 官方技術文檔
- **documents/**: 醫學參考文檔
- **static/**: Web 靜態資源
- **faiss_index/**: RAG 向量搜索索引
- **report_history/**: 生成的報告歷史
- **tools/**: 開發工具
- **examples/**: 使用示例

## 🚀 使用指南

### 啟動應用
```bash
# 啟動 Streamlit 前端
python -m streamlit run src/frontend/app.py --server.port 8501

# 啟動 NPU 服務（如果需要）
python scripts/start_npu.py
```

### 配置文件
- **依賴安裝**: 查看 `config/requirements.txt`
- **評分系統**: 修改 `config/scoring_sys.json`
- **NPU 設置**: 查看 `src/config/npu_optimization.py`

### 開發指南
- **添加新組件**: 在 `src/frontend/components/` 中創建
- **添加新服務**: 在 `src/services/` 中創建
- **添加新模型**: 在 `src/models/` 中創建
- **添加新測試**: 在 `tests/` 中創建（待擴展）

## 📝 路徑引用更新

### 圖片路徑
```python
# 新的圖片路徑查找邏輯
assets_path = Path(__file__).parent.parent.parent.parent / "assets" / "images" / image_filename
```

### 配置文件路徑
```python
# 評分系統配置路徑
rubric_path = Path(self.settings.project_root) / "config" / "scoring_sys.json"
```

### 向下兼容
- 圖片路徑查找會依次檢查：
  1. `assets/images/` (新位置)
  2. 根目錄 (向下兼容)
  3. `static/samples/` (備用位置)

## 🎯 整理效果

### 整理前
- ❌ 根目錄混亂，文件散落
- ❌ 文檔分散，難以查找
- ❌ 配置文件位置不明確
- ❌ 腳本文件雜亂無章

### 整理後
- ✅ **清晰的目錄結構** - 按功能分類組織
- ✅ **標準化的資源管理** - assets 目錄統一管理
- ✅ **配置集中管理** - config 目錄統一配置
- ✅ **腳本統一管理** - scripts 目錄統一腳本
- ✅ **文檔分類整理** - docs 和 assets/docs 分類管理
- ✅ **向下兼容** - 保持原有功能不受影響

## 🔄 遷移記錄

### 文件移動記錄
1. **圖片文件**:
   - `ECG-image.jpg` → `assets/images/ECG-image.jpg`
   - `CXR-image.jpeg` → `assets/images/CXR-image.jpeg`

2. **配置文件**:
   - `scoring_sys.json` → `config/scoring_sys.json`
   - `requirements*.txt` → `config/`

3. **腳本文件**:
   - `start_*.py`, `test_*.py`, `build_index.py` 等 → `scripts/`

4. **文檔文件**:
   - 各種 `*_FIX.md`, `*_UPDATE.md` 等 → `assets/docs/`

### 代碼更新記錄
1. **圖片路徑查找邏輯** - 更新為優先檢查 `assets/images/`
2. **配置文件路徑** - 更新為 `config/scoring_sys.json`
3. **向下兼容性** - 保持對舊路徑的支持

## 📚 最佳實踐

### 文件命名
- 使用小寫字母和連字符
- 避免空格和特殊字符
- 保持一致的命名規範

### 目錄結構
- 按功能分類，而非文件類型
- 保持層級不超過 3-4 層
- 使用有意義的目錄名稱

### 資源管理
- 靜態資源統一放在 `assets/`
- 配置文件統一放在 `config/`
- 腳本文件統一放在 `scripts/`

## 🎉 總結

通過這次目錄整理，我們實現了：

✅ **標準化的項目結構** - 符合業界最佳實踐
✅ **清晰的資源管理** - 靜態資源和配置文件統一管理
✅ **易於維護和擴展** - 結構清晰，便於團隊協作
✅ **向下兼容** - 不影響現有功能
✅ **文檔完整** - 提供詳細的結構說明和使用指南

現在的項目結構更加專業、清晰，便於維護和團隊協作！
