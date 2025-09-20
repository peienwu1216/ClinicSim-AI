
import requests
from openai import OpenAI
import base64

def call_ai(messages: str)-> str:
    r = requests.get("http://localhost:8000/api/v1/models")

    # Initialize the client to use Lemonade Server
    client = OpenAI(
        base_url="http://localhost:8000/api/v1",
        api_key="lemonade"  # required but unused
    )

    # Create a chat completion
    completion = client.chat.completions.create(
        model="Qwen2.5-0.5B-Instruct-CPU",  # or any other available model
        messages=[
            {"role": "user", "content": messages}
        ]
    )

    # Print the response
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


# def call_ai_multimodal(messages: list, model: str = "squeeze-ai-lab/TinyAgent-1.1B") -> str:
#     """
#     调用多模态模型处理图像和文本
    
#     Args:
#         messages: 消息列表，可以包含文本和图像
#         model: 使用的模型名称
    
#     Returns:
#         str: AI 的响应
#     """
#     # Initialize the client to use Lemonade Server
#     client = OpenAI(
#         base_url="http://localhost:8000/api/v1",
#         api_key="lemonade"  # required but unused
#     )

#     # Create a chat completion
#     completion = client.chat.completions.create(
#         model=model,
#         messages=messages
#     )

#     # Print the response
#     print(completion.choices[0].message.content)
#     return completion.choices[0].message.content


call_ai( "What is the capital of France?")