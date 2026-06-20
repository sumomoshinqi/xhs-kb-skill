# XHS KB Skill Interface

## Installation

Install by placing the `xhs-kb` folder under one of these directories:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R xhs-kb "${CODEX_HOME:-$HOME/.codex}/skills/"
```

The skill uses an external knowledge base data root. On this machine the default is:

```bash
~/Documents/Codex/2026-06-18/sous/outputs/xhs_codex_kb
```

On another machine, set:

```bash
export XHS_KB_ROOT="/path/to/xhs_codex_kb"
```

Or pass `--kb /path/to/xhs_codex_kb` to any command.

## Commands

### stats

Show coverage and chunk counts.

```bash
python3 scripts/xhs_kb.py stats
python3 scripts/xhs_kb.py stats --json
```

### search

Search chunks and return ranked snippets.

```bash
python3 scripts/xhs_kb.py search "小红书 标题公式 痛点 解决方案" -n 5
python3 scripts/xhs_kb.py search "薯条 聚光 蒲公英 达人合作" --category "2、营销种草师课件"
python3 scripts/xhs_kb.py search "28天 SOP 新品起盘" --json
```

### context

Create a compact evidence pack for drafting or diagnosis.

```bash
python3 scripts/xhs_kb.py context "油皮精华 种草笔记 标题 封面" -n 6 --chars 420
```

Use this before producing strategy or content. Read the strongest source files when the task needs precise structure.

### source

Read a source file by `kb_path`, source id, or fuzzy path/title match.

```bash
python3 scripts/xhs_kb.py source "documents/001-小红爆款笔记写作指南及商家经营手册.md" --head 3000
python3 scripts/xhs_kb.py source "小红爆款笔记写作指南及商家经营手册" --head 2000
```

## Natural-Language Usage

Example prompts:

- `用 $xhs-kb 给油皮精华写一篇小红书种草笔记，带标题、封面文案、正文和标签。`
- `用 $xhs-kb 诊断这篇小红书笔记为什么点击低，并给重写版。`
- `用 $xhs-kb 做一个新商家 14 天开店和内容种草计划。`
- `用 $xhs-kb 查薯条、聚光、蒲公英分别适合什么投放场景，并列证据。`

## Output Contract

For evidence-backed answers, include local evidence paths like:

```text
依据：
1. documents/001-小红爆款笔记写作指南及商家经营手册.md
2. extracted/010-2、营销种草师课件 小红书商业产品全景介绍.pdf.md
```

For direct content generation, cite evidence only when requested or when the answer is strategic/audit-like.
