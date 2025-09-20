
import requests
from openai import OpenAI
import base64

def call_ai(messages: str, model: str = "Qwen2.5-0.5B-Instruct-CPU", host: str = "http://127.0.0.1:5001") -> str:
    """呼叫 AI 服務"""
    try:
        # 檢查服務是否可用
        r = requests.get(f"{host}/api/v1/models", timeout=5)
        if r.status_code != 200:
            raise Exception(f"AI 服務不可用，狀態碼: {r.status_code}")

        # Initialize the client to use Lemonade Server
        client = OpenAI(
            base_url=f"{host}/api/v1",
            api_key="lemonade"  # required but unused
        )

        # Create a chat completion
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": messages}
            ]
        )

        # Print the response
        response = completion.choices[0].message.content
        print(f"[AI Response] {response}")
        return response
        
    except Exception as e:
        error_msg = f"AI 服務錯誤: {str(e)}"
        print(f"[AI Error] {error_msg}")
        return error_msg

