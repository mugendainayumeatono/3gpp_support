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

## 2. 快速上手：构建 .skill 文件

项目提供了一套自动化工具，用于将代码、文档及指令封装成标准的 `.skill` 文件（基于 ZIP 格式），以便在支持的 AI 平台中快速部署。

### 2.1 打包 Skill
使用 `create_skill.sh` 脚本进行打包：
- **智能打包 (默认行为)**：
  ```bash
  ./create_skill.sh
  ```
  脚本会自动检测 `doc/SKILL.md` 是否存在：
  - 如果**不存在**：自动调用 `generate_SKILL-md.sh` 生成新文件。
  - 如果**已存在**：直接使用现有文件，不再重复生成。
- **强制重新生成并打包**：
  ```bash
  ./create_skill.sh -g
  # 或
  ./create_skill.sh --generate
  ```
  无论 `doc/SKILL.md` 是否存在，都会强制调用 Gemini 重新生成，并自动保留最多 2 个历史备份（`SKILL.md.1` 和 `SKILL.md.2`）。

### 2.2 自动化指令优化
`generate_SKILL-md.sh` 脚本依赖 Gemini CLI，它会读取 `doc/prompt.txt` 中的优化策略，通过 AI 自动更新 `doc/SKILL.md`，使其描述更符合 AI Agent 的理解偏好。

---

## 3. 技术实现细节

### 3.1 摘要自动化提取 (Scope Spider)
为了实现高效的协议定位，`3gpp_spec_scope_spider.py` 采用了以下技术路径：
- **在线发现**：实时获取 3GPP FTP 镜像 `latest` 路径下的最新链接。
- **内存解压**：在内存中直接解压 `.zip` 及其内部的 `.docx` 文件，提取 `word/document.xml` 原始内容。
- **正则匹配**：利用正则表达式精准定位 `1 Scope` 章节，剔除无关的元数据，仅保留核心功能描述。

### 3.2 文档获取方式
除了自动化脚本，本项目也保留了传统的批量获取方法作为补充：
- **Wget 命令行**：
  ```bash
  # 递归下载指定系列的最新文档
  wget -r -np -nH --cut-dirs=3 -A "*.zip" https://www.3gpp.org/ftp/Specs/latest/Rel-17/38_series/
  ```
- **第三方工具 (download_3gpp)**：
  ```bash
  pip install download_3gpp
  download_3gpp --rel 16 --series 23
  ```

---
*更多详细信息请参阅 `doc/` 目录下的各项脚本指南及 `doc/SKILL.md` 描述文件。*
