from backend.agent.embedder import chroma_client, embed_text

collection = chroma_client.get_or_create_collection(name="briefai_docs")


def search_documents(query: str, n_results: int = 5):
    query_embedding = embed_text(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    if not results["ids"][0]:
        return []

    hits = []
    for i, doc in enumerate(results["documents"][0]):
        hits.append({
            "content": doc,
            "file_path": results["metadatas"][0][i]["file_path"],
            "score": round(1 - results["distances"][0][i], 3)
        })

    return hits