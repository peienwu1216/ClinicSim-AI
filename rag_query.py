from tavily_client import search_tavily
from vector_store import VectorStore
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 1. 用 Tavily 查資料
query = "蟑螂蛋餅"
docs = search_tavily(query, limit=5)
print(docs)

# 2. 建立向量資料庫
vs = VectorStore()
vs.build(docs)

# 3. 問問題，找到最相關資料
question = "好吃的早餐"
top_docs = vs.query(question, top_k=3)

# 4. 把問題和檢索到的資料送給 LLM 生成答案
context = "\n".join(top_docs)
messages = [
    {"role": "system", "content": "你是一個助理，根據提供的資料回答問題。"},
    {"role": "user", "content": f"根據以下資料回答問題：\n{context}\n\n問題：{question}"}
]

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0,
    max_tokens=300
)

print("=== RAG 回答 ===")
print(response.choices[0].message.content.strip())
