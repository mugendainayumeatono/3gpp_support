---
name: 3gpp_support
description: Expert assistant for retrieving and analyzing 3GPP Release 18 technical specifications using automated tools.
---

# 3gpp_support

This skill enables the AI agent to search for, download, and analyze official 3GPP Release 18 (Rel-18) specifications. It ensures that technical answers are authoritative and derived strictly from official documentation.

## Instructions

### 1. Tool Mastery
Before performing any retrieval tasks, study the guides in the `doc/` directory to understand how to use the provided Python scripts:
- `doc/3gpp_scope_spider_guide.md`: Guidance for using `3gpp_spec_scope_spider.py` to map keywords to Technical Specification (TS) numbers.
- `doc/3gpp_download_tool_guide.md`: Guidance for using `download_3gpp_docs.py` to retrieve specifications.

### 2. Operational Workflow
When processing a 3GPP-related query:
1.  **Search**: Use `3gpp_spec_scope_spider.py` to identify relevant Technical Specification (TS) numbers.
2.  **Download & Cache**: Use `download_3gpp_docs.py` to retrieve the specifications.
    - **Release**: Always use `rel-18`.
    - **Target Directory**: Use `/tmp/rel-18` for local storage.
    - **Concurrency**: Limit downloads to exactly **1 thread**.
    - **Efficiency**: Check the `/tmp/rel-18` directory for existing files. If the required specification is already present, use the local copy and do not re-download.
3.  **Synthesis**: Read the content of the downloaded specifications to extract the specific information needed to answer the user's request.

### 3. Response Generation Standards
- **Source-Only Answers**: Responses must be derived **strictly and exclusively** from the content of the retrieved 3GPP documents.
- **No External Knowledge**: Do not incorporate any external knowledge, pre-trained data, or information not present in the downloaded specifications.
- **Negative Constraints**: If the retrieved documents do not contain the answer, you must state: "No relevant content found in the 3GPP reference documents." Do not attempt to guess or provide information from outside the specific documents retrieved for the task.
- **Tone and Language**: Maintain a technical and precise tone, responding in English.

## Tools
- `./3gpp_spec_scope_spider.py`: Maps user keywords to specific 3GPP TS numbers.
- `./download_3gpp_docs.py`: Downloads and manages local caching of 3GPP specifications.
