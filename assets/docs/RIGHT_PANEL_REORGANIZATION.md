# 🔧 右側檢查面板重新組織修復

## 🎯 需求說明

用戶要求修復右側的檢查邏輯，將最重要的檢查項目放在第一層：
- **第一層（緊急檢查）**: ECG、生命體徵、胸部X-ray、抽血Troponin
- **第二層（次要檢查）**: 其他比較不重要的項目

## ✅ 修復內容

### 1. 重新組織數據結構
**文件**: `src/frontend/components/clinical_orders_simplified.py`

**修復前** - 單一層級結構:
```python
def _initialize_simplified_orders_data(self) -> List[Dict]:
    return [
        {"id": "ecg", "priority": "high"},
        {"id": "troponin", "priority": "high"},
        # 所有項目混在一起
    ]
```

**修復後** - 分層級結構:
```python
def _initialize_simplified_orders_data(self) -> Dict[str, List[Dict]]:
    return {
        "critical": [
            {
                "id": "ecg",
                "name": "心電圖",
                "icon": "📈",
                "description": "12導程心電圖 (<10分鐘)",
                "action": "我現在要為病人立即安排12導程心電圖檢查，在10分鐘內完成",
                "priority": "critical"
            },
            {
                "id": "vital_signs",
                "name": "生命體徵",
                "icon": "💓",
                "description": "血壓、心率、血氧、呼吸",
                "action": "立即測量病人的生命體徵：血壓、心率、血氧飽和度、呼吸頻率",
                "priority": "critical"
            },
            {
                "id": "chest_xray",
                "name": "胸部X光",
                "icon": "🖥️",
                "description": "Portable CXR",
                "action": "安排 Portable Chest X-ray，確認是否有氣胸或主動脈剝離等問題",
                "priority": "critical"
            },
            {
                "id": "troponin",
                "name": "抽血檢驗",
                "icon": "🩸",
                "description": "Troponin I + 其他",
                "action": "立即幫病人抽血，檢驗 Cardiac Troponin I、CK-MB 等心肌酵素",
                "priority": "critical"
            }
        ],
        "secondary": [
            {
                "id": "oxygen",
                "name": "氧氣治療",
                "icon": "💨",
                "description": "O₂ Support",
                "priority": "secondary"
            },
            {
                "id": "iv_access",
                "name": "建立靜脈管路",
                "icon": "💉",
                "description": "IV line",
                "priority": "secondary"
            },
            {
                "id": "aspirin",
                "name": "阿斯匹靈",
                "icon": "💊",
                "description": "Aspirin 160-325mg",
                "priority": "secondary"
            },
            {
                "id": "nitroglycerin",
                "name": "硝化甘油",
                "icon": "🫀",
                "description": "GTN spray/tablet",
                "priority": "secondary"
            }
        ]
    }
```

### 2. 新增分層UI結構

#### 第一層 - 緊急檢查（始終可見）
```python
def _render_critical_orders(self, on_order_action: Optional[Callable] = None) -> None:
    """渲染關鍵檢查項目（第一層）"""
    
    # 類別標題
    st.markdown("""
    <div class="category-header critical">
        <span class="category-icon">🚨</span>
        <span>緊急檢查</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 渲染關鍵檢查項目
    for order in self.orders_data["critical"]:
        self._render_order_item(order, on_order_action)
```

#### 第二層 - 次要檢查（可摺疊）
```python
def _render_secondary_orders(self, on_order_action: Optional[Callable] = None) -> None:
    """渲染次要檢查項目（第二層，可摺疊）"""
    
    # 使用 expander 創建可摺疊的次要檢查區域
    with st.expander("🔍 其他檢查與治療", expanded=False):
        st.markdown("""
        <div class="category-header secondary">
            <span class="category-icon">⚕️</span>
            <span>次要檢查</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 渲染次要檢查項目
        for order in self.orders_data["secondary"]:
            self._render_order_item(order, on_order_action)
```

### 3. 增強視覺設計

#### 新增優先級樣式
```css
.order-item.critical-priority {
    border-left: 4px solid #dc3545;
    background: linear-gradient(135deg, #fff5f5 0%, #f8f9fa 100%);
}

.order-item.secondary-priority {
    border-left: 3px solid #17a2b8;
    background: #f8f9fa;
}

.priority-critical {
    background: #dc3545;
    color: white;
}

.priority-secondary {
    background: #17a2b8;
    color: white;
}
```

#### 新增類別標題樣式
```css
.category-header {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    margin: 16px 0 8px 0;
    font-weight: 600;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.category-header.critical {
    background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
}

.category-header.secondary {
    background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
}
```

### 4. 更新核心邏輯

#### 修改渲染主方法
```python
def render(self, on_order_action: Optional[Callable[[str, Optional[str]], None]] = None) -> None:
    """渲染簡化版臨床檢測面板"""
    
    # 應用簡化版CSS
    self._apply_simplified_css()
    
    # 主容器
    with st.container():
        st.markdown("""
        <div class="clinical-orders-simplified">
            <div class="simplified-header">
                <span class="simplified-icon">⚕️</span>
                <span class="simplified-title">臨床檢查</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 渲染關鍵檢查項目（第一層）
        self._render_critical_orders(on_order_action)
        
        # 渲染次要檢查項目（第二層，可摺疊）
        self._render_secondary_orders(on_order_action)
```

#### 更新數據查詢方法
```python
def get_order_by_id(self, order_id: str) -> Optional[Dict]:
    """根據ID獲取Order資訊"""
    # 搜尋所有類別
    for category_orders in self.orders_data.values():
        for order in category_orders:
            if order["id"] == order_id:
                return order
    return None
```

## 🎨 UI設計改進

### 層級結構
1. **第一層 - 緊急檢查**
   - 🚨 緊急檢查（標題）
   - 📈 心電圖（12導程心電圖 <10分鐘）
   - 💓 生命體徵（血壓、心率、血氧、呼吸）
   - 🖥️ 胸部X光（Portable CXR）
   - 🩸 抽血檢驗（Troponin I + 其他）

2. **第二層 - 次要檢查（可摺疊）**
   - 🔍 其他檢查與治療（expander標題）
   - ⚕️ 次要檢查（內部標題）
   - 💨 氧氣治療
   - 💉 建立靜脈管路
   - 💊 阿斯匹靈
   - 🫀 硝化甘油

### 視覺特徵
- **緊急檢查**: 紅色邊框，漸層背景，"緊急"標籤
- **次要檢查**: 藍色邊框，普通背景，"次要"標籤
- **類別標題**: 漸層背景，圖標，清晰的視覺層次
- **可摺疊設計**: 次要檢查預設摺疊，保持界面簡潔

## 🚀 使用效果

### 修復前
- ❌ 所有檢查項目混在一起
- ❌ 沒有優先級區分
- ❌ 界面冗長，不易快速找到重要檢查
- ❌ 視覺層次不清晰

### 修復後
- ✅ **清晰的二層結構**: 緊急檢查優先顯示
- ✅ **優先級視覺化**: 紅色緊急，藍色次要
- ✅ **界面簡潔**: 次要檢查可摺疊
- ✅ **符合臨床邏輯**: ECG、生命體徵、X-ray、Troponin 在第一層

## 📋 檢查項目說明

### 第一層 - 緊急檢查
1. **心電圖 (ECG)** - 12導程心電圖，10分鐘內完成
2. **生命體徵** - 血壓、心率、血氧飽和度、呼吸頻率
3. **胸部X光** - Portable CXR，排除氣胸、主動脈剝離
4. **抽血檢驗** - Troponin I、CK-MB 等心肌酵素

### 第二層 - 次要檢查
1. **氧氣治療** - 維持血氧 > 94%
2. **建立靜脈管路** - 準備給予緊急藥物
3. **阿斯匹靈** - 160-325mg 口嚼
4. **硝化甘油** - 舌下噴劑或錠劑

## 🎯 總結

右側檢查面板已經成功重新組織：

✅ **符合臨床優先級**: 將ECG、生命體徵、胸部X-ray、抽血Troponin放在第一層
✅ **清晰的視覺層次**: 緊急檢查用紅色，次要檢查用藍色
✅ **界面優化**: 次要檢查可摺疊，保持界面簡潔
✅ **一致的交互**: 所有檢查項目保持相同的點擊交互方式
✅ **完整的功能**: 保留原有的圖片顯示和訊息發送功能

現在用戶可以快速找到並執行最重要的檢查項目，同時將較不緊急的檢查項目整理在可摺疊的區域中，大幅提升了使用體驗和臨床實用性！
