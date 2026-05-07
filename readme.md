# 3GPP Support: AI Agent Skill for Standards Retrieval

本项目旨在构建一个专门用于查询 3GPP 协议（特别是 Rel-18）的 AI Agent Skill，使 AI 助手能够基于官方规格书提供权威、准确的技术解答。

## 1. 项目简介与工作原理

本项目通过两个核心 Python 脚本与 AI 的协作，实现了从“模糊查询”到“精准回复”的完整闭环：

1.  **精准定位 (Discovery)**：
    运行 `3gpp_spec_scope_spider.py` 自动化提取所有相关协议的摘要（Clause 1 Scope）。AI 通过分析这些摘要，能够精准锁定与用户疑问直接相关的规格书编号（如 TS 38.101-1），避免盲目搜索。
2.  **按需获取 (Retrieval)**：
    根据定位出的编号，调用 `download_3gpp_docs.py` 从官方镜像自动下载、解压并缓存对应的规格书正文。
3.  **智能合成 (Synthesis)**：
    AI 深度阅读下载的规格书原文，过滤冗余信息，最终输出基于协议事实的高质量回复，彻底解决 AI 在专业领域可能存在的“幻觉”问题。

---

## 2. 使用指南与示例

本节介绍如何直接使用项目工具进行协议检索，以及如何构建可部署的 AI Agent Skill。

### 2.1 协议发现工具 (Discovery Tool)
使用 `3gpp_spec_scope_spider.py` 获取协议系列的摘要信息，用于建立本地知识索引或提供给 AI 进行语义匹配。

*   **使用示例**：
    ```bash
    # 爬取 Rel-19（默认）38 系列协议的 Scope 摘要，并保存为 JSON
    python3 3gpp_spec_scope_spider.py --series 38 --output 38_series_scopes.json
    ```
*   **期待结果**：
    生成一个 `38_series_scopes.json` 文件。文件内容示例：
    ```json
    {
      "38.101-1": "The present document establishes the minimum RF characteristics and minimum performance requirements for NR User Equipment (UE)...",
      "38.211": "The present document describes the physical channels and modulation for NR..."
    }
    ```

### 2.2 协议获取工具 (Retrieval Tool)
使用 `download_3gpp_docs.py` 根据协议编号快速下载并解压文档正文。

*   **使用示例**：
    ```bash
    # 下载 TS 38.101-1 协议并解压到指定目录
    python3 download_3gpp_docs.py --spec 38.101-1 --output /tmp/rel-18
    ```
*   **期待结果**：
    在 `/tmp/rel-18` 目录下你会看到解压后的内容：
    - `38101-1-i00.zip` (原始包)
    - `38101-1-i00.docx` (协议正文)

### 2.3 构建 .skill 文件 (Packaging)
使用 `create_skill.sh` 脚本将代码、文档及指令封装，以便在 AI 平台中部署。

*   **使用示例**：
    ```bash
    # 智能打包：如果 SKILL.md 不存在则自动生成，存在则复用
    ./create_skill.sh
    
    # 强制重新生成：调用 Gemini 优化指令后打包
    ./create_skill.sh -g
    ```
*   **期待结果**：
    在当前目录下生成 `3gpp_support.skill` 文件。该文件可以直接导入支持 Skill 机制的 AI 客户端。

---

## 3. 技术实现细节

### 3.1 自动化指令优化 (Gemini 赋能)
`generate_SKILL-md.sh` 脚本利用 Gemini CLI 的强大处理能力，根据 `doc/prompt.txt` 预设的专家角色和约束条件，对 `doc/SKILL.md` 进行语义层面的润色和结构优化。这种“指令工程自动化”能显著提升 AI Agent 在实际执行任务时的遵从度和响应质量。

### 3.2 摘要自动化提取原理
`3gpp_spec_scope_spider.py` 采用轻量化解析方案，无需安装大型 Office 组件：
- **流式处理**：实时从 3GPP FTP 镜像获取最新协议包链接。
- **内存解压**：直接在内存中处理 `.zip` 和 `.docx`（XML），极大减少了磁盘 IO 和处理时间。
- **精准截取**：通过正则表达式在庞大的 XML 数据中快速定位 `1 Scope` 章节，确保提取的信息纯粹且高频。

---
*更多详细信息请参阅 `doc/` 目录下的各项脚本指南。*
