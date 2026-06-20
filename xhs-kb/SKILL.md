---
name: xhs-kb
description: Search and use the local Xiaohongshu/XHS knowledge base built from the Feishu Wiki on 小红书爆款笔记、商家增长、运营 SOP、标题封面正文、薯条/聚光/蒲公英、开店与投放资料. Use when the user asks for 小红书/XHS content drafting, note rewriting, account or post diagnosis, merchant operation plans, local/郑州 SOP, or evidence-backed answers from this local knowledge base.
---

# XHS Knowledge Base

Use this skill to retrieve evidence from the local Xiaohongshu knowledge base before drafting, diagnosing, or planning.

## Data Root

Resolve the knowledge base root in this order:

1. User-provided `--kb <path>`
2. `XHS_KB_ROOT`
3. Default local root: `~/Documents/Codex/2026-06-18/sous/outputs/xhs_codex_kb`

The root must contain `index/catalog.json`, `index/chunks.jsonl`, `documents/`, and `extracted/`.

## Required Workflow

1. Run `scripts/xhs_kb.py search "<query>"` or `scripts/xhs_kb.py context "<query>"` before answering substantive XHS questions.
2. Open the strongest source files with `scripts/xhs_kb.py source "<kb_path>"` when exact wording or structure matters.
3. Use the retrieved sources to decide the answer shape:
   - Drafting note: title candidates, cover copy, body, tags, comment prompt, publishing notes.
   - Rewriting note: diagnose hook, audience, pain point, proof, structure, tags, then rewrite.
   - Account/post diagnosis: check positioning, audience, topic, cover, title, body, tags, timing, interaction, paid amplification.
   - Merchant growth: separate opening setup, product seeding, content, creator collaboration, ad tools, live/private-domain handoff.
4. Cite local evidence paths in the answer when the user asks for evidence, reports, strategy, or audit output.
5. Do not claim to have read sources whose `extracted_text` is false; say that only metadata/original files are available.

## CLI Interface

Use Python 3 with the bundled script:

```bash
python3 /Users/sumomoshinqi/.codex/skills/xhs-kb/scripts/xhs_kb.py stats
python3 /Users/sumomoshinqi/.codex/skills/xhs-kb/scripts/xhs_kb.py search "小红书 标题公式 痛点 解决方案" -n 5
python3 /Users/sumomoshinqi/.codex/skills/xhs-kb/scripts/xhs_kb.py context "油皮精华 种草笔记 标题 封面" -n 6
python3 /Users/sumomoshinqi/.codex/skills/xhs-kb/scripts/xhs_kb.py source "documents/001-小红爆款笔记写作指南及商家经营手册.md" --head 3000
```

For complete arguments and install notes, read `references/interface.md`.

## Retrieval Hints

- Titles/covers/body: search `标题公式 痛点 解决方案 封面 正文 互动`.
- Merchant/opening: search `商家 开店 日常运营 商品 种草`.
- Ads/collaboration: search `薯条 聚光 蒲公英 达人 合作`.
- Local SOP: search `郑州帮 28天 SOP 新品起盘`.
- Copy examples: search `爆款文案 标题 情绪 钩子`.

## Quality Boundary

The current local bundle has 902 sources, 898 searchable text sources, and 10121 chunks. Four attachments only have metadata/original files, because three PDFs have no extractable text and one source is a `.lnk` shortcut.
