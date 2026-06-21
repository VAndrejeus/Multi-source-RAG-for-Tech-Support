# Multi-source RAG for Tech Support

## Technology Selection

### Domain Selection

OpenEMR was selected as the target software platform because it provides all three required knowledge source types:

- Product documentation
- Community forum discussions
- Technical blog posts

This enables realistic technical support question answering using publicly available sources.

### Documentation Source

Documentation data is collected from the OpenEMR Wiki and OpenEMR PDF manuals.

Web documentation is extracted using BeautifulSoup, while PDF documentation is processed using Docling.

## Documentation Collection

The documentation source was collected from the OpenEMR Wiki. Seven documentation pages were selected to provide coverage across installation, upgrades, user workflows, patient portal functionality, API usage, and security configuration.

Collected documentation pages:

* OpenEMR Wiki Home Page
* OpenEMR Installation Guides
* OpenEMR Upgrade Guides
* OpenEMR 7.0.0 Users Guide
* OpenEMR 7.0.4 API
* Patient Portal
* Securing OpenEMR

Documentation pages were scraped using the Requests and BeautifulSoup libraries and stored as structured JSON documents. Each document includes the source type, document type, title, URL, and extracted content.

During collection, some pages contained wiki navigation elements, localization content, and other non-documentation text. Rather than aggressively filtering content during collection, lightweight cleanup was deferred to the chunking stage. This approach preserved source fidelity while keeping the scraping pipeline simple and reproducible.

The collected documentation covers several common technical support topics, including installation, upgrades, scheduling, billing workflows, patient portal configuration, API integration, and security hardening. These topics provide a strong foundation for evaluating retrieval quality across realistic support questions.

### PDF Documentation

In addition to web-based documentation, two OpenEMR PDF user guides were downloaded and included as part of the documentation source.

PDF files collected:

- OpenEMR 4.1 Users Guide
- OpenEMR 3.1 Users Guide

PDF documentation will be processed with Docling so that structured document content can be extracted before chunking. This adds support for a different documentation format while keeping the source category consistent with the assignment requirement for product documentation.

Docling was initially evaluated for PDF extraction, but the selected OpenEMR PDF manuals produced memory errors during preprocessing on the local environment. To keep the pipeline reliable and reproducible, PDF text extraction was implemented with pypdf instead. PDF content was still normalized into the same documentation schema before chunking.


## Blog Collection

The second knowledge source consisted of OpenEMR technical blog posts. Blog articles were collected directly from the OpenEMR blog and stored as structured JSON documents.

A total of ten blog articles were collected covering product releases, certification efforts, interoperability initiatives, telehealth functionality, payment processing integrations, development workflows, and community announcements.

Unlike documentation pages, blog articles tend to provide higher-level explanations, implementation context, release information, and community perspectives. This makes them useful for answering questions where official documentation may not provide sufficient background information.

Blog content was extracted primarily from article paragraph elements and stored with source metadata including title, URL, and source type. The blog source serves as a secondary authority behind official documentation when answering user questions.

## Forum Collection

The third knowledge source consisted of community forum discussions collected from the OpenEMR Discourse forum.

The OpenEMR community forum uses the Discourse platform, which provides structured JSON endpoints for retrieving discussion topics and replies. Rather than scraping HTML pages, forum data was collected directly from the Discourse JSON API. This approach simplified data extraction and preserved thread structure.

A total of fifteen forum threads were collected covering technical support issues, configuration questions, feature requests, troubleshooting discussions, user workflow concerns, and community development topics.

Each forum thread was stored as a structured JSON document containing:

- Thread title
- Source URL
- Original user question
- Individual replies
- Thread metadata

Forum discussions provide a valuable source of real-world troubleshooting information that is often not available in official documentation. They also introduce the possibility of conflicting information, making forum content useful for evaluating source prioritization and contradiction handling within the retrieval pipeline.

Forum content is treated as a lower-authority source than official documentation but remains valuable for answering practical support questions and identifying common user issues.

## PDF Processing

Two OpenEMR PDF user guides were incorporated into the documentation source.

Initially, Docling was evaluated for PDF extraction. However, the selected OpenEMR manuals generated preprocessing and memory-related issues in the local environment. To ensure a reliable and reproducible pipeline, PDF text extraction was implemented using pypdf.

Extracted PDF content was normalized into the same schema used by the other documentation sources before chunking.

---

## Semantic Chunking Strategy

Different chunking strategies were applied based on the structure of each knowledge source.

### Documentation

Documentation content was chunked using a semantic paragraph-grouping strategy. Paragraph embeddings were generated using the Sentence Transformers model `all-MiniLM-L6-v2`. Consecutive paragraphs were compared using cosine similarity, and new chunks were created when semantic similarity dropped below a configured threshold or when a chunk exceeded the maximum target size.

Configuration:

- Maximum chunk size: 500 words
- Minimum chunk size: 120 words
- Similarity threshold: 0.45

### Blogs

Blog content used the same semantic chunking approach but with larger chunk sizes to preserve article context.

Configuration:

- Maximum chunk size: 600 words
- Minimum chunk size: 150 words
- Similarity threshold: 0.42

### Forums

Forum discussions were chunked using a thread-aware strategy.

- Original user questions were stored as individual chunks.
- Each forum reply was stored as a separate chunk.
- Very short replies were excluded.

This approach preserves the natural structure of troubleshooting conversations and support discussions.

### Chunking Results

| Source | Chunks |
|----------|----------:|
| Documentation | 58 |
| Blogs | 22 |
| Forums | 51 |
| Total | 131 |

---

## Embedding and Vector Storage

All chunks were embedded using the Sentence Transformers model:

`all-MiniLM-L6-v2`

The resulting embeddings were stored in a persistent ChromaDB vector database.

Each stored chunk includes:

- Chunk text
- Source type
- Document title
- Source URL
- Authority score

Authority scores were assigned to support source prioritization during retrieval:

| Source | Authority Score |
|----------|----------:|
| Documentation | 3 |
| Blog | 2 |
| Forum | 1 |

---

## Retrieval Strategy

User questions are embedded using the same embedding model used during ingestion.

The retrieval pipeline performs:

1. Query embedding generation
2. Vector similarity search in ChromaDB
3. Retrieval of top candidate chunks
4. Source-aware score adjustment using authority weights

Documentation sources receive the highest weighting because they represent official product information. Blog posts receive moderate weighting, while forum discussions receive lower weighting due to their community-generated nature.

This retrieval strategy helps prioritize authoritative information while still allowing practical troubleshooting content from community discussions to be surfaced when relevant.

## Reranking Strategy

A lightweight reranking layer was implemented after vector retrieval.

The reranker combines:

- Vector similarity
- Source authority weighting
- Query keyword overlap

This approach improves ranking quality while avoiding the computational cost of cross-encoder models.

## Retrieval Filtering

A minimum similarity threshold is applied before reranking.

Chunks below the threshold are discarded to reduce retrieval noise and prevent unrelated content from influencing generated answers.

## Answer Generation

Retrieved chunks are combined into a context window and supplied to a local large language model for answer generation.

Gemma 2 9B running through Ollama was selected as the generation model. The model receives the user's question together with the highest-ranked retrieved chunks.

The prompt instructs the model to:

* Answer using only retrieved context
* Avoid introducing unsupported information
* Acknowledge when sufficient information is unavailable
* Prefer higher-authority sources when multiple sources are retrieved

This grounding approach reduces hallucinations and ensures that responses remain tied to the collected OpenEMR knowledge base.

---

## Query Logging

A logging mechanism was implemented to record system activity and support evaluation.

For each query, the system stores:

* Timestamp
* User question
* Generated answer
* Sources used during retrieval

Logs are stored in JSONL format, allowing efficient append-only storage and future analysis of retrieval behavior and source utilization.

Logging provides transparency into system decisions and supports debugging and performance evaluation.

---

## Contradiction Handling

Information retrieved from documentation, blogs, and community forums may occasionally contain conflicting guidance.

To address this challenge, the system incorporates source authority ranking. Documentation sources are assigned the highest authority score, followed by blogs and forum discussions.

When multiple source types are retrieved, the answer generation process prioritizes information from higher-authority sources. The system also provides a source-priority notice indicating that source authority was considered during answer generation.

This approach provides a practical mechanism for handling contradictions while maintaining transparency regarding how conflicting information is resolved.

---

## End-to-End Retrieval-Augmented Generation Pipeline

The complete system consists of the following stages:

1. Multi-source data collection
2. PDF processing and normalization
3. Semantic chunking
4. Embedding generation
5. ChromaDB vector storage
6. Similarity-based retrieval
7. Source-aware reranking
8. Contradiction handling
9. Answer generation using Gemma 2
10. Query logging

The resulting pipeline allows users to submit technical support questions and receive grounded responses generated from documentation, blog posts, and community forum discussions.


## Current Dataset Statistics

| Metric               | Value |
| -------------------- | ----: |
| Documentation Pages  |     7 |
| PDF Manuals          |     2 |
| Blog Articles        |    10 |
| Forum Threads        |    15 |
| Total Chunks         |   131 |
| Documentation Chunks |    58 |
| Blog Chunks          |    22 |
| Forum Chunks         |    51 |

## Technologies Used

* Python
* Requests
* BeautifulSoup
* pypdf
* Sentence Transformers
* ChromaDB
* Ollama
* Gemma 2 9B
* JSON / JSONL
