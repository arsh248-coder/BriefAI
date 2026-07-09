import chromadb
from openai import OpenAI
import ollama
import os
import hashlib

# Persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="/app/chromadb_data")
collection = chroma_client.get_or_create_collection(name="briefai_docs")


def get_client(api_key=None):
    if api_key:
        return OpenAI(api_key=api_key)
    return OpenAI()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def embed_text(text: str, api_key=None, mode="openai"):
    if mode == "local":
        response = ollama.embeddings(model="nomic-embed-text", prompt=text)
        return response["embedding"]
    else:
        client = get_client(api_key)
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding


def embed_document(file_path: str, content: str, api_key=None, mode="openai"):
    chunks = chunk_text(content)
    for i, chunk in enumerate(chunks):
        chunk_id = hashlib.md5(f"{file_path}_{i}".encode()).hexdigest()
        embedding = embed_text(chunk, api_key=api_key, mode=mode)
        collection.upsert(
            ids=[chunk_id],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"file_path": file_path, "chunk_index": i}]
        )
    return len(chunks)


def is_document_embedded(file_path: str):
    results = collection.get(where={"file_path": file_path})
    return len(results["ids"]) > 0


def get_indexed_files():
    results = collection.get(include=["metadatas"])
    if not results["metadatas"]:
        return []
    seen = set()
    files = []
    for meta in results["metadatas"]:
        path = meta.get("file_path", "")
        if path and path not in seen:
            seen.add(path)
            files.append({
                "name": os.path.basename(path),
                "path": path
            })
    return files


def delete_document(file_path: str):
    results = collection.get(where={"file_path": file_path})
    if results["ids"]:
        collection.delete(ids=results["ids"])
    return True