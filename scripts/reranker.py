import re


#Additional weighting applied after vector retrieval
SOURCE_AUTHORITY_BONUS = {
    "documentation": 0.15,
    "blog": 0.08,
    "forum": 0.03,
}


def extract_keywords(text):

    #Simple keyword extraction for reranking
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

    return set(words)


def keyword_overlap_score(query, chunk_text):

    query_words = extract_keywords(query)
    chunk_words = extract_keywords(chunk_text)

    if not query_words:
        return 0

    overlap = len(query_words.intersection(chunk_words))

    return overlap / len(query_words)


def rerank(query, retrieved_results):

    reranked = []

    for result in retrieved_results:

        keyword_score = keyword_overlap_score(
            query,
            result["text"]
        )

        source_bonus = SOURCE_AUTHORITY_BONUS.get(
            result["source_type"],
            0
        )

        #Combine retrieval score with keyword matching
        rerank_score = (
            result["weighted_score"]
            + (keyword_score * 0.25)
            + source_bonus
        )

        result["keyword_score"] = keyword_score
        result["rerank_score"] = rerank_score

        reranked.append(result)

    reranked.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked