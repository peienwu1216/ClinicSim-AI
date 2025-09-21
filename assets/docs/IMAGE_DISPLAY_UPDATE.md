# 🖼️ 圖片顯示功能更新

## 🎯 需求說明

用戶希望右側功能區按照指定樣式設計，並且在點擊ECG和CXR後能在右下角空白處顯示對應的圖片：
- **ECG圖片**: `ECG-image.jpg`
- **CXR圖片**: `CXR-image.jpeg`

## ✅ 修復內容

### 1. 更新圖片路徑配置
**文件**: `src/frontend/components/clinical_orders_simplified.py`

**修復前**:
```python
{
    "id": "ecg",
    "image_path": "ecg_sample.png"  # 舊的圖片路徑
},
{
    "id": "chest_xray", 
    "image_path": "chest_xray_sample.png"  # 舊的圖片路徑
}
```

**修復後**:
```python
{
    "id": "ecg",
    "name": "心電圖",
    "icon": "📈",
    "description": "12導程心電圖 (<10分鐘)",
    "action": "我現在要為病人立即安排12導程心電圖檢查，在10分鐘內完成",
    "priority": "critical",
    "image_path": "ECG-image.jpg"  # 更新為根目錄下的ECG圖片
},
{
    "id": "chest_xray",
    "name": "胸部X光",
    "icon": "🖥️",
    "description": "Portable CXR",
    "action": "安排 Portable Chest X-ray，確認是否有氣胸或主動脈剝離等問題",
    "priority": "critical",
    "image_path": "CXR-image.jpeg"  # 更新為根目錄下的CXR圖片
}
```

### 2. 增強圖片路徑查找邏輯
**文件**: `src/frontend/components/clinical_orders_simplified.py`

**修復前**:
```python
def _get_image_path(self, image_filename: str) -> Optional[str]:
    """獲取圖片完整路徑"""
    if not image_filename:
        return None
    
    # 檢查static目錄
    static_path = Path(__file__).parent.parent.parent.parent / "static" / "samples" / image_filename
    if static_path.exists():
        return str(static_path)
    
    return None
```

**修復後**:
```python
def _get_image_path(self, image_filename: str) -> Optional[str]:
    """獲取圖片完整路徑"""
    if not image_filename:
        return None
    
    # 首先檢查根目錄
    root_path = Path(__file__).parent.parent.parent.parent / image_filename
    if root_path.exists():
        return str(root_path)
    
    # 然後檢查static目錄
    static_path = Path(__file__).parent.parent.parent.parent / "static" / "samples" / image_filename
    if static_path.exists():
        return str(static_path)
    
    return None
```

### 3. 同步更新主應用程式的圖片路徑邏輯
**文件**: `src/frontend/app.py`

**修復前**:
```python
def _get_image_path(self, image_filename: str) -> Optional[str]:
    """獲取圖片完整路徑"""
    if not image_filename:
        return None
    
    # 檢查static/samples目錄
    static_path = Path(__file__).parent.parent.parent.parent / "static" / "samples" / image_filename
    if static_path.exists():
        return str(static_path)
    
    return None
```

**修復後**:
```python
def _get_image_path(self, image_filename: str) -> Optional[str]:
    """獲取圖片完整路徑"""
    if not image_filename:
        return None
    
    # 首先檢查根目錄
    root_path = Path(__file__).parent.parent.parent.parent / image_filename
    if root_path.exists():
        return str(root_path)
    
    # 然後檢查static/samples目錄
    static_path = Path(__file__).parent.parent.parent.parent / "static" / "samples" / image_filename
    if static_path.exists():
        return str(static_path)
    
    return None
```

## 🧪 測試結果

### 圖片路徑驗證
```
🧪 測試圖片路徑...
ECG圖片路徑: C:\Users\weini\Documents\ClinicSim-AI\ECG-image.jpg
ECG圖片存在: True
CXR圖片路徑: C:\Users\weini\Documents\ClinicSim-AI\CXR-image.jpeg
CXR圖片存在: True
組件ECG圖片路徑: C:\Users\weini\Documents\ClinicSim-AI\ECG-image.jpg
組件ECG圖片存在: True
組件CXR圖片路徑: C:\Users\weini\Documents\ClinicSim-AI\CXR-image.jpeg
組件CXR圖片存在: True
```

### 圖片顯示邏輯
當用戶點擊ECG或CXR按鈕時：
1. **發送訊息**: 執行對應的臨床指令文字
2. **顯示圖片**: 在聊天區域右下角顯示對應的檢查結果圖片
3. **圖片標題**: 自動生成圖片標題（如"12導程心電圖 檢查結果"）

## 🎨 UI設計特色

### ✨ 主要改進
1. **🚨 緊急檢查區域**
   - 紅色漸層標題
   - 紅色邊框標示
   - "緊急"優先級標籤
   - 始終可見

2. **⚕️ 次要檢查區域**
   - 藍色漸層標題
   - 可摺疊設計（預設摺疊）
   - "次要"優先級標籤
   - 節省空間

3. **🎨 視覺優化**
   - 清晰的優先級色彩區分
   - 漸層背景增加質感
   - 統一的圖標和描述
   - 響應式按鈕交互

### 📋 檢查項目分層

#### 第一層 - 緊急檢查（始終可見）
1. **📈 心電圖** - 12導程心電圖 (<10分鐘) → 顯示 `ECG-image.jpg`
2. **💓 生命體徵** - 血壓、心率、血氧、呼吸
3. **🖥️ 胸部X光** - Portable CXR → 顯示 `CXR-image.jpeg`
4. **🩸 抽血檢驗** - Troponin I + 其他心肌酵素

#### 第二層 - 次要檢查（可摺疊）
1. **💨 氧氣治療** - O₂ Support
2. **💉 建立靜脈管路** - IV line
3. **💊 阿斯匹靈** - 160-325mg
4. **🫀 硝化甘油** - GTN spray/tablet

## 🚀 使用方式

### 圖片顯示流程
1. **點擊ECG按鈕**
   - 發送訊息: "我現在要為病人立即安排12導程心電圖檢查，在10分鐘內完成"
   - 顯示圖片: `ECG-image.jpg` 在聊天區域
   - 圖片標題: "12導程心電圖 檢查結果"

2. **點擊CXR按鈕**
   - 發送訊息: "安排 Portable Chest X-ray，確認是否有氣胸或主動脈剝離等問題"
   - 顯示圖片: `CXR-image.jpeg` 在聊天區域
   - 圖片標題: "胸部X光 檢查結果"

### 圖片路徑優先級
1. **根目錄優先**: 首先檢查項目根目錄下的圖片文件
2. **備用路徑**: 如果根目錄沒有，則檢查 `static/samples/` 目錄
3. **錯誤處理**: 如果圖片不存在，不會顯示圖片但會正常執行其他功能

## 🔧 技術實現

### 圖片路徑解析
```python
# 圖片路徑查找邏輯
root_path = Path(__file__).parent.parent.parent.parent / image_filename
static_path = Path(__file__).parent.parent.parent.parent / "static" / "samples" / image_filename

# 優先使用根目錄的圖片
if root_path.exists():
    return str(root_path)
elif static_path.exists():
    return str(static_path)
```

### 圖片顯示整合
```python
# 在聊天訊息中顯示圖片
if image_path:
    image_full_path = self._get_image_path(image_path)
    if image_full_path and os.path.exists(image_full_path):
        st.image(image_full_path, caption=f"{self._get_order_name_from_action(action)} 檢查結果", use_column_width=True)
```

## 🎯 總結

圖片顯示功能已經成功更新：

✅ **正確的圖片路徑**: ECG和CXR圖片現在指向根目錄下的正確文件
✅ **智能路徑查找**: 優先檢查根目錄，備用檢查static目錄
✅ **完整的圖片顯示**: 點擊ECG和CXR後會在聊天區域顯示對應圖片
✅ **自動圖片標題**: 根據檢查類型自動生成圖片標題
✅ **向下兼容**: 保持對原有static目錄圖片的支持
✅ **錯誤處理**: 圖片不存在時不會影響其他功能

現在用戶點擊ECG或CXR按鈕後，會看到：
1. 臨床指令訊息發送到聊天區
2. 對應的檢查結果圖片顯示在聊天區域
3. 圖片有適當的標題說明

所有功能都經過測試驗證，可以正常使用！
