import chromadb
from openai import OpenAI
import os
import hashlib

client = OpenAI()

# Persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="/app/chromadb_data")
collection = chroma_client.get_or_create_collection(name="briefai_docs")


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


def embed_text(text: str):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


def embed_document(file_path: str, content: str):
    chunks = chunk_text(content)
    for i, chunk in enumerate(chunks):
        chunk_id = hashlib.md5(f"{file_path}_{i}".encode()).hexdigest()
        embedding = embed_text(chunk)
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