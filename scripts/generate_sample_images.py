"""
生成臨床檢測樣本圖片
包括ECG、胸部X光等
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_ecg_sample():
    """創建ECG樣本圖片"""
    # 創建圖形
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('white')
    
    # 模擬ECG信號 - STEMI (V1-V4 ST elevation)
    time = np.linspace(0, 4, 2000)  # 4秒的ECG
    
    # 基本心律
    heart_rate = 75
    rr_interval = 60 / heart_rate
    
    # 生成多個心跳
    ecg_signal = np.zeros_like(time)
    
    for i in range(5):  # 5個心跳
        beat_start = i * rr_interval
        
        # P波
        p_wave = np.exp(-((time - beat_start - 0.1) / 0.02) ** 2) * 0.1
        
        # QRS複合波
        qrs_start = beat_start + 0.15
        qrs = np.exp(-((time - qrs_start) / 0.02) ** 2) * 0.8
        
        # T波
        t_start = beat_start + 0.35
        t_wave = np.exp(-((time - t_start) / 0.08) ** 2) * 0.3
        
        # 在V1-V4導程添加ST段抬高
        if i < 3:  # 前3個心跳顯示STEMI
            st_elevation = np.exp(-((time - beat_start - 0.2) / 0.1) ** 2) * 0.4
            st_elevation = np.where((time > beat_start + 0.15) & (time < beat_start + 0.25), st_elevation, 0)
            ecg_signal += p_wave + qrs + t_wave + st_elevation
        else:
            ecg_signal += p_wave + qrs + t_wave
    
    # 添加基線漂移
    baseline = 0.05 * np.sin(2 * np.pi * 0.5 * time)
    ecg_signal += baseline
    
    # 繪製ECG
    ax.plot(time, ecg_signal, 'b-', linewidth=1.5, color='#2563eb')
    
    # 設置圖形屬性
    ax.set_xlim(0, 4)
    ax.set_ylim(-0.5, 1.2)
    ax.set_xlabel('時間 (秒)', fontsize=12, fontweight='bold')
    ax.set_ylabel('振幅 (mV)', fontsize=12, fontweight='bold')
    ax.set_title('12導程心電圖 - Lead V1-V4 (STEMI)', fontsize=16, fontweight='bold', pad=20)
    
    # 添加網格
    ax.grid(True, alpha=0.3)
    
    # 添加註釋
    ax.annotate('ST段抬高', xy=(0.8, 0.7), xytext=(1.5, 0.9),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=12, color='red', fontweight='bold')
    
    ax.annotate('異常Q波', xy=(0.6, 0.3), xytext=(1.2, 0.5),
                arrowprops=dict(arrowstyle='->', color='orange', lw=2),
                fontsize=12, color='orange', fontweight='bold')
    
    # 添加導程標籤
    ax.text(0.02, 0.95, 'Lead V1-V4', transform=ax.transAxes, 
            fontsize=14, fontweight='bold', 
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))
    
    # 移除頂部和右側邊框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    # 保存圖片
    output_path = Path(__file__).parent / "static" / "samples" / "ecg_sample.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"ECG樣本圖片已保存到: {output_path}")

def create_chest_xray_sample():
    """創建胸部X光樣本圖片"""
    # 創建圖形
    fig, ax = plt.subplots(figsize=(10, 12))
    fig.patch.set_facecolor('black')
    
    # 模擬胸部X光 - 正常
    # 創建一個簡單的胸部輪廓
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-8, 8, 100)
    X, Y = np.meshgrid(x, y)
    
    # 模擬肺部區域
    lungs = np.sqrt((X + 1.5)**2 + (Y - 0.5)**2) < 2.5
    lungs += np.sqrt((X - 1.5)**2 + (Y - 0.5)**2) < 2.5
    
    # 模擬心臟輪廓
    heart = np.sqrt((X)**2 + (Y - 1)**2) < 1.8
    
    # 模擬肋骨
    ribs = np.zeros_like(X)
    for i in range(-3, 4):
        rib_y = i * 1.2
        if abs(rib_y) < 6:
            rib = np.sqrt((X)**2 + (Y - rib_y)**2) > 4.5
            ribs += rib * 0.3
    
    # 組合所有元素
    chest_image = lungs * 0.8 + heart * 0.9 + ribs * 0.4
    chest_image = np.clip(chest_image, 0, 1)
    
    # 反轉顏色（X光是負片）
    chest_image = 1 - chest_image
    
    # 顯示圖片
    ax.imshow(chest_image, cmap='gray', extent=[-5, 5, -8, 8])
    ax.set_xlim(-5, 5)
    ax.set_ylim(-8, 8)
    
    # 設置標題
    ax.set_title('胸部X光 - 前後位 (AP View)', fontsize=16, fontweight='bold', 
                color='white', pad=20)
    
    # 移除軸
    ax.axis('off')
    
    # 添加標籤
    ax.text(0.02, 0.95, 'Normal Chest X-ray', transform=ax.transAxes, 
            fontsize=14, fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.8))
    
    plt.tight_layout()
    
    # 保存圖片
    output_path = Path(__file__).parent / "static" / "samples" / "chest_xray_sample.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='black')
    plt.close()
    
    print(f"胸部X光樣本圖片已保存到: {output_path}")

def create_lab_results_sample():
    """創建實驗室檢查結果樣本"""
    # 創建圖形
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white')
    
    # 實驗室數據
    tests = ['Troponin I', 'CK-MB', 'LDH', 'CBC-WBC', 'CBC-RBC', 'PT', 'aPTT']
    values = [2.5, 15.2, 280, 12000, 4.2, 12.5, 35]
    normal_ranges = ['<0.04', '<5.0', '120-240', '4000-10000', '4.5-5.5', '11-13', '25-35']
    units = ['ng/mL', 'U/L', 'U/L', '/μL', '×10⁶/μL', 'sec', 'sec']
    colors = ['red', 'red', 'orange', 'orange', 'green', 'green', 'green']
    
    # 創建表格
    y_positions = np.arange(len(tests))
    
    # 繪製背景條
    for i, (test, value, normal_range, unit, color) in enumerate(zip(tests, values, normal_ranges, units, colors)):
        # 背景條
        ax.barh(i, value, height=0.6, color=color, alpha=0.3)
        
        # 數值標籤
        ax.text(value + 0.1, i, f'{value} {unit}', va='center', fontweight='bold')
        
        # 正常範圍
        ax.text(-2, i, normal_range, va='center', ha='right', fontsize=10, 
                bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgray', alpha=0.7))
    
    # 設置y軸
    ax.set_yticks(y_positions)
    ax.set_yticklabels(tests, fontweight='bold')
    
    # 設置x軸
    ax.set_xlim(-8, 15)
    ax.set_xlabel('數值', fontweight='bold')
    
    # 設置標題
    ax.set_title('實驗室檢查結果', fontsize=16, fontweight='bold', pad=20)
    
    # 添加圖例
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor='red', alpha=0.3, label='異常升高'),
        plt.Rectangle((0,0),1,1, facecolor='orange', alpha=0.3, label='邊界值'),
        plt.Rectangle((0,0),1,1, facecolor='green', alpha=0.3, label='正常範圍')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # 移除頂部和右側邊框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    # 保存圖片
    output_path = Path(__file__).parent / "static" / "samples" / "lab_results_sample.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"實驗室檢查結果樣本圖片已保存到: {output_path}")

def main():
    """主函數"""
    print("開始生成臨床檢測樣本圖片...")
    
    # 確保目錄存在
    samples_dir = Path(__file__).parent / "static" / "samples"
    samples_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成各種樣本圖片
    create_ecg_sample()
    create_chest_xray_sample()
    create_lab_results_sample()
    
    print("所有樣本圖片生成完成！")

if __name__ == "__main__":
    main()
