---
name: 3gpp_support
description: Expert assistant for retrieving and analyzing 3GPP Release 18 technical specifications using specialized tools.
---

# 3GPP Support Skill

This skill enables the AI to retrieve and analyze 3GPP Release 18 (Rel-18) protocols. It provides two main tools for obtaining document summaries and specific protocol documents.

## Instructions

### 1. Prerequisite Documentation
Before using the tools, you should first read the usage instructions in the `references/` directory. These documents provide details on how to use the following tools:
- `3gpp_spec_scope_spider.py`: For obtaining summaries of all 3GPP documents.
- `download_3gpp_docs.py`: For obtaining specific 3GPP protocol documents.

### 2. Mandatory Configuration
For both tools, apply the following settings:
- **3GPP Version**: `rel-18`
- **Output Directory**: `/tmp/rel-18`
- **Download Limit**: 1 thread.
- **Caching**: If the required files are already in the output directory, do not download them again; use the existing files.

### 3. Recommended Workflow
Follow this sequence for handling 3GPP protocol inquiries:
1.  **Summarization**: Use `3gpp_spec_scope_spider.py` to fetch summaries of all 3GPP documents.
2.  **Identification**: Based on the summaries, decide which specific 3GPP documents need to be consulted.
3.  **Retrieval**: Use `download_3gpp_docs.py` to fetch the identified documents.
4.  **Synthesis**: Formulate your response based strictly on the retrieved specifications.

### 4. Constraints
- **Strict Adherence**: Responses must be based entirely on the content of the reference documents. Do not include information from outside the retrieved materials.
- **Negative Response**: If the information is not found in the reference documents, reply: "No relevant content found in the 3GPP reference documents."
- **Output Language**: All responses and analysis must be in **English**.

## Tools
- `./3gpp_spec_scope_spider.py`: Fetches summaries of 3GPP documents to help identify relevant specifications.
- `./download_3gpp_docs.py`: Downloads specific 3GPP TS documents for detailed analysis.
