"""
NPU 優化配置
針對 AMD NPU 的上下文大小和處理策略優化
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class NPUOptimizationConfig:
    """NPU 優化配置"""
    
    # 上下文大小限制
    max_context_length: int = 2000  # 單次處理的最大上下文長度（字符）
    max_tokens_per_request: int = 500  # 單次請求的最大 token 數
    
    # 批次處理設定
    batch_size: int = 2  # 每批次處理的文檔數量
    max_batch_processing_time: int = 30  # 單批次最大處理時間（秒）
    
    # 濃縮策略
    summary_length_per_doc: int = 150  # 每個文檔的摘要長度（字符）
    max_final_context_length: int = 1000  # 最終上下文的長度限制
    
    # NPU 特定設定
    npu_recipe: str = "oga-npu"  # NPU 使用的 recipe
    fallback_recipe: str = "oga-hybrid"  # 備用 recipe
    
    # 性能監控
    enable_performance_logging: bool = True
    log_context_sizes: bool = True
    log_processing_times: bool = True
    
    def get_optimization_strategy(self, context_size: int) -> Dict[str, Any]:
        """根據上下文大小獲取優化策略"""
        if context_size <= self.max_context_length:
            return {
                "strategy": "direct",
                "description": "上下文大小適中，可以直接處理",
                "needs_map_reduce": False,
                "estimated_batches": 1
            }
        else:
            estimated_batches = (context_size // self.max_context_length) + 1
            return {
                "strategy": "map_reduce",
                "description": f"需要 Map-Reduce 策略，預計分 {estimated_batches} 個批次",
                "needs_map_reduce": True,
                "estimated_batches": estimated_batches,
                "compression_ratio": self.max_context_length / context_size
            }
    
    def get_batch_config(self, total_docs: int) -> Dict[str, Any]:
        """獲取批次處理配置"""
        num_batches = (total_docs + self.batch_size - 1) // self.batch_size
        
        return {
            "batch_size": self.batch_size,
            "num_batches": num_batches,
            "docs_per_batch": [
                min(self.batch_size, total_docs - i * self.batch_size)
                for i in range(num_batches)
            ],
            "max_processing_time": self.max_batch_processing_time
        }
    
    def should_use_npu(self, context_size: int) -> bool:
        """判斷是否應該使用 NPU"""
        return context_size <= self.max_context_length
    
    def get_fallback_strategy(self) -> Dict[str, Any]:
        """獲取備用策略配置"""
        return {
            "fallback_recipe": self.fallback_recipe,
            "reduce_batch_size": True,
            "enable_gpu_fallback": True,
            "max_retry_attempts": 2
        }


# 預設配置實例
DEFAULT_NPU_CONFIG = NPUOptimizationConfig()

# 針對不同場景的配置
CONFIGURATIONS = {
    "conservative": NPUOptimizationConfig(
        max_context_length=1500,
        batch_size=1,
        summary_length_per_doc=100
    ),
    "balanced": NPUOptimizationConfig(
        max_context_length=2000,
        batch_size=2,
        summary_length_per_doc=150
    ),
    "aggressive": NPUOptimizationConfig(
        max_context_length=3000,
        batch_size=3,
        summary_length_per_doc=200
    )
}


def get_npu_config(config_name: str = "balanced") -> NPUOptimizationConfig:
    """獲取 NPU 優化配置"""
    return CONFIGURATIONS.get(config_name, DEFAULT_NPU_CONFIG)


def estimate_processing_time(context_size: int, num_docs: int, config: NPUOptimizationConfig = None) -> Dict[str, Any]:
    """估算處理時間"""
    if config is None:
        config = DEFAULT_NPU_CONFIG
    
    strategy = config.get_optimization_strategy(context_size)
    
    if strategy["needs_map_reduce"]:
        # Map-Reduce 策略的時間估算
        batch_config = config.get_batch_config(num_docs)
        estimated_time = batch_config["num_batches"] * config.max_batch_processing_time
        return {
            "strategy": "map_reduce",
            "estimated_time_seconds": estimated_time,
            "num_batches": batch_config["num_batches"],
            "time_per_batch": config.max_batch_processing_time
        }
    else:
        # 直接處理的時間估算
        estimated_time = min(5, context_size / 1000)  # 粗略估算：每1000字符1秒
        return {
            "strategy": "direct",
            "estimated_time_seconds": estimated_time,
            "num_batches": 1,
            "time_per_batch": estimated_time
        }
