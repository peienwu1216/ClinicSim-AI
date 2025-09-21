# 🚀 AMD Ryzen AI NPU 設定指南

本指南說明如何在 ClinicSim-AI 中啟用 AMD Ryzen AI NPU 加速，使用 Lemonade OGA 框架。

## 📋 前置需求

### 硬體需求
- **AMD Ryzen AI 300 系列處理器** (如 Ryzen AI 9 HX 370, Ryzen AI 9 365)
- **Windows 11 22H2 或更新版本**
- **至少 16GB RAM** (推薦 32GB)

### 軟體需求
- **Python 3.8+**
- **Lemonade SDK** 或 **Lemonade Server**
- **AMD 驅動程式** (最新版本)

## 🔧 安裝步驟

### 1. 安裝 Lemonade SDK

```bash
# 安裝 Lemonade SDK (包含 OGA 支援)
pip install lemonade-sdk

# 或安裝完整版本
pip install "lemonade-sdk[dev,oga-cpu]"
```

### 2. 安裝專案依賴

```bash
# 安裝專案依賴
pip install -r requirements.txt
pip install -r requirements-lemonade.txt
```

## ⚙️ 配置設定

### 環境變數設定

創建 `.env` 檔案或設定環境變數：

```env
# AI 提供者設定
AI_PROVIDER=lemonade

# Lemonade 模型設定
LEMONADE_MODEL_CHECKPOINT=amd/Qwen2.5-7B-Instruct-awq-uint4-asym-g128-lmhead-g32-fp16-onnx-hybrid
LEMONADE_RECIPE=oga-hybrid

# Server 模式設定 (可選)
LEMONADE_BASE_URL=http://localhost:8000/api/v1
LEMONADE_API_KEY=lemonade
```

### 配置說明

#### 模型檢查點 (LEMONADE_MODEL_CHECKPOINT)
選擇支援 AMD NPU 的模型檢查點：

**推薦模型：**
- `amd/Qwen2.5-7B-Instruct-awq-uint4-asym-g128-lmhead-g32-fp16-onnx-hybrid` (7B, Hybrid)
- `amd/Llama-3.2-1B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid` (1B, Hybrid)
- `amd/Phi-3.5-mini-instruct-awq-g128-int4-asym-fp16-onnx-hybrid` (Mini, Hybrid)

**重要：** 必須選擇標記為 `onnx-hybrid` 或 `onnx-ryzen-strix` 的檢查點。

#### 設備選擇 (LEMONADE_RECIPE)
控制模型在哪些設備上執行：

- **`oga-npu`**: 純 NPU 執行 (最快，但需要 NPU 支援)
- **`oga-hybrid`**: 混合執行 (NPU + CPU，推薦)
- **`oga-cpu`**: CPU 執行 (最慢，但最穩定)
- **`hf-cpu`**: HuggingFace CPU 執行 (備用)

#### Server 模式 (可選)
如果使用 Lemonade Server 而非直接 SDK：

```env
LEMONADE_BASE_URL=http://localhost:8000/api/v1
LEMONADE_API_KEY=lemonade
```

## 🧪 測試配置

### 運行煙霧測試

```bash
# 運行完整的 NPU 測試
python -m tools.npu_smoke_test

# 或直接運行
python tools/npu_smoke_test.py
```

### 測試內容

測試腳本會檢查：
1. **設備信息檢測** - 確認 NPU 是否可用
2. **模型載入** - 測試模型載入時間
3. **推理測試** - 測試生成速度和品質
4. **服務可用性** - 確認 AI 服務正常運作

### 預期輸出

```
🚀 Lemonade OGA NPU 煙霧測試
============================================================
設定摘要:
  AI Provider: lemonade
  模型檢查點: amd/Qwen2.5-7B-Instruct-awq-uint4-asym-g128-lmhead-g32-fp16-onnx-hybrid
  Recipe: oga-hybrid
  Server 模式: 否

🔍 設備信息檢測
============================================================
設備信息: {'npu': True, 'cpu': True, 'gpu': False}
NPU 可用: 是

🧪 SDK 模式測試
============================================================
載入時間: 12.34 秒
推理時間: 2.56 秒
回應: Recipes control device selection by specifying which backend...

📊 測試總結
============================================================
  設備信息檢測: ✅ 通過
  SDK 模式測試: ✅ 通過
  AI 服務測試: ✅ 通過

總計: 3/3 測試通過
🎉 所有測試通過！NPU 配置正確。
```

## 🚀 啟動應用程式

### 方法 1: 使用啟動腳本

```bash
# 啟動 NPU 加速版本
python start_npu.py
```

### 方法 2: 手動啟動

```bash
# 後端服務
python main.py

# 前端界面 (新終端)
streamlit run app.py
```

## 🔍 故障排除

### 常見問題

#### 1. NPU 未檢測到
**症狀：** 測試顯示 "NPU 可用: 否"

**解決方案：**
- 確認使用 Ryzen AI 300 系列處理器
- 更新 AMD 驅動程式到最新版本
- 切換到 `LEMONADE_RECIPE=oga-hybrid` 或 `oga-cpu`

#### 2. 模型載入失敗
**症狀：** "無法載入 Lemonade 模型"

**解決方案：**
- 確認網路連接 (需要下載模型)
- 檢查模型檢查點名稱是否正確
- 嘗試不同的 recipe (`hf-cpu` 作為備用)

#### 3. 推理速度慢
**症狀：** 推理時間超過 10 秒

**解決方案：**
- 確認使用 `oga-hybrid` 或 `oga-npu` recipe
- 檢查 NPU 是否被其他程序佔用
- 嘗試較小的模型 (1B 而非 7B)

#### 4. Server 模式連接失敗
**症狀：** "無法連接到 Lemonade Server"

**解決方案：**
- 確認 Lemonade Server 正在運行
- 檢查 `LEMONADE_BASE_URL` 是否正確
- 確認 Server 已載入對應的模型

### 調試模式

啟用詳細日誌：

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### 性能監控

使用 Windows 工作管理員監控：
- **NPU 使用率** - 應在推理時顯示活動
- **CPU 使用率** - 應相對較低
- **記憶體使用** - 模型載入後應穩定

## 📊 性能基準

### 預期性能 (Qwen-2.5-7B-Instruct-Hybrid)

| Recipe | 載入時間 | 推理時間 (50 tokens) | 記憶體使用 |
|--------|----------|---------------------|------------|
| oga-npu | 8-15 秒 | 1-3 秒 | 4-6 GB |
| oga-hybrid | 10-20 秒 | 2-4 秒 | 4-6 GB |
| oga-cpu | 15-30 秒 | 5-10 秒 | 4-6 GB |
| hf-cpu | 20-40 秒 | 10-20 秒 | 6-8 GB |

### 優化建議

1. **首次使用** - 使用 `oga-hybrid` 確保穩定性
2. **生產環境** - 使用 `oga-npu` 獲得最佳性能
3. **調試模式** - 使用 `hf-cpu` 避免硬體問題

## 🔄 切換設備

### 動態切換

修改環境變數後重啟應用程式：

```bash
# 切換到純 NPU
export LEMONADE_RECIPE=oga-npu

# 切換到混合模式
export LEMONADE_RECIPE=oga-hybrid

# 切換到 CPU (備用)
export LEMONADE_RECIPE=oga-cpu
```

### 模型切換

```bash
# 切換到較小模型
export LEMONADE_MODEL_CHECKPOINT=amd/Llama-3.2-1B-Instruct-awq-g128-int4-asym-fp16-onnx-hybrid

# 切換到較大模型
export LEMONADE_MODEL_CHECKPOINT=amd/Qwen2.5-7B-Instruct-awq-uint4-asym-g128-lmhead-g32-fp16-onnx-hybrid
```

## 📚 進階配置

### 自定義模型檢查點

支援任何符合 OGA 格式的模型：

```env
LEMONADE_MODEL_CHECKPOINT=your-custom/model-checkpoint
LEMONADE_RECIPE=oga-hybrid
```

### 多模型支援

可以配置多個模型並動態切換：

```python
# 在代碼中動態切換
settings.lemonade_model_checkpoint = "new-model-checkpoint"
ai_service = AIServiceFactory.create_from_config(settings)
```

## 🆘 獲取幫助

如果遇到問題：

1. **檢查日誌** - 查看詳細錯誤信息
2. **運行測試** - 使用 `python -m tools.npu_smoke_test`
3. **檢查硬體** - 確認 NPU 支援
4. **更新驅動** - 安裝最新 AMD 驅動程式
5. **切換模式** - 嘗試不同的 recipe 設定

## 📝 更新日誌

- **v2.0.0** - 統一 Lemonade 配置，支援 recipe 系統
- **v1.0.0** - 初始 NPU 支援

---

**注意：** 本指南基於 AMD Ryzen AI 300 系列處理器和 Windows 11 環境。其他硬體配置可能需要調整。
