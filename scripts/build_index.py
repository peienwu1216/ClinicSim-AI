import os
import sys
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.image_processor import process_images_in_directory

# --- 設定 ---
DOCUMENTS_PATH = "documents"  # 將你的 PDF、TXT 檔案放在這裡
INDEX_PATH = "faiss_index"    # 向量資料庫儲存路徑
EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5" # 中英雙語皆表現優異的開源模型

def build_index():
    """
    讀取 documents 資料夾中的所有文件，將其轉換為向量並建立 FAISS 索引。
    這是一個一次性的過程，在開發前運行即可。
    """
    print("--- 開始建立 RAG 向量索引 ---")
    
    if not os.path.exists(DOCUMENTS_PATH):
        os.makedirs(DOCUMENTS_PATH)
        print(f"已建立 '{DOCUMENTS_PATH}' 資料夾，請將你的 PDF、TXT 文件放入其中後再執行一次。")
        return

    # 1. 載入所有文件
    all_docs = []
    p = Path(DOCUMENTS_PATH)
    
    # 載入 PDF 和文字檔案
    for file in p.glob('**/*'):
        if file.is_dir():
            continue
        try:
            if file.suffix == '.pdf':
                print(f"正在載入 PDF: {file.name}")
                loader = PyMuPDFLoader(str(file))
                docs = loader.load()
                # 確保每個文檔都有正確的來源資訊
                for doc in docs:
                    # PyMuPDFLoader 會自動在 metadata 中包含 'source' 和 'page' 資訊
                    # 我們只需要確保這些資訊存在
                    if 'source' not in doc.metadata:
                        doc.metadata['source'] = str(file)
                    if 'page' not in doc.metadata:
                        doc.metadata['page'] = 0  # 預設頁碼
                    print(f"  - 頁面 {doc.metadata.get('page', 0) + 1}: {len(doc.page_content)} 字元")
                all_docs.extend(docs)
            elif file.suffix in ['.txt', '.md']:
                print(f"正在載入文字檔: {file.name}")
                loader = TextLoader(str(file), encoding='utf-8')
                docs = loader.load()
                # 為文字檔案添加來源資訊
                for doc in docs:
                    doc.metadata['source'] = str(file)
                    doc.metadata['page'] = 0  # 文字檔案沒有頁碼概念
                all_docs.extend(docs)
        except Exception as e:
            print(f"載入檔案 {file.name} 失敗: {e}")
    
    # 載入圖片檔案
    print("\n--- 開始處理圖片檔案 ---")
    image_docs = process_images_in_directory(p, method="easyocr")
    all_docs.extend(image_docs)

    if not all_docs:
        print(f"在 '{DOCUMENTS_PATH}' 資料夾中找不到任何可讀取的文件。")
        return
        
    print(f"文件載入完成，共 {len(all_docs)} 頁。開始切塊...")
    
    # 2. 切割文件 - 使用更小的chunk size以提高精準度
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,  # 減少chunk大小以提高精準度
        chunk_overlap=50,  # 減少重疊以提高精準度
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]  # 更細緻的分隔符
    )
    chunks = text_splitter.split_documents(all_docs)
    print(f"切塊完成，共生成 {len(chunks)} 個知識片段。")
    
    # 3. 過濾低品質的chunks
    filtered_chunks = []
    for chunk in chunks:
        content = chunk.page_content.strip()
        
        # 過濾太短的chunks
        if len(content) < 30:
            continue
            
        # 過濾包含太多無意義內容的chunks
        if content.count('案例') > 2 or content.count('案例1') > 0:
            continue
            
        # 過濾只包含標題的chunks
        if content.count('\n') == 0 and len(content) < 100:
            continue
            
        filtered_chunks.append(chunk)
    
    chunks = filtered_chunks
    print(f"過濾後，共保留 {len(chunks)} 個高品質知識片段。")

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
