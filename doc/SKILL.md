---
name: 3gpp_support
description: Expert assistant for retrieving and analyzing 3GPP Release 18 technical specifications using automated tools.
---

# 3gpp_support

This skill provides the capability to retrieve, download, and analyze official 3GPP Release 18 (Rel-18) technical specifications to answer technical queries with high authority and zero hallucination.

## Instructions

### 1. Tool Mastery
Before executing any retrieval tasks, you must familiarize yourself with the operation of the bundled Python scripts by reading their respective guides:
- `doc/3gpp_scope_spider_guide.md`: Guidance for keyword-to-TS mapping using `3gpp_spec_scope_spider.py`.
- `doc/3gpp_download_tool_guide.md`: Guidance for specification downloading using `download_3gpp_docs.py`.

### 2. Operational Workflow
When tasked with answering a 3GPP-related question:
1.  **Search**: Use `3gpp_spec_scope_spider.py` to identify relevant Technical Specification (TS) numbers based on the user's query.
2.  **Download & Cache**: Use `download_3gpp_docs.py` to retrieve the identified specifications.
    - **Release**: Always use `rel-18`.
    - **Target Directory**: Always use `/tmp/rel-18`.
    - **Concurrency**: Set to `1` thread for reliability.
    - **Efficiency**: Check `/tmp/rel-18` for existing files. If the required specification is already present, use the local copy and do not re-download.
3.  **Synthesize**: Read the content of the downloaded documents to extract the specific information needed to answer the user's request.

### 3. Response Generation Standards
- **Document-Centricity**: Answers must be derived **strictly and exclusively** from the content of the retrieved 3GPP documents.
- **No External Knowledge**: Do not incorporate any external knowledge, pre-trained data, or information not present in the downloaded specifications.
- **Negative Constraints**: If the retrieved documents do not contain the answer, you must state: "No relevant content found in the 3GPP reference documents." Do not attempt to guess or provide information from outside the specific documents retrieved for the task.
- **Clarity and Precision**: Maintain a technical and precise tone, responding in English.

## Bundled Tools
- `./3gpp_spec_scope_spider.py`: Maps user keywords to specific 3GPP TS numbers.
- `./download_3gpp_docs.py`: Downloads and manages local caching of 3GPP specifications.
