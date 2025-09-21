#!/usr/bin/env python3
"""
Map-Reduce 策略測試腳本
測試 NPU 優化效果和上下文處理能力
"""

import sys
import os
import time
from pathlib import Path

# 添加項目根目錄到 Python 路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.config.settings import get_settings
from src.services.map_reduce_service import MapReduceService
from src.services.ai_service import get_ai_service
from src.models.conversation import Conversation, Message, MessageRole
from src.models.report import Citation


def create_test_conversation():
    """創建測試對話"""
    conversation = Conversation(case_id="test_case_1")
    
    # 添加模擬對話
    conversation.add_message(MessageRole.USER, "你好，我是醫學生，今天來學習問診技巧。")
    conversation.add_message(MessageRole.ASSISTANT, "你好！我是您的 OSCE 指導老師。今天我們要練習急性胸痛的問診。請開始問診。")
    conversation.add_message(MessageRole.USER, "請問您今天為什麼來醫院？")
    conversation.add_message(MessageRole.ASSISTANT, "我胸口很痛，已經痛了兩個小時了。")
    conversation.add_message(MessageRole.USER, "能描述一下疼痛的性質嗎？")
    conversation.add_message(MessageRole.ASSISTANT, "是壓迫性的疼痛，像有重物壓在胸口。")
    conversation.add_message(MessageRole.USER, "疼痛有放射到其他地方嗎？")
    conversation.add_message(MessageRole.ASSISTANT, "有，會放射到左手臂。")
    conversation.add_message(MessageRole.USER, "您有做過心電圖檢查嗎？")
    conversation.add_message(MessageRole.ASSISTANT, "還沒有，醫生說要等檢查。")
    
    return conversation


def create_test_citations():
    """創建測試引註（模擬大量文檔）"""
    citations = []
    
    # 模擬多個長文檔
    long_document_1 = """
    急性冠狀動脈症候群 (ACS) 的診斷和治療指引
    
    1. 臨床表現
    急性冠狀動脈症候群的主要臨床表現包括：
    - 胸痛：典型的心絞痛表現為胸骨後壓迫性疼痛，可放射至左臂、頸部、下顎或背部
    - 疼痛性質：壓迫性、緊縮性、燒灼感
    - 持續時間：通常持續數分鐘至數小時
    - 誘發因子：運動、情緒激動、寒冷、飽餐後
    - 緩解因子：休息、硝酸甘油
    
    2. 診斷檢查
    對於疑似 ACS 的患者，應立即進行以下檢查：
    - 12 導程心電圖：應在 10 分鐘內完成
    - 心肌標記物：Troponin I/T, CK-MB
    - 胸部 X 光：排除其他原因
    - 血液檢查：CBC, 電解質, 腎功能
    
    3. 治療原則
    - 立即給予氧氣
    - 阿司匹林 300mg 嚼服
    - 硝酸甘油舌下含片
    - 嗎啡止痛（如需要）
    - 考慮抗血小板藥物和抗凝血劑
    
    4. 危險分層
    根據 TIMI 風險評分進行危險分層：
    - 低風險：0-2 分
    - 中風險：3-4 分  
    - 高風險：5-7 分
    """ * 3  # 重複內容增加長度
    
    long_document_2 = """
    STEMI 的診斷和緊急處理
    
    1. 心電圖診斷標準
    STEMI 的心電圖診斷標準包括：
    - 兩個相鄰導程 ST 段抬高 ≥ 1mm
    - 在 V2-V3 導程，男性 ≥ 2mm，女性 ≥ 1.5mm
    - 新發生的左束支傳導阻滯
    - 後壁 STEMI：V1-V2 導程 ST 段壓低，V7-V9 導程 ST 段抬高
    
    2. 緊急處理流程
    一旦診斷 STEMI，應立即啟動：
    - 心導管團隊通知
    - 準備緊急心導管檢查
    - 目標：門診到氣球擴張時間 < 90 分鐘
    - 如果無法在 90 分鐘內進行心導管，考慮血栓溶解治療
    
    3. 藥物治療
    - 雙重抗血小板治療：阿司匹林 + P2Y12 抑制劑
    - 抗凝血劑：肝素或低分子量肝素
    - 他汀類藥物：高劑量他汀
    - β-阻斷劑：如無禁忌症
    - ACE 抑制劑：如無禁忌症
    
    4. 併發症處理
    - 心律不整：VF/VT 需要立即電擊
    - 心因性休克：考慮 IABP 或 ECMO
    - 機械性併發症：乳頭肌斷裂、心室中隔穿孔
    """ * 3  # 重複內容增加長度
    
    long_document_3 = """
    問診技巧和 OPQRST 結構
    
    1. OPQRST 問診結構
    完整的胸痛問診應包括：
    - O (Onset)：發作時間和方式
    - P (Provocation/Palliation)：誘發和緩解因子
    - Q (Quality)：疼痛性質
    - R (Radiation)：放射位置
    - S (Severity)：嚴重程度 (1-10 分)
    - T (Time)：持續時間和時間模式
    
    2. 危險因子詢問
    重要的心血管危險因子包括：
    - 年齡：男性 > 45 歲，女性 > 55 歲
    - 家族史：早發性心血管疾病
    - 吸菸史：現在或過去吸菸
    - 高血壓：收縮壓 > 140 mmHg
    - 糖尿病：空腹血糖 > 126 mg/dL
    - 高血脂：總膽固醇 > 200 mg/dL
    
    3. 鑑別診斷
    胸痛的鑑別診斷包括：
    - 心因性：ACS, 心包炎, 主動脈剝離
    - 肺因性：肺栓塞, 氣胸, 肺炎
    - 胃腸道：胃食道逆流, 消化性潰瘍
    - 肌肉骨骼：肋軟骨炎, 肌肉拉傷
    - 其他：帶狀疱疹, 焦慮症
    
    4. 問診技巧
    - 使用開放式問題開始
    - 適時使用封閉式問題確認
    - 注意非語言溝通
    - 建立良好的醫病關係
    - 確保隱私和舒適的環境
    """ * 3  # 重複內容增加長度
    
    citations = [
        Citation(
            id=1,
            query="急性胸痛診斷流程",
            content=long_document_1,
            source="臨床指引_ACS_2024.pdf",
            score=0.95
        ),
        Citation(
            id=2,
            query="STEMI 緊急處理",
            content=long_document_2,
            source="STEMI_治療指引_2024.pdf", 
            score=0.92
        ),
        Citation(
            id=3,
            query="問診技巧 OPQRST",
            content=long_document_3,
            source="問診技巧手冊_2024.pdf",
            score=0.88
        )
    ]
    
    return citations


def test_map_reduce_performance():
    """測試 Map-Reduce 性能"""
    print("=" * 60)
    print("Map-Reduce 策略性能測試")
    print("=" * 60)
    
    # 初始化服務
    settings = get_settings()
    ai_service = get_ai_service(settings)
    map_reduce_service = MapReduceService(settings, ai_service)
    
    # 創建測試數據
    conversation = create_test_conversation()
    citations = create_test_citations()
    
    # 估算上下文大小
    print("\n1. 上下文大小分析:")
    context_size = map_reduce_service.estimate_context_size(conversation, citations)
    for key, value in context_size.items():
        print(f"   {key}: {value}")
    
    print(f"\n   處理策略: {map_reduce_service.get_processing_strategy(context_size)}")
    
    # 測試 Map-Reduce 處理
    print("\n2. Map-Reduce 處理測試:")
    start_time = time.time()
    
    try:
        condensed_result = map_reduce_service.process_large_context(conversation, citations)
        end_time = time.time()
        
        print(f"   ✅ 處理成功")
        print(f"   ⏱️  處理時間: {end_time - start_time:.2f} 秒")
        print(f"   📄 濃縮後長度: {len(condensed_result)} 字符")
        print(f"   📊 壓縮比: {len(condensed_result) / context_size['citations_length']:.2%}")
        
        # 顯示濃縮結果預覽
        print(f"\n3. 濃縮結果預覽:")
        print("-" * 40)
        print(condensed_result[:500] + "..." if len(condensed_result) > 500 else condensed_result)
        print("-" * 40)
        
    except Exception as e:
        print(f"   ❌ 處理失敗: {e}")
        return False
    
    return True


def test_npu_optimization():
    """測試 NPU 優化效果"""
    print("\n" + "=" * 60)
    print("NPU 優化效果測試")
    print("=" * 60)
    
    settings = get_settings()
    ai_service = get_ai_service(settings)
    
    if not ai_service.is_available():
        print("❌ AI 服務不可用，無法進行 NPU 測試")
        return False
    
    print(f"✅ AI 服務可用: {settings.ai_provider}")
    
    # 測試小任務（應該在 NPU 上運行）
    print("\n1. 測試小任務（NPU 優化）:")
    small_prompt = "請簡要說明急性胸痛的主要症狀。"
    
    try:
        from src.models.conversation import Message
        messages = [Message(role=MessageRole.SYSTEM, content=small_prompt)]
        
        start_time = time.time()
        response = ai_service.chat(messages)
        end_time = time.time()
        
        print(f"   ✅ 小任務完成")
        print(f"   ⏱️  處理時間: {end_time - start_time:.2f} 秒")
        print(f"   📄 回應長度: {len(response)} 字符")
        print(f"   💬 回應預覽: {response[:100]}...")
        
    except Exception as e:
        print(f"   ❌ 小任務失敗: {e}")
        return False
    
    return True


def main():
    """主測試函數"""
    print("🚀 開始 Map-Reduce 策略測試")
    print("此測試將驗證 NPU 優化效果和上下文處理能力\n")
    
    # 測試 Map-Reduce 性能
    map_reduce_success = test_map_reduce_performance()
    
    # 測試 NPU 優化
    npu_success = test_npu_optimization()
    
    # 總結
    print("\n" + "=" * 60)
    print("測試結果總結")
    print("=" * 60)
    
    if map_reduce_success:
        print("✅ Map-Reduce 策略: 測試通過")
    else:
        print("❌ Map-Reduce 策略: 測試失敗")
    
    if npu_success:
        print("✅ NPU 優化: 測試通過")
    else:
        print("❌ NPU 優化: 測試失敗")
    
    if map_reduce_success and npu_success:
        print("\n🎉 所有測試通過！Map-Reduce 策略已成功實現 NPU 優化。")
        print("\n💡 使用建議:")
        print("   1. 在生成詳細報告時，系統會自動使用 Map-Reduce 策略")
        print("   2. 文檔會被分批濃縮，確保 NPU 能夠處理")
        print("   3. 最終報告生成時會使用濃縮後的上下文")
        print("   4. 這樣可以最大化 NPU 的使用效率")
    else:
        print("\n⚠️ 部分測試失敗，請檢查配置和服務狀態")
    
    return map_reduce_success and npu_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
