import requests
url = "http://localhost:8000/v1/chat/completions"
data = {"model":"Qwen3-1.7B-GGUF","messages":[{"role":"user","content":"hi"}]}
print("hi")
print(requests.post(url, json=data).text)