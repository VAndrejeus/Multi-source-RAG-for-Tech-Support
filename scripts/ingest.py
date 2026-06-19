import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

#Where processed chunks are stored
PROCESSED_DIR = Path("data_sources/processed")

#Where ChromaDB stores vectors
CHROMA_DIR = Path("chroma_db")

#Use same model as semantic chunking
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_chunks():

    #Load all chunk files into one list
    chunk_files = [
        PROCESSED_DIR / "documentation_chunks.json",
        PROCESSED_DIR / "blog_chunks.json",
        PROCESSED_DIR / "forum_chunks.json",
    ]

    chunks = []

    for file_path in chunk_files:

        with open(file_path, "r", encoding="utf-8") as f:
            chunks.extend(json.load(f))

    return chunks


def main():

    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks")

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    #Reset collection so ingestion is repeatable
    try:
        client.delete_collection("openemr_support")
    except Exception:
        pass

    collection = client.create_collection(
        name="openemr_support"
    )

    documents = []
    ids = []
    metadatas = []

    for chunk in chunks:

        documents.append(chunk["chunk_text"])
        ids.append(chunk["chunk_id"])

        #Chroma metadata must be simple values
        metadatas.append({
            "source_type": chunk.get("source_type", ""),
            "document_type": chunk.get("document_type", ""),
            "title": chunk.get("title", ""),
            "url": chunk.get("url", ""),
            "authority_score": chunk.get("authority_score", 1),
        })

    print("Creating embeddings...")

    embeddings = model.encode(
        documents,
        show_progress_bar=True
    ).tolist()

    print("Adding chunks to ChromaDB...")

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Ingested {len(documents)} chunks into ChromaDB")


if __name__ == "__main__":
    main()