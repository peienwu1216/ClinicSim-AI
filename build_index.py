import os
import requests
import base64
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# --- 設定 ---
DOCUMENTS_PATH = "documents"  # 將你的 PDF、TXT 檔案放在這裡
INDEX_PATH = "faiss_index"    # 向量資料庫儲存路徑
EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5" # 中英雙語皆表現優異的開源模型

# --- Lemonade Server 設定 ---
LEMONADE_API_URL = "http://127.0.0.1:8080/v1/chat/completions"
LEMONADE_API_KEY = "lemonade"  # API Key 認證
LEMONADE_VLM_MODEL = "squeeze-ai-lab/TinyAgent-1.1B"   # 多模態模型

def process_images_to_documents(images_path: Path) -> list[Document]:
    """
    使用 Lemonade Server 的多模態模型處理圖像，將其轉換為文字描述並建立 Document 物件。
    
    Args:
        images_path: 圖像檔案所在的路徑
        
    Returns:
        list[Document]: 包含圖像描述的 Document 物件列表
    """
    if not images_path.exists():
        print(f"⚠️ 警告：圖像路徑 '{images_path}' 不存在。")
        return []
    
    # 导入 call_AI.py 的方法
    from call_AI import call_ai_multimodal
    
    image_documents = []
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    print(f"🔍 開始處理圖像檔案...")
    
    for image_file in images_path.glob('**/*'):
        if image_file.is_file() and image_file.suffix.lower() in supported_formats:
            try:
                print(f"📷 正在處理圖像: {image_file.name}")
                
                # 1. 讀取並編碼圖像
                with open(image_file, 'rb') as f:
                    image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                
                # 2. 準備多模态消息
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "請詳細描述這張圖片中的內容，包括所有可見的醫學相關資訊、圖表、文字等。"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{image_file.suffix[1:]};base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ]
                
                # 3. 使用 call_AI.py 的多模态方法
                description = call_ai_multimodal(messages, LEMONADE_VLM_MODEL)
                
                # 建立 Document 物件
                doc = Document(
                    page_content=description,
                    metadata={
                        "source": str(image_file),
                        "type": "image",
                        "filename": image_file.name,
                        "description_length": len(description)
                    }
                )
                image_documents.append(doc)
                print(f"✅ 圖像處理完成: {image_file.name}")
                    
            except Exception as e:
                print(f"❌ 處理圖像 {image_file.name} 時發生錯誤: {e}")
                continue
    
    print(f"🎯 圖像處理完成，共處理 {len(image_documents)} 張圖片。")
    return image_documents

def build_index():
    """
    讀取 documents 資料夾中的所有文件，將其轉換為向量並建立 FAISS 索引。
    這是一個一次性的過程，在開發前運行即可。
    支援的文件類型：PDF、TXT、MD、以及各種圖像格式。
    """
    print("--- 開始建立 RAG 向量索引 ---")
    
    if not os.path.exists(DOCUMENTS_PATH):
        os.makedirs(DOCUMENTS_PATH)
        print(f"已建立 '{DOCUMENTS_PATH}' 資料夾，請將你的 PDF、TXT 文件放入其中後再執行一次。")
        return

    # 1. 載入所有文件（文字文件）
    all_docs = []
    p = Path(DOCUMENTS_PATH)
    for file in p.glob('**/*'):
        if file.is_dir():
            continue
        try:
            if file.suffix == '.pdf':
                print(f"正在載入 PDF: {file.name}")
                loader = PyMuPDFLoader(str(file))
                all_docs.extend(loader.load())
            elif file.suffix in ['.txt', '.md']:
                print(f"正在載入文字檔: {file.name}")
                loader = TextLoader(str(file), encoding='utf-8')
                all_docs.extend(loader.load())
        except Exception as e:
            print(f"載入檔案 {file.name} 失敗: {e}")

    # 2. 處理圖像文件（如果存在）
    images_path = Path(DOCUMENTS_PATH) / "images"
    if images_path.exists():
        print("🖼️ 發現圖像資料夾，開始處理圖像...")
        image_docs = process_images_to_documents(images_path)
        all_docs.extend(image_docs)
    else:
        print("ℹ️ 未發現 'images' 子資料夾，跳過圖像處理。")

    if not all_docs:
        print(f"在 '{DOCUMENTS_PATH}' 資料夾中找不到任何可讀取的文件。")
        return
        
    print(f"文件載入完成，共 {len(all_docs)} 頁。開始切塊...")
    
    # 3. 切割文件
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = text_splitter.split_documents(all_docs)
    print(f"切塊完成，共生成 {len(chunks)} 個知識片段。")

    # 4. 初始化 Embedding 模型
    print(f"正在初始化 Embedding 模型: {EMBEDDING_MODEL} (可能需要一些時間下載)...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'trust_remote_code': True},
        encode_kwargs={'normalize_embeddings': True}
    )

    # 5. 建立 FAISS 索引並儲存
    print("正在將知識片段轉換為向量並建立 FAISS 索引...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(INDEX_PATH)
    
    print("\n--- ✅ RAG 索引建立成功！---")
    print(f"索引檔案已儲存至 '{INDEX_PATH}' 資料夾。")
    print("重要：請確保你的 .gitignore 檔案中有 `faiss_index/` 這一行。")

if __name__ == '__main__':
    build_index()
