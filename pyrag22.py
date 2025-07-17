import os
import time
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import ollama

CHROMA_PATH = "./chroma_db"

# Setup embeddings model globally for reuse
print("[1] Loading embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

def load_or_create_vectorstore():
    if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
        print("[✓] Found existing Chroma DB — loading...")
        start = time.time()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        print(f"[✓] Loaded vectorstore in {time.time() - start:.2f} seconds")
        return db

    print("[!] No Chroma DB found — building from scratch...")

    start = time.time()
    loader = DirectoryLoader(r'YOUR FILE LOCATION HERE', glob="*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    print(f"[✓] Loaded {len(docs)} documents in {time.time() - start:.2f} seconds")

    start = time.time()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    print(f"[✓] Split into {len(chunks)} chunks in {time.time() - start:.2f} seconds")

    start = time.time()
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name="qwen_cache"
    )
    print(f"[✓] Created vectorstore from documents in {time.time() - start:.2f} seconds")

    start = time.time()
    db.persist()
    print(f"[✓] Persisted vectorstore to disk in {time.time() - start:.2f} seconds")

    return db

def rag_query(query: str, k: int = 3):
    print(f"[Query] Searching for top {k} chunks for query: '{query}'")
    start = time.time()
    results = vectorstore.similarity_search(query, k=k)
    print(f"[Query] Similarity search took {time.time() - start:.2f} seconds")

    context = "\n".join(doc.page_content for doc in results)

    print("[Query] Generating response with Qwen2.5 via Ollama...")
    start = time.time()
    response = ollama.generate(
        model="YOUR MODEL HERE",
        prompt=f"Using this data:\n{context}\n\nAnswer the following question:\n{query}"
    )
    print(f"[Query] Ollama generate took {time.time() - start:.2f} seconds")

    return response['response']

if __name__ == "__main__":
    vectorstore = load_or_create_vectorstore()

    while True:
        user_query = input("\nEnter your question (or 'exit' to quit): ").strip()
        if user_query.lower() in ['exit', 'quit']:
            break
        answer = rag_query(user_query)
        print("\n--- Response ---")
        print(answer)
