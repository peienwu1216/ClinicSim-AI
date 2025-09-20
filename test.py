from tavily import TavilyClient
from dotenv import load_dotenv
import os

# 讀取 .env
load_dotenv()  
API_KEY = os.getenv("TAVILY_API_KEY")
if not API_KEY:
    raise ValueError("請先設定環境變數 TAVILY_API_KEY")

# 建立 Tavily client
client = TavilyClient(API_KEY)

# 想查詢的問題
query = "大腸桿菌"

# 使用 search 方法查詢
try:
    response = client.search(query=query, limit=3)  # limit 可選

    # 取得 results
    results = response.get("results", []) if isinstance(response, dict) else response

    if results:
        for i, item in enumerate(results, 1):
            # 使用 url 與 title 作為來源資訊
            print(f"來源 {i}: {item.get('url', 'N/A')}")
            print(f"標題: {item.get('title', 'N/A')}")
            print(f"內容: {item.get('content', 'N/A')}\n")
    else:
        print("沒有查詢到任何結果")
except Exception as e:
    print("請求失敗:", e)
