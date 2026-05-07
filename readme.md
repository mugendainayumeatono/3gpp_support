# 3GPP Support: AI Agent Skill for Standards Retrieval

本项目旨在构建一个专门用于查询 3GPP 协议（特别是 Rel-18）的 AI Agent Skill，使 AI 助手能够基于官方规格书提供权威、准确的技术解答。

## 1. 项目简介与工作原理

本项目通过两个核心 Python 脚本与 AI 的协作，实现了从“模糊查询”到“精准回复”的完整闭环：

1.  **精准定位 (Discovery)**：
    运行 `3gpp_spec_scope_spider.py` 自动化提取协议摘要（Clause 1 Scope）。AI 分析摘要后锁定相关规格书编号。
2.  **按需获取 (Retrieval)**：
    调用 `download_3gpp_docs.py` 从官方镜像自动下载并解压对应的规格书正文。
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

### 4.1 自动化指令优化 (Gemini 赋能)
`generate_SKILL-md.sh` 脚本利用 Gemini CLI，根据 `doc/prompt.txt` 预设的专家角色，对 `doc/SKILL.md` 进行语义层面的结构优化。这种“自动化指令工程”显著提升了 AI Agent 执行任务时的遵从度。

### 4.2 摘要自动化提取原理
`3gpp_spec_scope_spider.py` 采用轻量化解析方案：
- **流式处理**：实时从 3GPP FTP 镜像获取最新协议链接。
- **内存解压**：直接在内存中处理 `.zip` 和 `.docx`（XML），极大减少了磁盘 IO 损耗。
- **精准截取**：通过正则表达式在 XML 中快速定位 `1 Scope` 章节，确保信息的纯粹性。

---
*更多详细信息请参阅 `doc/` 目录下的各项脚本指南。*
