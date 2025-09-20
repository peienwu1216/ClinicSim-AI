"""
生命體徵數據模型
"""

from typing import Optional
from pydantic import BaseModel, Field


class VitalSigns(BaseModel):
    """生命體徵模型"""
    hr_bpm: Optional[int] = Field(None, description="心率 (bpm)")
    spo2_room_air: Optional[int] = Field(None, description="血氧 (%)")
    bp_mmhg: Optional[str] = Field(None, description="血壓 (mmHg)")
    rr_bpm: Optional[int] = Field(None, description="呼吸 (次/分)")
    temperature: Optional[float] = Field(None, description="體溫 (°C)")
    
    def to_dict(self) -> dict:
        """轉換為字典格式"""
        return {
            "HR_bpm": self.hr_bpm,
            "SpO2_room_air": self.spo2_room_air,
            "BP_mmHg": self.bp_mmhg,
            "RR_bpm": self.rr_bpm,
            "Temperature": self.temperature
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "VitalSigns":
        """從字典創建實例"""
        return cls(
            hr_bpm=data.get("HR_bpm"),
            spo2_room_air=data.get("SpO2_room_air"),
            bp_mmhg=data.get("BP_mmHg"),
            rr_bpm=data.get("RR_bpm"),
            temperature=data.get("Temperature")
        )
