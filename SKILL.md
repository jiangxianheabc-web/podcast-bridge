---
name: podcast-bridge
description: 一个让 AI Agent 订阅、转录、检索并理解全球播客的 Skill。支持添加和同步 RSS 订阅、获取播客单集、免费转录音频、生成章节与摘要、跨单集全文搜索，并将全文稿保存为本地 Markdown 或 Obsidian 知识库。适用于用户提供小宇宙单集链接、RSS 源、播客名称或单集编号，以及要求转录播客、总结单集、提取要点、检索话题、推荐播客、导入订阅、同步订阅或维护 RSS 源等场景。
---
---

# podcast-bridge

podcast-bridge 用于管理播客订阅、同步 RSS 单集元数据、转录播客、生成章节、搜索本地播客知识库，并基于全文稿生成摘要或笔记。

## 核心原则

根据用户请求选择最窄、最直接的工作流：

| 用户请求 | 执行动作 |
|---|---|
| 提供单集链接并要求全文稿 | 运行 `python transcribe.py "<url>" --chapters`，返回全文稿路径和基础统计。 |
| 提供单集链接并要求总结、要点或笔记 | 先转录，读取生成的全文稿，再在最终回复中写出用户要求的总结内容。 |
| 提供 RSS URL 或播客名称并要求添加 | 添加、同步或列出元数据；默认不要批量转录。 |
| 询问某个节目是否聊过某个话题 | 同步或查询本地库，并区分“全文命中”和“仅标题/简介命中”。 |
| 要求推荐播客 | 读取 `podcast-bridge-feeds/feeds/*.json`，按主题推荐；只有用户明确要求时才导入订阅。 |
| RSS 源损坏或订阅维护 | 使用 `podcast-bridge-feeds/resolve_feeds.py` 和 `podcast-bridge-feeds/import_feeds.py`。 |

重要边界：

- `transcribe.py` 是确定性的执行入口，负责转录、章节生成、RSS 入库和搜索。
- 摘要需要在读取全文稿之后由 Agent 自己生成；`--summary` 只是兼容旧参数和表达期望风格，不会稳定地产生摘要文件。
- 默认 ASR provider 使用 `bcut`，不需要 API Key。
- 查询当前状态时，应读取实时文件或 SQLite 数据库，不要依赖文档里的固定订阅数量。
- 如果用户要求摘要，最终回复必须包含摘要正文，不能只回复“转录完成”。

## 参考文件路由

只读取当前任务需要的参考文件：

- `references/transcription.md`：单集转录、启动前检查、ASR provider 选项、输出路径。
- `references/summarization.md`：brief、deep、product、investment、Obsidian 等摘要格式。
- `references/rss-workflows.md`：订阅管理、订阅库导入、RSS 同步/列表/搜索/转录。
- `references/troubleshooting.md`：常见失败、编码问题、API/provider 错误、状态查询。
- `references/project-layout.md`：仓库结构、数据文件、路径假设。

## 常用命令

在 podcast-bridge 项目根目录运行以下命令。`config.json` 中的 `library_dir` 会决定使用哪个本地播客库。

```bash
python transcribe.py --preflight-only "<episode-url>"
python transcribe.py "<episode-url>" --chapters
python transcribe.py rss subs
python transcribe.py rss sync "<podcast-name>" --limit 50
python transcribe.py rss list "<podcast-name>" --limit 50
python transcribe.py rss search "<podcast-name>" "<topic>" --days 90
python transcribe.py rss transcribe "<podcast-name>" <episode-id> --chapters
```

如果当前工作目录不在项目根目录，应使用 `transcribe.py` 的绝对路径。

维护内置订阅库：

```bash
cd podcast-bridge-feeds
python resolve_feeds.py bootstrap
python resolve_feeds.py add "Latent Space" --category ai --country us
python resolve_feeds.py validate feeds/
python import_feeds.py --all
```

## 交付要求

转录完成后，尽量报告生成的全文稿路径和基础统计信息，包括时长、分段数量、字数或字符数。

回答搜索类问题时，必须说明覆盖范围：有多少单集具备可搜索全文，有多少单集只有标题/简介元数据可搜索。
