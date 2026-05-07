# 3GPP Support: AI Agent Skill for Standards Retrieval

本项目旨在构建一个专门用于查询 3GPP 协议（特别是 Rel-18）的 AI Agent Skill，使 AI 助手能够基于官方规格书提供权威、准确的技术解答。

## 1. 项目简介与工作原理

本项目通过两个核心 Python 脚本与 AI 的协作，实现了从“模糊查询”到“精准回复”的完整闭环：

1.  **精准定位 (Discovery)**：
    运行 `3gpp_spec_scope_spider.py` 自动化提取协议摘要（Clause 1 Scope）。AI 分析摘要后锁定相关规格书编号。
2.  **按需获取 (Retrieval)**：
    根据定位出的编号，调用 `download_3gpp_docs.py` 从官方镜像自动下载并解压对应的规格书正文。
3.  **智能合成 (Synthesis)**：
    AI 阅读规格书原文，过滤冗余信息，输出基于协议事实的回复，解决 AI 的“幻觉”问题。

---

## 2. 构建与部署：生成 .skill 文件

项目提供了一套自动化工具，用于将代码、文档及 AI 指令封装成标准的 `.skill` 文件（基于 ZIP 格式），以便在支持 Skill 机制的 AI 平台中快速部署。

### 2.1 打包方法
使用 `create_skill.sh` 脚本进行打包：

*   **智能打包 (推荐/默认)**：
    ```bash
    # 逻辑：SKILL.md 不存在则自动生成；存在则直接使用
    ./create_skill.sh
    ```
*   **强制重新生成**：
    ```bash
    # 逻辑：无论是否存在，均调用 Gemini 优化指令后重新生成 SKILL.md
    ./create_skill.sh -g
    ```

### 2.2 期待结果
运行成功后，你会在当前目录下看到：
- **`3gpp_support.skill`**：最终的 Skill 压缩包，可直接导入 AI 客户端。
- **`doc/SKILL.md.[1/2]`** (可选)：在使用 `-g` 标志时生成的历史版本备份。

---

## 3. 工具使用指南：Python 脚本调用

如果你希望直接在本地命令行环境中使用相关工具，可以参考以下操作示例。

### 3.1 协议发现示例 (Scope Spider)
用于批量获取协议系列的摘要，建立本地索引。
- **命令**：
  ```bash
  python3 3gpp_spec_scope_spider.py --series 38 --output 38_series.json
  ```
- **输出**：生成包含 Spec 编号及其 Scope 文本的 JSON 文件。

### 3.2 协议获取示例 (Download Tool)
用于精准下载特定协议的 docx 正文。
- **命令**：
  ```bash
  python3 download_3gpp_docs.py --spec 38.101-1 --output /tmp/rel-18
  ```
- **输出**：在目标目录下获取解压后的协议 `.docx` 文件。

---

## 4. 技术实现细节

### 4.1 3GPP 文档结构与存储
- **组织形式**：按系列（Series）组织，如 38 系列 (5G NR), 23 系列 (Architecture)。
- **存储路径**：官方 FTP/HTTP 镜像 [https://www.3gpp.org/ftp/Specs/](https://www.3gpp.org/ftp/Specs/)。
- **文件格式**：通常为 `.zip` 包，内含 `.doc` 或 `.docx` 文件。

### 4.2 本地协议获取工具实现方法 (download_3gpp_docs.py)
本项目采用自研的 Python 脚本实现协议的精准获取与处理，其核心方法如下：
1.  **动态链接定位**：利用 `urllib.request` 获取 3GPP FTP 镜像的 HTML 索引，通过正则表达式 (`re`) 实时解析出符合特定 Release 和 Series 要求的最新 `.zip` 下载地址。
2.  **多线程并发下载**：使用 `ThreadPoolExecutor` 构建线程池（默认 8 线程），通过并发执行提高大批量协议包的下载效率。
3.  **内存级解压与转存**：下载的二进制流直接进入 `io.BytesIO` 缓冲区，利用 `zipfile` 模块在内存中完成解压，随后将提取出的 `.docx` 文件持久化到本地缓存目录。
4.  **DOCX 结构化解析 (可选)**：
    - 进一步解压 `.docx` 以读取其底层的 `word/document.xml`。
    - 使用 `xml.etree.ElementTree` 遍历 XML 节点，通过样式属性（w:pStyle）和正则编号匹配（Heading Heuristics）识别章节标题。
    - 将非结构化的文档内容按章节标题（Title）和段落（Content）拆分，最终导出为易于 AI 索引的 JSON 格式。

### 4.3 摘要自动化提取核心流程 (Spider 实现)
1.  **定位最新版本**：访问 3GPP 官方 FTP 的 `latest` 路径（如 `Rel-19/38_series`），获取所有协议的最新 `.zip` 包链接。
2.  **内存解压与解析**：
    - 下载 `.zip` 包并在内存中解压出其中的 `.docx` 文档。
    - 进一步解压 `.docx`（本质为 ZIP 格式）以读取 `word/document.xml` 原始 XML 内容。
3.  **文本精准匹配**：
    - 使用 `xml.etree.ElementTree` 遍历 XML 节点，提取段落文本。
    - 通过正则匹配定位 `1 Scope` 章节的起始位置，并截取到 `2 References` 章节之前的内容。
4.  **结构化存储**：将提取到的 Spec ID 与对应的 Scope 文本保存为 JSON 格式。

### 4.4 AI Agent Skill 打包与管理
本项目提供了一套用于构建和管理 AI Agent Skill 的自动化脚本，其核心在于将静态的代码与动态生成的指令（SKILL.md）相结合。
- **create_skill.sh**：负责创建标准目录结构，将核心脚本与 Markdown 指南归档并封装。
- **自动化指令优化**：通过 `generate_SKILL-md.sh` 调用 Gemini CLI 润色 `SKILL.md`，显著提升 AI Agent 的遵从度。
- **智能备份机制**：在重新生成 `SKILL.md` 时，自动保留最多 2 个历史版本以便快速回退。

---
*更多详细信息请参阅 `doc/` 目录下的各项脚本指南。*
