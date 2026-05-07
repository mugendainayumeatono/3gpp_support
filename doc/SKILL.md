---
name: 3gpp_support
description: Expert assistant for retrieving and analyzing 3GPP Release 18 (rel-18) technical specifications. Use this skill when you need to discover, download, or search 3GPP standards documentation using automated tools.
---

# 3gpp_support

This skill provides tools and workflows for interacting with official 3GPP Release 18 (rel-18) specifications.

## Instructions

### 1. Tool Mastery
Before executing any tasks, review the guides in `references/` to understand the usage of the bundled scripts:
- `3gpp_spec_scope_spider_guide.md`: Guide for `scripts/3gpp_spec_scope_spider.py` (spec discovery).
- `3gpp_download_tool_guide.md`: Guide for `scripts/download_3gpp_docs.py` (document retrieval).

### 2. Operational Parameters
Always adhere to these constraints when using the scripts:
- **Target Release**: rel-18
- **Local Cache**: `/tmp/rel-18`
- **Persistence**: Check `/tmp/rel-18` for existing files before initiating a download.
- **Concurrency**: Limit downloads to **exactly 1 thread**.

### 3. Response Protocol
- **Source Integrity**: Base all answers **exclusively** on the content of retrieved 3GPP documents.
- **No Hallucinations**: Do not supplement responses with external knowledge, assumptions, or data from other releases.
- **Negative Response**: If the requested information is not present in the retrieved specifications, respond with: "No relevant content found in the 3GPP reference documents."

## Bundled Scripts
- `scripts/3gpp_spec_scope_spider.py`: Maps functional requirements to 3GPP specification numbers.
- `scripts/download_3gpp_docs.py`: Downloads and extracts 3GPP specification files to the local cache.
