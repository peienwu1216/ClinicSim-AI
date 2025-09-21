"""
簡化版臨床檢測組件 - 只保留最重要的檢查項目
"""

import streamlit as st
from typing import Dict, List, Optional, Callable
import os
from pathlib import Path

from .base import BaseComponent
from .custom_toggle import create_custom_expander


class ClinicalOrdersSimplifiedComponent(BaseComponent):
    """簡化版臨床檢測組件 - 精選最重要的檢查項目"""
    
    def __init__(self, key: str):
        super().__init__(key)
        self.orders_data = self._initialize_simplified_orders_data()
    
    def _initialize_simplified_orders_data(self) -> Dict[str, List[Dict]]:
        """初始化簡化版臨床檢測Orders數據 - 分層級組織"""
        return {
            "critical": [
                {
                    "id": "ecg",
                    "name": "心電圖",
                    "icon": "📈",
                    "description": "12導程心電圖 (<10分鐘)",
                    "action": "我現在要為病人立即安排12導程心電圖檢查，在10分鐘內完成",
                    "priority": "critical",
                    "image_path": "ECG-image.jpg"
                },
                {
                    "id": "vital_signs",
                    "name": "生命體徵",
                    "icon": "💓",
                    "description": "血壓、心率、血氧、呼吸",
                    "action": "立即測量病人的生命體徵：血壓、心率、血氧飽和度、呼吸頻率",
                    "priority": "critical",
                    "image_path": None
                },
                {
                    "id": "chest_xray",
                    "name": "胸部X光",
                    "icon": "🖥️",
                    "description": "Portable CXR",
                    "action": "安排 Portable Chest X-ray，確認是否有氣胸或主動脈剝離等問題",
                    "priority": "critical",
                    "image_path": "CXR-image.jpeg"
                },
                {
                    "id": "troponin",
                    "name": "抽血檢驗",
                    "icon": "🩸",
                    "description": "Troponin I + 其他",
                    "action": "立即幫病人抽血，檢驗 Cardiac Troponin I、CK-MB 等心肌酵素",
                    "priority": "critical",
                    "image_path": None
                }
            ],
            "secondary": [
                {
                    "id": "oxygen",
                    "name": "氧氣治療",
                    "icon": "💨",
                    "description": "O₂ Support",
                    "action": "給予病人氧氣，維持血氧濃度 > 94%",
                    "priority": "secondary",
                    "image_path": None
                },
                {
                    "id": "iv_access",
                    "name": "建立靜脈管路",
                    "icon": "💉",
                    "description": "IV line",
                    "action": "建立靜脈管路，準備給予緊急藥物",
                    "priority": "secondary",
                    "image_path": None
                },
                {
                    "id": "aspirin",
                    "name": "阿斯匹靈",
                    "icon": "💊",
                    "description": "Aspirin 160-325mg",
                    "action": "給予 Aspirin 160-325mg 口嚼，除非有禁忌症",
                    "priority": "secondary",
                    "image_path": None
                },
                {
                    "id": "nitroglycerin",
                    "name": "硝化甘油",
                    "icon": "🫀",
                    "description": "GTN spray/tablet",
                    "action": "給予硝化甘油舌下噴劑或錠劑，緩解胸痛",
                    "priority": "secondary",
                    "image_path": None
                }
            ]
        }
    
    def render(self, on_order_action: Optional[Callable[[str, Optional[str]], None]] = None) -> None:
        """渲染簡化版臨床檢測面板"""
        
        # 應用簡化版CSS
        self._apply_simplified_css()
        
        # 直接渲染檢查項目，不使用外框
        # 渲染關鍵檢查項目（第一層）
        self._render_critical_orders(on_order_action)
        
        # 渲染次要檢查項目（第二層，可摺疊）
        self._render_secondary_orders(on_order_action)
    
    def _apply_simplified_css(self):
        """應用簡化版CSS樣式"""
        st.markdown("""
        <style>
        /* 移除外框樣式，直接使用按鈕 */
        
        /* 按鈕樣式優化 - 緊湊布局 */
        .stButton > button {
            background: #f8f9fa !important;
            color: #2c3e50 !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
            margin-bottom: 6px !important;
            text-align: left !important;
            justify-content: flex-start !important;
        }
        
        .stButton > button:hover {
            background: #e9ecef !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* 緊急檢查按鈕樣式 */
        .stButton > button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #fff5f5 0%, #f8f9fa 100%) !important;
            border-left: 4px solid #dc3545 !important;
            color: #2c3e50 !important;
        }
        
        .stButton > button[data-testid="baseButton-primary"]:hover {
            background: linear-gradient(135deg, #ffe6e6 0%, #e9ecef 100%) !important;
        }
        
        /* 次要檢查按鈕樣式 */
        .stButton > button[data-testid="baseButton-secondary"] {
            background: #f8f9fa !important;
            border-left: 3px solid #17a2b8 !important;
            color: #2c3e50 !important;
        }
        
        .stButton > button[data-testid="baseButton-secondary"]:hover {
            background: #e9ecef !important;
        }
        
        /* 優先級標示 */
        .priority-badge {
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 500;
            margin-left: auto;
        }
        
        .priority-critical {
            background: #dc3545;
            color: white;
        }
        
        .priority-secondary {
            background: #17a2b8;
            color: white;
        }
        
        /* 類別標題樣式 - 緊湊版 */
        .category-header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 6px 10px;
            border-radius: 6px;
            margin: 4px 0 2px 0;
            font-weight: 600;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .category-header.critical {
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        }
        
        .category-header.secondary {
            background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
        }
        
        .category-icon {
            font-size: 1rem;
        }
        
        /* 隱藏 expander 的展開圖標文字 */
        [data-testid="stExpander"] .streamlit-expanderHeader p {
            display: none !important;
        }
        
        /* 隱藏 expander 的展開圖標 */
        [data-testid="stExpander"] .streamlit-expanderToggle {
            display: none !important;
        }
        
        /* 隱藏 expander 的展開箭頭圖標 */
        [data-testid="stExpander"] .streamlit-expanderHeader::after {
            display: none !important;
        }
        
        /* 讓 expander 標題更簡潔 */
        [data-testid="stExpander"] .streamlit-expanderHeader {
            font-size: 0.9rem !important;
            font-weight: 600 !important;
        }
        
        /* 隱藏所有可能的展開圖標文字 */
        [data-testid="stExpander"] *[class*="expander"] *[class*="arrow"] {
            display: none !important;
        }
        
        /* 讓右側檢查項目往上移動 */
        .stColumn:last-child {
            margin-top: -20px !important;
            padding-top: 0 !important;
        }
        
        /* 隱藏 expander 的展開箭頭和文字 */
        [data-testid="stExpander"] .streamlit-expanderHeader {
            position: relative;
        }
        
        [data-testid="stExpander"] .streamlit-expanderHeader::after {
            content: "" !important;
            display: none !important;
        }
        
        /* 隱藏 expander 的展開圖標文字 - 使用更精確的選擇器 */
        [data-testid="stExpander"] .streamlit-expanderHeader {
            overflow: hidden !important;
        }
        
        [data-testid="stExpander"] .streamlit-expanderHeader > *:not(:first-child) {
            display: none !important;
        }
        
        /* 隱藏所有可能的展開圖標 */
        [data-testid="stExpander"] .streamlit-expanderHeader [class*="expanderToggle"],
        [data-testid="stExpander"] .streamlit-expanderHeader [class*="arrow"],
        [data-testid="stExpander"] .streamlit-expanderHeader [class*="icon"],
        [data-testid="stExpander"] .streamlit-expanderHeader svg {
            display: none !important;
            visibility: hidden !important;
        }
        
        /* 隱藏 expander 中的 Material Icons 文字 */
        [data-testid="stExpander"] .streamlit-expanderHeader *[class*="material-icons"],
        [data-testid="stExpander"] .streamlit-expanderHeader *[class*="MuiIcon"] {
            display: none !important;
        }
        
        /* 強制隱藏所有 expander 中的圖標文字 */
        [data-testid="stExpander"] .streamlit-expanderHeader * {
            font-family: 'Noto Sans TC', 'Inter', sans-serif !important;
        }
        
        /* 隱藏 expander 中所有包含特定字符的元素 */
        [data-testid="stExpander"] .streamlit-expanderHeader *:contains("keyboard_double_arrow"),
        [data-testid="stExpander"] .streamlit-expanderHeader *:contains("▼"),
        [data-testid="stExpander"] .streamlit-expanderHeader *:contains("▶") {
            display: none !important;
        }
        
        /* 自定義摺疊按鈕樣式 */
        .stButton > button[key="toggle_secondary_orders"] {
            background: linear-gradient(135deg, #17a2b8 0%, #138496 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 8px 12px !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            margin-bottom: 8px !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stButton > button[key="toggle_secondary_orders"]:hover {
            background: linear-gradient(135deg, #138496 0%, #117a8b 100%) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 添加 JavaScript 來強制隱藏圖標文字
        st.markdown("""
        <script>
        // 等待頁面加載完成後執行
        setTimeout(function() {
            // 查找所有包含 keyboard_double_arrow 文字的元素
            const elements = document.querySelectorAll('*');
            elements.forEach(function(element) {
                if (element.textContent && element.textContent.includes('keyboard_double_arrow')) {
                    element.style.display = 'none';
                    element.style.visibility = 'hidden';
                }
            });
            
            // 查找所有 expander 中的圖標元素
            const expanders = document.querySelectorAll('[data-testid="stExpander"]');
            expanders.forEach(function(expander) {
                const header = expander.querySelector('.streamlit-expanderHeader');
                if (header) {
                    // 隱藏除了標題文字以外的所有子元素
                    const children = header.children;
                    for (let i = 1; i < children.length; i++) {
                        children[i].style.display = 'none';
                    }
                }
            });
        }, 100);
        </script>
        """, unsafe_allow_html=True)
    
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
    
    def _render_secondary_orders(self, on_order_action: Optional[Callable] = None) -> None:
        """渲染次要檢查項目（第二層，可摺疊）"""
        
        def render_secondary_content():
            """渲染次要檢查內容"""
            st.markdown("""
            <div class="category-header secondary">
                <span class="category-icon">⚕️</span>
                <span>次要檢查</span>
            </div>
            """, unsafe_allow_html=True)
            
            # 渲染次要檢查項目
            for order in self.orders_data["secondary"]:
                self._render_order_item(order, on_order_action)
        
        # 使用自定義 toggle 替代 st.expander
        create_custom_expander(
            title="其他檢查與治療",
            content_func=render_secondary_content,
            key="secondary_orders_toggle",
            style="arrows",
            default_expanded=False
        )
    
    def _render_order_item(self, order: Dict, on_order_action: Optional[Callable] = None) -> None:
        """渲染單個檢查項目"""
        
        # 根據優先級設定樣式
        priority_class = f"{order['priority']}-priority"
        
        # 創建按鈕內容
        priority_text = "緊急" if order['priority'] == 'critical' else "次要"
        
        # 使用 Streamlit 的 button 來處理點擊，但自定義樣式
        if st.button(
            f"{order['icon']} {order['name']} - {order['description']}",
            key=f"order_action_{order['id']}",
            use_container_width=True,
            type="primary" if order['priority'] == 'critical' else "secondary"
        ):
            if on_order_action:
                image_filename = order.get("image_path")
                image_path = self._get_image_path(image_filename) if image_filename else None
                on_order_action(order["action"], image_path)
    
    def _get_image_path(self, image_filename: str) -> Optional[str]:
        """獲取圖片完整路徑"""
        if not image_filename:
            return None
        
        # 首先檢查assets/images目錄
        assets_path = Path(__file__).parent.parent.parent.parent / "assets" / "images" / image_filename
        if assets_path.exists():
            return str(assets_path)
        
        # 然後檢查根目錄（向下兼容）
        root_path = Path(__file__).parent.parent.parent.parent / image_filename
        if root_path.exists():
            return str(root_path)
        
        # 然後檢查static目錄
        static_path = Path(__file__).parent.parent.parent.parent / "static" / "samples" / image_filename
        if static_path.exists():
            return str(static_path)
        
        return None
    
    def display_order_result(self, order_id: str, result_text: str, image_path: Optional[str] = None) -> None:
        """顯示Order執行結果"""
        if image_path:
            image_full_path = self._get_image_path(image_path)
            if image_full_path and os.path.exists(image_full_path):
                st.image(image_full_path, caption=f"{order_id} 檢查結果", use_container_width=True)
        
        st.markdown(f"**[系統訊息]** {result_text}")
    
    def get_order_by_id(self, order_id: str) -> Optional[Dict]:
        """根據ID獲取Order資訊"""
        # 搜尋所有類別
        for category_orders in self.orders_data.values():
            for order in category_orders:
                if order["id"] == order_id:
                    return order
        return None
