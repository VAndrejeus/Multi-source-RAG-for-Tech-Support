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