# Performance Analysis

## Overview

To evaluate the system, I ran 10 OpenEMR support questions across documentation, PDF manuals, blogs, and forum discussions.

The goal was to see how well the retrieval pipeline could find relevant information and whether the reranking strategy helped prioritize better sources before sending context to the LLM.

---

## Retrieval Performance

The retrieval pipeline uses ChromaDB with sentence-transformer embeddings (`all-MiniLM-L6-v2`).

For each question, the system creates an embedding, retrieves matching chunks, filters low similarity results, and then reranks the remaining chunks before building the final prompt.

Overall retrieval worked best for questions that were directly covered by documentation and user guides. Questions about patient portal setup, upgrades, security, facilities, and adding patients all returned relevant chunks.

Blog retrieval also worked fairly well. Questions about OpenEMR version 8 and ONC certification were able to retrieve the correct blog posts and generate reasonable answers.

Forum retrieval was more mixed. This was expected since I only collected 15 forum threads. Some forum questions returned useful troubleshooting information while others did not have enough matching content.

---

## Reranking Performance

After retrieval, a simple reranking strategy was used.

The reranking score combines:

* Vector similarity
* Source authority score
* Keyword overlap

Documentation was given the highest authority score, followed by blogs and then forums.

This helped push official documentation higher in the rankings when multiple source types were retrieved. In most cases the documentation sources appeared near the top of the results, which generally led to better answers.

The reranking approach is fairly simple but it worked well enough for this project and was easy to implement.

---

## Contradiction Handling

The project requirements asked for a mechanism to handle contradictions between sources.

My approach was to assign authority scores to different source types:

* Documentation = 3
* Blog = 2
* Forum = 1

If multiple source types were retrieved, documentation was prioritized over blogs and forums.

This does not actually verify facts or detect contradictions directly. Instead it assumes that official documentation is generally more reliable than community discussions. For this project that seemed like a reasonable tradeoff.

---

## Results

I tested the system using 10 questions.

Approximate results:

| Result Type              | Count |
| ------------------------ | ----: |
| Strong Responses         |     8 |
| Partial Responses        |     1 |
| Insufficient Information |     1 |

Most questions returned useful answers with relevant supporting sources.

One interesting result was the question about patient appointment scheduling through the portal. The system could not find enough information to answer confidently and instead stated that the available sources were insufficient. While this is not a perfect answer, it is preferable to hallucinating information.

---

## Observations

A few things stood out during testing.

Documentation and PDF manuals produced the strongest answers by far. This makes sense because they contain structured instructions and procedures.

Blog posts were useful for release-related questions and certification information.

Forums were the least consistent source. Some threads contained very useful troubleshooting information, but the overall forum dataset was small so coverage was limited.

I also noticed occasional retrieval noise where a forum chunk would appear in results even though it was not directly related to the question.

Another issue I encountered during development was context window overflow. Initially I was sending too many retrieved chunks to Gemma which caused the model to stop generating after a single word. Limiting the number of chunks and truncating long chunks fixed the issue.

---

## Conclusion

Overall I was happy with the performance of the retrieval and reranking pipeline given the size of the dataset and the assigmnet requirements.

The strongest results came from documentation and PDF-based questions. Blog retrieval worked well for release information and certification questions. Forum retrieval was less reliable due to the smaller dataset but still provided useful troubleshooting examples.

The combination of semantic retrieval, source weighting, reranking, and context filtering was enough to produce grounded answers for most of the evaluation questions without requiring more complex techniques.
