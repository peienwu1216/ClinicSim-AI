from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TAVILY_API_KEY")
if not API_KEY:
    raise ValueError("請先設定環境變數 TAVILY_API_KEY")

client = TavilyClient(API_KEY)

def search_tavily(query, limit=5):
    """用 Tavily 查詢資料，回傳字典列表"""
    response = client.search(query=query, limit=limit)
    results = response.get("results", []) if isinstance(response, dict) else response
    return [
        {
            "title": item.get("title", "N/A"),
            "content": item.get("content", ""),
            "url": item.get("url", "N/A")
        }
        for item in results
    ]
