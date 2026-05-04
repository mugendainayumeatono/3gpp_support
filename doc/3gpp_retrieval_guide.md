# 3GPP 协议文档批量下载与摘要获取指南

本文档总结了获取 3GPP 协议规格书及其摘要的方法。

## 1. 文档结构与存储
- **组织形式**：按系列（Series）组织，如 38 系列 (5G NR), 23 系列 (Architecture)。
- **存储路径**：官方 FTP/HTTP 镜像 [https://www.3gpp.org/ftp/Specs/](https://www.3gpp.org/ftp/Specs/)。
- **文件格式**：通常为 `.zip` 包，内含 `.doc` 或 `.docx` 文件。

## 2. 批量下载方法

### 2.1 使用 Wget (命令行)
可以通过 `wget` 递归下载特定 Release 或系列的最新文档：
```bash
# 下载 Release 17 的 38 系列最新文档
wget -r -np -nH --cut-dirs=3 -A "*.zip" https://www.3gpp.org/ftp/Specs/latest/Rel-17/38_series/
```

### 2.2 使用 Python 工具
安装 `download_3gpp` 工具：
```bash
pip install download_3gpp
# 下载 Release 16 的 23 系列
download_3gpp --rel 16 --series 23
```

## 3. 摘要获取方法 (Clause 1 Scope 自动化提取)
当前项目已确定采用**直接解析协议文档正文**的方法来获取最准确的摘要（即 Clause 1 Scope）。

### 3.1 核心流程
1. **定位最新版本**：访问 3GPP 官方 FTP 的 `latest` 路径（如 `Rel-19/38_series`），获取所有协议的最新 `.zip` 包链接。
2. **内存解压与解析**：
   - 下载 `.zip` 包并在内存中解压出其中的 `.docx` 文档。
   - 进一步解压 `.docx`（本质为 ZIP 格式）以读取 `word/document.xml` 原始 XML 内容。
3. **文本精准匹配**：
   - 使用 `xml.etree.ElementTree` 遍历 XML 节点，提取段落文本。
   - 通过正则匹配定位 `1 Scope` 章节的起始位置，并截取到 `2 References` 章节之前的内容。
4. **结构化存储**：将提取到的 Spec ID 与对应的 Scope 文本保存为 JSON 格式。

### 3.2 工具说明
项目提供的 `3gpp_spec_scope_spider.py` 脚本实现了上述流程，支持多线程并发处理。

