# 3GPP 协议文档下载与结构化工具 (download_3gpp_docs.py) 使用指南

`download_3gpp_docs.py` 是一个专为 3GPP 协议工程师和开发者设计的工具，用于从 3GPP 官方 FTP 服务器自动获取、下载、解压并结构化 5G/4G 协议文档（.docx 格式）。

## 1. 核心功能
*   **自动化检索**：根据 Release（版本）和 Series（系列）自动在 3GPP 官网检索最新的下载链接。
*   **精准下载**：支持下载整个系列，或通过 Spec ID 精确匹配特定协议。
*   **智能跳过 (Skip-if-exists)**：在下载前自动检查目标目录。如果最终生成的文件（`.json` 或 `.docx`）已存在，则跳过下载与处理，节省带宽。
*   **内存解压**：直接在内存中处理 .zip 包，减少磁盘 I/O。
*   **结构化转换**：可选将 .docx 文档转换为结构化的 JSON 格式，便于程序读取和搜索。
*   **自动清理**：在转换为 JSON 后自动删除冗余的 .docx 文件。
*   **多线程加速**：默认开启 8 线程并发处理。

## 2. 命令行参数说明

| 参数 | 缩写 | 强制 | 说明 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| `--rel` | `-r` | 是 | 3GPP Release 版本号 | `18`, `17`, `16` |
| `--series` | `-s` | 是 | 协议系列号 | `38` (5G NR), `23` (Architecture) |
| `--specs` | (无) | 否 | 指定具体的 Spec ID (空格分隔) | `38.331 38.211` |
| `--json` | (无) | 否 | 开启 JSON 结构化转换并删除 docx | (开关) |
| `--output` | `-o` | 否 | 指定输出目录 (默认为系统临时目录) | `./downloads` |
| `--threads` | `-t` | 否 | 并发下载线程数 (默认 8) | `16` |

## 3. 使用示例

### 示例 A：下载 Release 18 的整个 38 系列文档
下载所有 5G NR 相关的最新协议到当前目录下的 `nr_docs` 文件夹。
```bash
python3 download_3gpp_docs.py -r 18 -s 38 -o ./nr_docs
```

### 示例 B：下载并结构化特定的协议 (38.331)
下载并直接转换为 JSON 格式，方便进行文本分析。转换完成后，原始 .docx 将被删除。
```bash
python3 download_3gpp_docs.py -r 18 -s 38 --specs 38.331 --json -o ./json_data
```

### 示例 C：批量下载多个特定的 Release 17 协议
```bash
python3 download_3gpp_docs.py -r 17 -s 38 --specs 38.331 38.211 38.213 -o ./rel17_core
```

### 示例 D：高并发结构化下载 23 系列 (核心网)
针对核心网大量文档，增加线程数以加快处理速度。
```bash
python3 download_3gpp_docs.py -r 16 -s 23 --json -t 16 -o ./rel16_core_json
```

## 4. 输出 JSON 结构说明
当使用 `--json` 参数时，生成的 `.json` 文件结构如下：
```json
[
  {
    "title": "Pre-amble",
    "content": "文档前言内容..."
  },
  {
    "title": "1 Scope",
    "content": "本协议的适用范围描述..."
  },
  {
    "title": "5.2.2.3 Acquisition of System Information",
    "content": "具体的小节正文内容..."
  }
]
```

## 5. AI 使用提示 (Prompt Helper)
如果你是 AI Agent，可以参考以下逻辑使用此工具：
1. **查找范围**：当用户询问某项技术,在 Rel-18 中的定义时。
2. **第一步**：执行 `python3 download_3gpp_docs.py -r 18 -s 38 --specs 38.331 --json`。
3. **第二步**：读取生成的 `.json` 文件。
4. **第三步**：在 `content` 字段中搜索关键词。
5. **第四步**：根据 JSON 中的 `title`（章节名）和`content`（内容）为用户提供带出处的准确回答。
