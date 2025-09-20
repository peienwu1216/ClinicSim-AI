"""
緊湊版臨床檢測Orders組件 - 適合右上角顯示
"""

import streamlit as st
from typing import Dict, List, Optional, Callable
import os
from pathlib import Path

from .base import BaseComponent


class ClinicalOrdersCompactComponent(BaseComponent):
    """緊湊版臨床檢測Orders組件"""
    
    def __init__(self, key: str):
        super().__init__(key)
        self.orders_data = self._initialize_compact_orders_data()
    
    def _initialize_compact_orders_data(self) -> Dict:
        """初始化緊湊版臨床檢測Orders數據"""
        return {
            "bedside": {
                "title": "床邊檢查",
                "icon": "⚕️",
                "orders": [
                    {
                        "id": "ecg",
                        "name": "ECG",
                        "description": "心電圖",
                        "action": "我現在要為病人安排12導程心電圖檢查",
                        "enabled": True,
                        "image_path": "ecg_sample.png"
                    },
                    {
                        "id": "pocus",
                        "name": "POCUS",
                        "description": "超音波",
                        "action": "執行床邊超音波，確認心包膜或肺部狀況",
                        "enabled": False,
                        "image_path": None
                    }
                ]
            },
            "labs": {
                "title": "實驗室",
                "icon": "🩸",
                "orders": [
                    {
                        "id": "troponin",
                        "name": "Troponin",
                        "description": "心肌酵素",
                        "action": "幫病人抽血，檢驗 Cardiac Troponin I",
                        "enabled": True,
                        "image_path": None
                    },
                    {
                        "id": "cbc",
                        "name": "CBC",
                        "description": "血球計數",
                        "action": "檢驗 CBC/DC，確認是否有貧血或感染",
                        "enabled": True,
                        "image_path": None
                    }
                ]
            },
            "imaging": {
                "title": "影像學",
                "icon": "🖥️",
                "orders": [
                    {
                        "id": "chest_xray",
                        "name": "CXR",
                        "description": "胸部X光",
                        "action": "安排 Portable Chest X-ray，確認是否有氣胸或主動脈剝離等問題",
                        "enabled": True,
                        "image_path": "chest_xray_sample.png"
                    }
                ]
            },
            "medications": {
                "title": "藥物",
                "icon": "💊",
                "orders": [
                    {
                        "id": "oxygen",
                        "name": "O₂",
                        "description": "氧氣",
                        "action": "給予病人氧氣，維持血氧濃度 > 94%",
                        "enabled": True,
                        "image_path": None
                    },
                    {
                        "id": "aspirin",
                        "name": "Aspirin",
                        "description": "阿斯匹靈",
                        "action": "給予 Aspirin 160-325mg 口嚼",
                        "enabled": True,
                        "image_path": None
                    },
                    {
                        "id": "ntg",
                        "name": "NTG",
                        "description": "硝化甘油",
                        "action": "給予 Nitroglycerin (NTG) 0.4mg 舌下含服",
                        "enabled": True,
                        "image_path": None
                    },
                    {
                        "id": "morphine",
                        "name": "Morphine",
                        "description": "嗎啡",
                        "action": "若 NTG 無法緩解胸痛，給予 Morphine 2-4mg IV",
                        "enabled": True,
                        "image_path": None
                    }
                ]
            }
        }
    
    def render(self, on_order_action: Optional[Callable[[str, Optional[str]], None]] = None) -> None:
        """渲染緊湊版臨床檢測Orders面板"""
        
        # 應用緊湊版CSS
        self._apply_compact_css()
        
        # 使用st.container創建右上角區域
        with st.container():
            st.markdown("""
            <div class="clinical-orders-compact">
                <div class="compact-header">
                    <span class="compact-icon">📋</span>
                    <span class="compact-title">臨床決策</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 創建緊湊版分頁
            tab_titles = [
                "⚕️ 床邊",
                "🩸 實驗室", 
                "🖥️ 影像",
                "💊 藥物"
            ]
            
            tabs = st.tabs(tab_titles)
            
            # 渲染每個分頁
            for i, (category_key, category_data) in enumerate(self.orders_data.items()):
                with tabs[i]:
                    self._render_compact_category_orders(category_data, on_order_action)
    
    def _apply_compact_css(self):
        """應用緊湊版CSS樣式"""
        st.markdown("""
        <style>
        .clinical-orders-compact {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 16px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .compact-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .compact-icon {
            font-size: 1.2rem;
            color: #2563eb;
        }
        
        .compact-title {
            font-size: 1rem;
            font-weight: 600;
            color: #2563eb;
        }
        
        /* 緊湊版分頁 */
        .clinical-orders-compact .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            margin-bottom: 8px;
        }
        
        .clinical-orders-compact .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 0.8rem;
            font-weight: 500;
            min-height: auto;
        }
        
        .clinical-orders-compact .stTabs [data-baseweb="tab-panel"] {
            padding: 8px 0;
        }
        
        /* 緊湊版按鈕 */
        .clinical-orders-compact .stButton > button {
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 0.75rem;
            min-height: auto;
            height: auto;
            line-height: 1.2;
        }
        
        /* 按鈕佈局 */
        .compact-button-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
            gap: 6px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_compact_category_orders(self, category_data: Dict, on_order_action: Optional[Callable] = None) -> None:
        """渲染緊湊版特定類別的Orders"""
        orders = category_data["orders"]
        
        # 根據類別決定佈局
        if category_data["title"] == "床邊檢查":
            cols = st.columns(len(orders))
            for i, order in enumerate(orders):
                with cols[i]:
                    self._render_compact_order_button(order, on_order_action)
        
        elif category_data["title"] == "實驗室":
            cols = st.columns(len(orders))
            for i, order in enumerate(orders):
                with cols[i]:
                    self._render_compact_order_button(order, on_order_action)
        
        elif category_data["title"] == "影像學":
            cols = st.columns(len(orders))
            for i, order in enumerate(orders):
                with cols[i]:
                    self._render_compact_order_button(order, on_order_action)
        
        else:  # 藥物處方
            cols = st.columns(len(orders))
            for i, order in enumerate(orders):
                with cols[i]:
                    self._render_compact_order_button(order, on_order_action)
    
    def _render_compact_order_button(self, order: Dict, on_order_action: Optional[Callable] = None) -> None:
        """渲染緊湊版Order按鈕"""
        if order["enabled"]:
            if st.button(
                f"**{order['name']}**\n{order['description']}", 
                use_container_width=True,
                disabled=False,
                key=f"compact_order_{order['id']}"
            ):
                if on_order_action:
                    image_path = order.get("image_path")
                    on_order_action(order["action"], image_path)
        else:
            st.button(
                f"**{order['name']}**\n{order['description']}", 
                use_container_width=True,
                disabled=True,
                key=f"compact_order_{order['id']}_disabled"
            )
            st.caption("🔒", help="即將推出")
    
    def _get_image_path(self, image_filename: str) -> Optional[str]:
        """獲取圖片完整路徑"""
        if not image_filename:
            return None
        
        # 檢查static目錄
        static_path = Path(__file__).parent.parent.parent.parent / "static" / "samples" / image_filename
        if static_path.exists():
            return str(static_path)
        
        return None
    
    def display_order_result(self, order_id: str, result_text: str, image_path: Optional[str] = None) -> None:
        """顯示Order執行結果"""
        if image_path:
            image_full_path = self._get_image_path(image_path)
            if image_full_path and os.path.exists(image_full_path):
                st.image(image_full_path, caption=f"{order_id} 檢查結果", use_column_width=True)
        
        st.markdown(f"**[系統訊息]** {result_text}")
    
    def get_order_by_id(self, order_id: str) -> Optional[Dict]:
        """根據ID獲取Order資訊"""
        for category_data in self.orders_data.values():
            for order in category_data["orders"]:
                if order["id"] == order_id:
                    return order
        return None
