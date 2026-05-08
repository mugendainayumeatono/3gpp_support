---
name: 3gpp_support
description: Expert assistant for retrieving and analyzing 3GPP Release 18 technical specifications using specialized tools.
---

# 3GPP Support Skill

This skill enables the AI to retrieve and analyze 3GPP Release 18 (Rel-18) protocols. It provides two main tools for obtaining document summaries and specific protocol documents.

## Instructions

### 1. Mandatory Configuration
For both tools, always apply the following settings:
- **3GPP Version**: `rel-18` (or `18` depending on the tool's parameter requirements).
- **Output Directory**: `/tmp/rel-18`
- **Download Limit**: 1 thread (use `-t 1`).
- **Caching**: If the required files are already in the output directory, do not download them again; use the existing files.

### 2. Recommended Workflow
Follow this sequence for handling 3GPP protocol inquiries:
1.  **Summarization**: Use `3gpp_spec_scope_spider.py` to fetch summaries of 3GPP documents. This helps build a map of the protocol landscape.
2.  **Identification**: Based on the summaries, identify the specific 3GPP documents (Spec IDs) relevant to the user's query.
3.  **Retrieval**: Use `download_3gpp_docs.py` to fetch and structure the identified documents into JSON format.
4.  **Analysis**: Search the generated JSON files for keywords and specific sections.
5.  **Synthesis**: Formulate a response based strictly on the retrieved specifications, citing the section titles.

### 3. Constraints
- **Strict Adherence**: Responses must be based entirely on the content of the reference documents. Do not include information from outside the retrieved materials.
- **Negative Response**: If the information is not found in the reference documents, reply: "No relevant content found in the 3GPP reference documents."
- **Language**: All analysis and responses must be in **English**.

## Tool Documentation

### 1. 3GPP Protocol Scope Extraction Tool (3gpp_spec_scope_spider.py)

`3gpp_spec_scope_spider.py` is a high-performance automation tool designed to batch extract "Clause 1: Scope" from 3GPP 38-series (5G NR) protocol documents. It allows for quick construction of a protocol overview map for an entire Release.

#### Core Functions
- **Auto-detection**: Automatically discovers the latest released version on the 3GPP website if not specified.
- **Deep Parsing**: Handles 3GPP's "nested compression" format (.zip containing .docx).
- **Precise Extraction**: Uses regex and XML traversal to accurately capture content from the start of "1 Scope" to "2 References".
- **Full Automation**: One-click retrieval, download, memory decompression, XML parsing, and JSON report generation.
- **Lightweight Reporting**: Generates a summary JSON containing Spec IDs and their Scope descriptions.

#### Command Line Arguments

| Argument | Shorthand | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--release` | `-r` | No | Specify Release version. Auto-detects if omitted. | `18`, `17`, `Rel-19` |
| `--threads` | `-t` | No | Number of concurrent threads (Default: 1). | `16` |
| `--output` | `-o` | No | Directory or file path for the JSON report. | `./reports/` |

#### Usage Examples
- **Get summaries for Release 18**:
  ```bash
  python3 3gpp_spec_scope_spider.py -r 18 -t 1 -o /tmp/rel-18
  ```

#### AI Usage Tips
1. **Initialize Index**: Run the spider to get scopes for the target release.
2. **Semantic Search**: Match keywords in the `scope` field to determine which Spec ID contains the answer.
3. **Deep Dive**: After identifying the Spec ID, use `download_3gpp_docs.py` for full analysis.

---

### 2. 3GPP Document Download and Structuring Tool (download_3gpp_docs.py)

`download_3gpp_docs.py` is designed to automatically retrieve, download, decompress, and structure 5G/4G protocol documents (.docx) from the 3GPP FTP server.

#### Core Functions
- **Automated Retrieval**: Finds the latest download links based on Release and Series.
- **Precise Download**: Supports downloading entire series or specific Spec IDs.
- **In-memory Decompression**: Processes .zip files in memory to reduce I/O.
- **Structured Conversion**: Optionally converts .docx to structured JSON for easier searching.
- **Auto-cleanup**: Deletes redundant .docx files after JSON conversion.

#### Command Line Arguments

| Argument | Shorthand | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--rel` | `-r` | Yes | 3GPP Release version number. | `18`, `17` |
| `--series` | `-s` | Yes | Protocol series number. | `38` (5G NR), `23` (Architecture) |
| `--specs` | (None) | No | Specific Spec IDs (space separated). | `38.331 38.211` |
| `--json` | (None) | No | Enable JSON conversion and delete docx. | (Switch) |
| `--output` | `-o` | No | Output directory. | `/tmp/rel-18` |
| `--threads` | `-t` | No | Concurrent threads (Default: 8). | `1` |

#### Usage Examples
- **Download and structure specific Rel-18 protocol (38.331)**:
  ```bash
  python3 download_3gpp_docs.py -r 18 -s 38 --specs 38.331 --json -o /tmp/rel-18 -t 1
  ```

#### Output JSON Structure
When using `--json`, the generated file follows this format:
```json
[
  {
    "title": "1 Scope",
    "content": "Description of the scope..."
  },
  {
    "title": "5.2.2.3 Acquisition of System Information",
    "content": "Specific section text..."
  }
]
```

#### AI Usage Tips
1. **Fetch Document**: Use the tool with `--json` to get a structured version of the required spec.
2. **Read JSON**: Parse the resulting `.json` file.
3. **Search & Cite**: Search the `content` fields and use the `title` for accurate citations.
