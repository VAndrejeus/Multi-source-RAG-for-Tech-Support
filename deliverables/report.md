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