"""
臨床檢測Orders組件
提供結構化的臨床決策面板
"""

import streamlit as st
from typing import Dict, List, Optional, Callable
import os
from pathlib import Path

from .base import BaseComponent


class ClinicalOrdersComponent(BaseComponent):
    """臨床檢測Orders組件"""
    
    def __init__(self, key: str):
        super().__init__(key)
        self.orders_data = self._initialize_orders_data()
    
    def _initialize_orders_data(self) -> Dict:
        """初始化臨床檢測Orders數據"""
        return {
            "bedside": {
                "title": "床邊檢查",
                "icon": "⚕️",
                "orders": [
                    {
                        "id": "ecg",
                        "name": "12-Lead ECG",
                        "description": "12導程心電圖",
                        "action": "我現在要為病人安排12導程心電圖檢查",
                        "enabled": True,
                        "image_path": "ecg_sample.png"
                    },
                    {
                        "id": "pocus",
                        "name": "POCUS",
                        "description": "床邊超音波",
                        "action": "執行床邊超音波，確認心包膜或肺部狀況",
                        "enabled": False,
                        "image_path": None
                    }
                ]
            },
            "labs": {
                "title": "實驗室檢驗",
                "icon": "🩸",
                "orders": [
                    {
                        "id": "troponin",
                        "name": "Cardiac Enzymes",
                        "description": "心肌酵素 (Troponin I)",
                        "action": "幫病人抽血，檢驗 Cardiac Troponin I",
                        "enabled": True,
                        "image_path": None
                    },
                    {
                        "id": "cbc",
                        "name": "CBC/DC",
                        "description": "全血球計數",
                        "action": "檢驗 CBC/DC，確認是否有貧血或感染",
                        "enabled": True,
                        "image_path": None
                    },
                    {
                        "id": "coagulation",
                        "name": "Coagulation",
                        "description": "凝血功能 (PT/aPTT)",
                        "action": "檢驗 PT/aPTT，評估凝血功能",
                        "enabled": True,
                        "image_path": None
                    },
                    {
                        "id": "electrolytes",
                        "name": "Electrolytes",
                        "description": "電解質與腎功能",
                        "action": "檢驗電解質與腎功能 (Na, K, Cl, BUN, Cr)",
                        "enabled": True,
                        "image_path": None
                    }
                ]
            },
            "imaging": {
                "title": "影像學檢查",
                "icon": "🖥️",
                "orders": [
                    {
                        "id": "chest_xray",
                        "name": "Chest X-ray",
                        "description": "胸部X光",
                        "action": "安排 Portable Chest X-ray，確認是否有氣胸或主動脈剝離等問題",
                        "enabled": True,
                        "image_path": "chest_xray_sample.png"
                    },
                    {
                        "id": "ct_angio",
                        "name": "CT Angiography",
                        "description": "電腦斷層血管攝影",
                        "action": "安排 CTA for Aortic Dissection Protocol",
                        "enabled": False,
                        "image_path": None
                    }
                ]
            },
            "medications": {
                "title": "藥物處方",
                "icon": "💊",
                "orders": [
                    {
                        "id": "oxygen",
                        "name": "Oxygen",
                        "description": "氧氣治療",
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
                        "name": "Nitroglycerin",
                        "description": "硝化甘油 (NTG)",
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
        """渲染臨床檢測Orders面板"""
        st.markdown("---")
        
        # 使用自定義CSS卡片
        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-header">
                <span class="clinical-icon">📋</span>
                <div>
                    <h3 class="clinical-card-title">臨床決策 (Clinical Orders)</h3>
                    <p class="clinical-card-subtitle">點擊下方按鈕執行臨床檢測與處置</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 創建分頁
        tab_titles = [
            f"{category_data['icon']} {category_data['title']}"
            for category_data in self.orders_data.values()
        ]
        
        tabs = st.tabs(tab_titles)
        
        # 渲染每個分頁
        for i, (category_key, category_data) in enumerate(self.orders_data.items()):
            with tabs[i]:
                self._render_category_orders(category_data, on_order_action)
    
    def _render_category_orders(self, category_data: Dict, on_order_action: Optional[Callable] = None) -> None:
        """渲染特定類別的Orders"""
        orders = category_data["orders"]
        
        # 根據類別決定佈局
        if category_data["title"] == "床邊檢查":
            # 床邊檢查使用2欄佈局
            cols = st.columns(2)
            for i, order in enumerate(orders):
                with cols[i % 2]:
                    self._render_order_button(order, on_order_action)
        
        elif category_data["title"] == "實驗室檢驗":
            # 實驗室檢驗使用2欄佈局
            cols = st.columns(2)
            for i, order in enumerate(orders):
                with cols[i % 2]:
                    self._render_order_button(order, on_order_action)
        
        elif category_data["title"] == "影像學檢查":
            # 影像學檢查使用2欄佈局
            cols = st.columns(2)
            for i, order in enumerate(orders):
                with cols[i % 2]:
                    self._render_order_button(order, on_order_action)
        
        else:  # 藥物處方
            # 藥物處方使用4欄佈局
            cols = st.columns(4)
            for i, order in enumerate(orders):
                with cols[i % 4]:
                    self._render_order_button(order, on_order_action)
    
    def _render_order_button(self, order: Dict, on_order_action: Optional[Callable] = None) -> None:
        """渲染單個Order按鈕"""
        if order["enabled"]:
            if st.button(
                f"**{order['name']}**\n\n{order['description']}", 
                use_container_width=True,
                disabled=False,
                key=f"order_{order['id']}"
            ):
                if on_order_action:
                    # 傳遞action和可能的圖片路徑
                    image_path = order.get("image_path")
                    on_order_action(order["action"], image_path)
        else:
            st.button(
                f"**{order['name']}**\n\n{order['description']}", 
                use_container_width=True,
                disabled=True,
                key=f"order_{order['id']}_disabled"
            )
            st.caption("🔒 此功能即將推出")
    
    def _get_sample_image_path(self, image_filename: str) -> Optional[str]:
        """獲取樣本圖片路徑"""
        if not image_filename:
            return None
        
        # 檢查static目錄
        static_path = Path(__file__).parent.parent.parent.parent / "static" / "samples" / image_filename
        if static_path.exists():
            return str(static_path)
        
        # 如果不存在，返回None
        return None
    
    def display_order_result(self, order_id: str, result_text: str, image_path: Optional[str] = None) -> None:
        """顯示Order執行結果"""
        if image_path and os.path.exists(image_path):
            # 顯示圖片
            st.image(image_path, caption=f"{order_id} 檢查結果", use_column_width=True)
        
        # 顯示結果文字
        st.markdown(f"**[系統訊息]** {result_text}")
    
    def get_order_by_id(self, order_id: str) -> Optional[Dict]:
        """根據ID獲取Order資訊"""
        for category_data in self.orders_data.values():
            for order in category_data["orders"]:
                if order["id"] == order_id:
                    return order
        return None
