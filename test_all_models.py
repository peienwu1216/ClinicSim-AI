# 使用 call_AI.py 的方法测试所有模型
from call_AI import call_ai
import json

def test_model(model_name, test_message="你好，請用繁體中文回答一個簡單的問題：1+1等於多少？"):
    """
    測試指定的模型是否正常工作
    """
    try:
        print(f"🧪 測試模型: {model_name}")
        print(f"📝 測試訊息: {test_message}")
        print("-" * 60)
        
        # 使用 call_AI.py 的方法，但需要临时修改模型
        # 由于 call_AI.py 硬编码了模型，我们需要创建一个临时函数
        content = call_ai_with_model(model_name, test_message)
        
        print(f"✅ 回應成功:")
        print(f"📤 {content}")
        print(f"⏱️  回應時間: 正常")
        return True, content
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False, str(e)

def call_ai_with_model(model_name: str, message: str) -> str:
    """
    使用指定模型调用 AI
    """
    from openai import OpenAI
    
    # Initialize the client to use Lemonade Server
    client = OpenAI(
        base_url="http://127.0.0.1:8080/api/v1",
        api_key="lemonade"  # required but unused
    )

    # Create a chat completion with specified model
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": message}
        ]
    )

    return completion.choices[0].message.content

def main():
    """
    測試所有可用的模型
    """
    models = [
        "Qwen2.5-0.5B-Instruct-CPU",
        "Llama-3.2-1B-Instruct-Hybrid", 
        "Qwen-2.5-7B-Instruct-Hybrid",
        "squeeze-ai-lab/TinyAgent-1.1B"
    ]
    
    print("🚀 開始測試所有可用模型")
    print("=" * 80)
    
    results = {}
    
    for model in models:
        success, response = test_model(model)
        results[model] = {
            'success': success,
            'response': response
        }
        print("\n" + "=" * 80 + "\n")
    
    # 總結結果
    print("📊 測試結果總結:")
    print("=" * 80)
    
    successful_models = []
    failed_models = []
    
    for model, result in results.items():
        if result['success']:
            successful_models.append(model)
            print(f"✅ {model} - 正常運作")
        else:
            failed_models.append(model)
            print(f"❌ {model} - 失敗 ({result['response']})")
    
    print(f"\n🎯 建議:")
    if successful_models:
        print(f"✅ 可用的模型: {', '.join(successful_models)}")
        print(f"💡 推薦使用: {successful_models[0]} (第一個成功的模型)")
        
        # 特別推薦
        if "Qwen-2.5-7B-Instruct-Hybrid" in successful_models:
            print(f"🌟 最佳選擇: Qwen-2.5-7B-Instruct-Hybrid (7B 參數，性能最佳)")
        elif "Qwen2.5-0.5B-Instruct-CPU" in successful_models:
            print(f"⚡ 快速選擇: Qwen2.5-0.5B-Instruct-CPU (0.5B 參數，速度最快)")
    else:
        print("❌ 沒有可用的模型，請檢查 Lemonade Server 狀態")
    
    if failed_models:
        print(f"⚠️  失敗的模型: {', '.join(failed_models)}")

if __name__ == "__main__":
    main()
