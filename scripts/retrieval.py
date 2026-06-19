import chromadb
from sentence_transformers import SentenceTransformer

#Where ChromaDB is stored
CHROMA_DIR = "chroma_db"

#Same model used during ingestion
model = SentenceTransformer("all-MiniLM-L6-v2")

#Docs should carry more weight than blogs/forums, these are made up numbers anyway
SOURCE_WEIGHT = {
    "documentation": 0.15,
    "blog": 0.08,
    "forum": 0.03,
}


def retrieve(query, top_k=8):

    client = chromadb.PersistentClient(
        path=CHROMA_DIR
    )

    collection = client.get_collection(
        name="openemr_support"
    )

    #Embed user question
    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved = []

    for i in range(len(results["ids"][0])):

        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]

        #Chroma distance is lower when closer, so convert it
        similarity_score = 1 - distance

        source_type = metadata.get("source_type", "")
        weighted_score = similarity_score + SOURCE_WEIGHT.get(source_type, 0)

        retrieved.append({
            "chunk_id": results["ids"][0][i],
            "source_type": source_type,
            "title": metadata.get("title", ""),
            "url": metadata.get("url", ""),
            "similarity_score": similarity_score,
            "weighted_score": weighted_score,
            "text": results["documents"][0][i],
        })

    #Sort again after source weighting
    retrieved.sort(
        key=lambda x: x["weighted_score"],
        reverse=True
    )

    return retrieved


def main():

    query = input("Ask an OpenEMR support question: ")

    results = retrieve(query)

    print("\nTop Results:\n")

    for i, result in enumerate(results, start=1):

        print("=" * 80)
        print(f"Rank: {i}")
        print(f"Source: {result['source_type']}")
        print(f"Title: {result['title']}")
        print(f"Similarity: {result['similarity_score']:.4f}")
        print(f"Weighted Score: {result['weighted_score']:.4f}")
        print(f"URL: {result['url']}")
        print("-" * 80)
        print(result["text"][:700])
        print()


if __name__ == "__main__":
    main()