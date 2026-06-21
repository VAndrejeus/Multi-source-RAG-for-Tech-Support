# Multi-Source RAG for Tech Support

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for OpenEMR technical support.

The system combines information from multiple knowledge sources, including official documentation, technical blog posts, and community forum discussions. User questions are answered using retrieved source material and a locally hosted large language model.

The goal of the project is to improve technical support question answering by combining authoritative documentation with community knowledge while handling source prioritization and potential contradictions.

---

## Features

* Multi-source knowledge collection
* Documentation scraping from OpenEMR Wiki
* Blog collection from OpenEMR technical articles
* Forum collection from OpenEMR community discussions
* PDF documentation processing
* Semantic chunking using sentence embeddings
* Vector search with ChromaDB
* Source-aware retrieval and reranking
* Similarity filtering
* Contradiction handling through source authority ranking
* Grounded answer generation using Gemma 2 9B
* Query and source logging

---

## Data Sources

### Documentation

Documentation was collected from the OpenEMR Wiki and selected to cover common technical support topics.

Collected documentation pages:

* OpenEMR Wiki Home Page
* Installation Guides
* Upgrade Guides
* OpenEMR 7.0.0 Users Guide
* OpenEMR 7.0.4 API Documentation
* Patient Portal
* Securing OpenEMR

**Total Documentation Pages:** 7

### PDF Documentation

Additional documentation was collected from OpenEMR PDF manuals.

PDFs processed:

* OpenEMR 3.1 Users Guide
* OpenEMR 4.1 Users Guide

**Total PDF Manuals:** 2

### Blog Articles

Technical blog articles were collected from the OpenEMR website.

Topics include:

* Product releases
* ONC certification
* Telehealth integration
* Community partnerships
* Development workflows
* Healthcare interoperability

**Total Blog Articles:** 10

### Community Forums

Community discussions were collected from the OpenEMR Discourse forum using the Discourse JSON API.

Topics include:

* Technical support requests
* Configuration issues
* Troubleshooting discussions
* User workflow concerns
* Feature requests
* Development topics

**Total Forum Threads:** 15

---

## System Architecture

```text
User Question
       │
       ▼
Query Embedding
       │
       ▼
ChromaDB Retrieval
       │
       ▼
Similarity Filtering
       │
       ▼
Source-Aware Reranking
       │
       ▼
Contradiction Handling
       │
       ▼
Gemma 2 9B Answer Generation
       │
       ▼
Source Logging
       │
       ▼
Final Response
```

---

## Data Preparation Pipeline

Before the RAG system can answer questions, source data must be collected, processed, chunked, and indexed.

### Step 1: Collect Documentation

```bash
python scripts/scrape_documentation.py
```

This script collects official OpenEMR documentation from the OpenEMR Wiki.

Output:

```text
data_sources/documentation/
```

Documentation Pages Collected: **7**

---

### Step 2: Collect Blog Articles

```bash
python scripts/scrape_blogs.py
```

This script collects OpenEMR technical blog articles.

Output:

```text
data_sources/blogs/
```

Blog Articles Collected: **10**

---

### Step 3: Collect Community Forum Discussions

```bash
python scripts/scrape_forums.py
```

This script retrieves OpenEMR community discussions using the Discourse JSON API.

Output:

```text
data_sources/forums/
```

Forum Threads Collected: **15**

---

### Step 4: Process PDF Documentation

```bash
python scripts/process_pdfs.py
```

This script extracts text from OpenEMR PDF manuals and converts them into the same structured format used by the other documentation sources.

PDFs Processed:

* OpenEMR 3.1 Users Guide
* OpenEMR 4.1 Users Guide

PDF Manuals Processed: **2**

---

### Step 5: Semantic Chunking

```bash
python scripts/chunking.py
```

Documents are divided into semantically meaningful chunks using Sentence Transformers (`all-MiniLM-L6-v2`).

Instead of splitting documents using fixed-size chunks, semantic similarity between neighboring paragraphs is used to determine chunk boundaries.

Chunking Results:

| Source        | Chunks |
| ------------- | -----: |
| Documentation |     58 |
| Blogs         |     22 |
| Forums        |     51 |
| Total         |    131 |

Output:

```text
data_sources/processed/
```

---

### Step 6: Vector Database Ingestion

```bash
python scripts/ingest.py
```

All chunks are embedded using the Sentence Transformers model `all-MiniLM-L6-v2` and stored in ChromaDB.

Stored metadata includes:

* Source type
* Document title
* Source URL
* Chunk text

Chunks Indexed: **131**

Output:

```text
chroma_db/
```

---

### Step 7: Run the RAG System

```bash
python scripts/rag.py
```

The RAG application:

1. Converts the user question into an embedding
2. Retrieves relevant chunks from ChromaDB
3. Filters low-similarity results
4. Applies source-aware reranking
5. Handles source prioritization
6. Generates a grounded answer using Gemma 2 9B running locally through Ollama
7. Logs query activity

Example question:

```text
How do I enable the patient portal?
```

Generated output includes:

* Answer
* Sources Used
* Source Priority Information
* Query Log Entry

---

## Retrieval Pipeline

The retrieval pipeline performs:

1. Query embedding generation
2. Vector similarity search
3. Similarity filtering
4. Source-aware reranking
5. Context construction
6. LLM answer generation

To prevent context-window overflow, retrieved chunks are truncated before being sent to the language model. This ensures sufficient space remains for answer generation.
---

## Source Authority Ranking

To improve answer reliability, source-specific weighting bonuses are applied during reranking.

| Source | Reranking Bonus |
|---------|---------:|
| Documentation | 0.15 |
| Blog | 0.08 |
| Forum | 0.03 |

These values are intentionally small so that semantic similarity remains the primary ranking signal while still favoring more authoritative sources.

---

## Contradiction Handling

Information retrieved from documentation, blogs, and forums may occasionally contain conflicting guidance.

The system handles potential contradictions through source-aware reranking and source prioritization. Documentation receives the highest weighting, followed by blogs and forums.

When multiple source types contribute to an answer, the system informs the user that source prioritization was applied.

---

## Query Logging

Each query is logged to support evaluation and debugging.

Logged information includes:

* Timestamp
* User question
* Generated answer
* Sources used

Logs are stored in JSONL format.

---

## Dataset Statistics

| Metric               | Value |
| -------------------- | ----: |
| Documentation Pages  |     7 |
| PDF Manuals          |     2 |
| Blog Articles        |    10 |
| Forum Threads        |    15 |
| Documentation Chunks |    58 |
| Blog Chunks          |    22 |
| Forum Chunks         |    51 |
| Total Chunks         |   131 |

---

## Results

The final knowledge base contains:

| Source | Count |
|----------|----------:|
| Documentation Pages | 7 |
| PDF Manuals | 2 |
| Blog Articles | 10 |
| Forum Threads | 15 |
| Total Chunks | 131 |

The system successfully retrieves information from multiple source types and generates grounded answers using Gemma 2 9B. Retrieved sources are displayed alongside generated answers to improve transparency and traceability.

---

## Technologies Used

* Python
* Requests
* BeautifulSoup
* pypdf
* Sentence Transformers
* ChromaDB
* Ollama
* Gemma 2 9B
* JSON
* JSONL

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd "Multi-source RAG for Tech Support"
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the System

For a new setup:

```bash
python scripts/scrape_documentation.py
python scripts/scrape_blogs.py
python scripts/scrape_forums.py
python scripts/process_pdfs.py
python scripts/chunking.py
python scripts/ingest.py
python scripts/rag.py
```

Once the vector database has been created, only the following command is required:

```bash
python scripts/rag.py
```
## Evaluation

Example queries and system responses can be found in:

- deliverables/example_queries.md
- deliverables/performance_analysis.md

## Project Structure

```text
Multi-source RAG for Tech Support/
│
├── data_sources/
│   ├── documentation/
│   ├── blogs/
│   ├── forums/
│   └── processed/
│
├── chroma_db/
│
├── scripts/
│   ├── scrape_documentation.py
│   ├── scrape_blogs.py
│   ├── scrape_forums.py
│   ├── process_pdfs.py
│   ├── chunking.py
│   ├── ingest.py
│   ├── retrieval.py
│   ├── rag.py
│   ├── logger.py
│   └── contradiction_handler.py
│
├── logs/
├── deliverables/
├── requirements.txt
└── README.md
```

---

## Limitations

- Limited to collected OpenEMR sources
- Retrieval quality depends on source coverage
- Contradiction handling uses source authority ranking
