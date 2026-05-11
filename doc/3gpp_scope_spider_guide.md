# 3GPP 协议范围提取工具 (3gpp_spec_scope_spider.py) 使用指南

`3gpp_spec_scope_spider.py` 是一个高性能的自动化爬虫工具，专门用于批量提取 3GPP 38 系列（5G NR）协议文档中的 **第 1 章：范围 (Clause 1: Scope)** 内容。它能够快速构建整个 Release 的协议概要地图。

## 1. 核心功能
*   **版本自动探测**：默认自动发现 3GPP 官网已发布的最新 Release（如 Rel-19）。
*   **断点续传/增量更新**：自动读取已存在的 JSON 报告，跳过已成功处理的 Spec，支持在现有报告基础上进行增量补充。
*   **深度递归解析**：支持处理 3GPP 特有的“嵌套压缩”格式（`.zip` 包内含 `.docx`，而 `.docx` 本身也是压缩格式）。
*   **精准章节切片**：利用正则表达式和 XML 遍历，精确截取 `1 Scope` 开始到 `2 References` 之前的所有正文。
*   **全自动化流程**：一键完成“检索 -> 下载 -> 内存解压 -> XML 解析 -> 章节提取 -> JSON 汇总”。
*   **轻量化报告**：生成一份包含所有 Spec ID 及其 Scope 描述的汇总 JSON，无需存储庞大的原始文档。

## 2. 命令行参数说明

| 参数 | 缩写 | 强制 | 说明 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| `--release` | `-r` | 否 | 指定 Release 版本。不指定则自动探测最新版 | `18`, `17`, `Rel-19` |
| `--threads` | `-t` | 否 | 并发处理线程数 (默认 1，建议 16-32) | `32` |
| `--output` | `-o` | 否 | 指定生成的 JSON 报告保存的目录或文件路径 | `./my_reports/` 或 `./report.json` |

## 3. 使用示例

### 示例 A：自动获取最新 Release 的全系列概要
这是最常用的命令，工具会自动找到最新版本（如 Rel-19），并提取所有 38 系列协议的 Scope。
```bash
python3 3gpp_spec_scope_spider.py -t 32
```

### 示例 B：提取指定版本 (Release 18) 的协议概要并保存到指定目录
```bash
python3 3gpp_spec_scope_spider.py -r 18 -t 16 -o ./rel18_data/
```

### 示例 C：静默运行并生成报告
由于该脚本主要输出进度条和状态，可以直接运行并查看最终生成的 JSON。
```bash
python3 3gpp_spec_scope_spider.py -r 17 -t 20
```

## 4. 输出结果说明

**数据结构示例：**
```json
[
    {
        "spec": "38.331",
        "scope": "The present document specifies the Radio Resource Control protocol for the radio interface between UE and NG-RAN...",
        "status": "success"
    },
    {
        "spec": "38.211",
        "scope": "The present document describes the physical channels and signals for 5G NR...",
        "status": "success"
    }
]
```

## 5. AI 使用提示 (Prompt Helper)
如果你是 AI Agent，可以利用此工具快速构建知识库索引：
1.  **初始化索引**：运行 `python3 3gpp_spec_scope_spider.py -r 18 -t 32`。
2.  **语义检索**：在输出结果中,通过匹配 `scope` 中的关键词，确定用户的问题应该去哪份具体协议中寻找答案。
3.  **按需深挖**：在确定了 Spec ID（如 38.300）后，再调用 `download_3gpp_docs.py` 下载完整文档进行深入分析。
