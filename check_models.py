import requests
import json

def check_available_models():
    """
    檢查 Lemonade Server 上可用的模型列表
    """
    try:
        print("🔍 正在檢查 Lemonade Server 上的可用模型...")
        
        # 檢查可用模型
        models_url = "http://localhost:8000/api/v1/models"
        response = requests.get(models_url)
        response.raise_for_status()
        
        models_data = response.json()
        
        print("\n📋 可用的模型列表：")
        print("=" * 50)
        
        if 'data' in models_data:
            for i, model in enumerate(models_data['data'], 1):
                model_id = model.get('id', 'N/A')
                model_name = model.get('name', 'N/A')
                print(f"{i}. ID: {model_id}")
                print(f"   名稱: {model_name}")
                print()
        else:
            print("❌ 無法解析模型資料格式")
            print("原始回應：")
            print(json.dumps(models_data, indent=2, ensure_ascii=False))
        
        return models_data
        
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到 Lemonade Server")
        print("請確認：")
        print("1. Lemonade Server 正在運行 (localhost:8000)")
        print("2. 伺服器狀態正常")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 請求失敗: {e}")
        return None

if __name__ == "__main__":
    models = check_available_models()
    
    if models:
        print("\n💡 使用建議：")
        print("1. 將上面列表中的模型 ID 複製到您的程式碼中")
        print("2. 在 test.py 中更新 'model' 參數")
        print("3. 在 build_index.py 中更新 'LEMONADE_VLM_MODEL' 參數（如果是多模態模型）")
    else:
        print("\n🚨 無法獲取模型列表，請檢查 Lemonade Server 狀態")
