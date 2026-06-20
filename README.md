# xhs-kb

Codex skill for searching and using a local Xiaohongshu/XHS operations knowledge base.

This repository contains the **skill code and deployment instructions only**. It does not include the underlying 1GB knowledge base export, Feishu originals, extracted documents, or indexed chunks.

## What This Skill Does

`xhs-kb` helps Codex retrieve evidence from a local 小红书 knowledge base before drafting, rewriting, diagnosing, or planning.

It is designed for tasks such as:

- 小红书种草笔记生成：标题、封面文案、正文、标签、评论区引导
- 笔记诊断与改写：点击低、转化弱、标题/封面/正文结构问题
- 账号运营 SOP：起号、选题、素材库、发布时间、互动涨粉
- 商家增长：开店、商品种草、达人合作、直播、私域承接
- 投放与合作：薯条、聚光、蒲公英、达人合作场景判断
- 本地/郑州运营 SOP：28 天流程、新品起盘、每日工作流

## Repository Layout

```text
.
├── README.md
└── xhs-kb/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   └── interface.md
    └── scripts/
        └── xhs_kb.py
```

## Data Requirement

The skill expects an external knowledge base directory with this shape:

```text
xhs_codex_kb/
├── index/
│   ├── catalog.json
│   └── chunks.jsonl
├── documents/
├── extracted/
└── files/
```

The current source bundle contains:

- 902 total sources
- 898 searchable text sources
- 10121 chunks
- 4 metadata-only items where text could not be extracted

## Install

Clone the repo and copy the skill folder into Codex's skill directory:

```bash
git clone <repo-url>
cd xhs-kb-skill
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R xhs-kb "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Then point the skill to the local knowledge base:

```bash
export XHS_KB_ROOT="/path/to/xhs_codex_kb"
```

On the original machine, the default path is:

```bash
~/Documents/Codex/2026-06-18/sous/outputs/xhs_codex_kb
```

If the data lives there, `XHS_KB_ROOT` is optional.

## Use In Codex

Invoke the skill naturally:

```text
用 $xhs-kb 给油皮精华写一篇小红书种草笔记，带标题、封面文案、正文和标签。
用 $xhs-kb 诊断这篇小红书笔记为什么点击低，并给重写版。
用 $xhs-kb 做一个新商家 14 天开店和内容种草计划。
用 $xhs-kb 查薯条、聚光、蒲公英分别适合什么投放场景，并列证据。
```

For strategic or audit-style answers, ask Codex to include local evidence paths.

## CLI Interface

The bundled CLI can also be used directly.

### Stats

```bash
python3 ~/.codex/skills/xhs-kb/scripts/xhs_kb.py stats
python3 ~/.codex/skills/xhs-kb/scripts/xhs_kb.py stats --json
```

### Search

```bash
python3 ~/.codex/skills/xhs-kb/scripts/xhs_kb.py search "小红书 标题公式 痛点 解决方案" -n 5
python3 ~/.codex/skills/xhs-kb/scripts/xhs_kb.py search "薯条 聚光 蒲公英 达人合作" --category "2、营销种草师课件"
```

### Evidence Pack

```bash
python3 ~/.codex/skills/xhs-kb/scripts/xhs_kb.py context "油皮精华 种草笔记 标题 封面" -n 6 --chars 420
```

### Source Inspection

```bash
python3 ~/.codex/skills/xhs-kb/scripts/xhs_kb.py source "documents/001-小红爆款笔记写作指南及商家经营手册.md" --head 3000
python3 ~/.codex/skills/xhs-kb/scripts/xhs_kb.py source "小红爆款笔记写作指南及商家经营手册" --head 2000
```

Any command can override the data root:

```bash
python3 ~/.codex/skills/xhs-kb/scripts/xhs_kb.py --kb /path/to/xhs_codex_kb stats
```

## Validate

Validate the skill folder with Codex's skill validator:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/xhs-kb
```

Smoke-test the data connection:

```bash
python3 ~/.codex/skills/xhs-kb/scripts/xhs_kb.py stats
python3 ~/.codex/skills/xhs-kb/scripts/xhs_kb.py search "标题公式 痛点 解决方案" -n 3
```

## Deployment Notes

- Keep the knowledge base data outside Git unless you intentionally prepare a separate, access-controlled data artifact.
- Use `XHS_KB_ROOT` for different machines or refreshed exports.
- The skill cites local `kb_path` values such as `documents/...` and `extracted/...`; these paths are relative to the configured knowledge base root.
- The skill must not claim to read metadata-only attachments as full text.

