# 使用 call_AI.py 的方法测试 lemonade server
from call_AI import call_ai

print("测试 Lemonade Server 连接...")
try:
    response = call_ai("hi")
    print("✅ 连接成功！")
    print(f"响应: {response}")
except Exception as e:
    print(f"❌ 请求失败: {e}")