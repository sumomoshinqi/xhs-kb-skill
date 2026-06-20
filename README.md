# xhs-kb

`xhs-kb` 是一个 Codex skill，用来检索并使用本地小红书/XHS 运营知识库。

这个仓库已经包含：

- Codex skill：`xhs-kb/`
- 完整知识库数据：`xhs_codex_kb/`
- 可直接运行的检索 CLI：`xhs-kb/scripts/xhs_kb.py`

clone 后可以直接配置到 Codex 使用，不需要再单独导入飞书资料。

## 适用场景

这个 skill 适合处理这些需求：

- 小红书种草笔记生成：标题、封面文案、正文、标签、评论区引导
- 小红书笔记诊断与改写：点击低、转化弱、标题/封面/正文结构问题
- 小红书账号运营 SOP：起号、选题、素材库、发布时间、互动涨粉
- 商家增长：开店、商品种草、达人合作、直播、私域承接
- 投放与合作：薯条、聚光、蒲公英、达人合作场景判断
- 区域运营 SOP：28 天流程、新品起盘、每日工作流

## 仓库结构

```text
.
├── README.md
├── xhs-kb/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── references/
│   │   └── interface.md
│   └── scripts/
│       └── xhs_kb.py
└── xhs_codex_kb/
    ├── README.md
    ├── KNOWLEDGE_MAP.md
    ├── VALIDATION.md
    ├── documents/
    ├── extracted/
    ├── files/
    │   └── originals/
    ├── index/
    │   ├── catalog.json
    │   ├── chunks.jsonl
    │   ├── TREE.md
    │   └── search_kb.py
    └── raw/
```

## 知识库规模

当前内置知识库包含：

- source：902 个
- 在线文档：34 份
- 附件：868 份，原件保留在 `xhs_codex_kb/files/originals/`
- 可全文检索 source：898 个
- 检索 chunks：10121 条
- 4 个附件只保留元数据或无正文可抽取

## 快速开始

```bash
git clone https://github.com/sumomoshinqi/xhs-kb-skill.git
cd xhs-kb-skill
git lfs install
git lfs pull

python3 xhs-kb/scripts/xhs_kb.py stats
python3 xhs-kb/scripts/xhs_kb.py search "小红书 标题公式 痛点 解决方案" -n 5
```

脚本会自动优先读取仓库内的 `./xhs_codex_kb`，所以在 repo 根目录运行时不需要设置环境变量。

仓库使用 Git LFS 保存原始附件和大索引文件。正常 `git clone` 会自动拉取 LFS 文件；如果本地只拿到了 pointer 文件，执行 `git lfs pull`。

## 安装到 Codex

把 skill 目录复制到 Codex skills 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R xhs-kb "${CODEX_HOME:-$HOME/.codex}/skills/"
```

如果你希望 Codex 在任意目录都能找到这份知识库，设置 `XHS_KB_ROOT`：

```bash
export XHS_KB_ROOT="$(pwd)/xhs_codex_kb"
```

也可以把这行写入 shell 配置文件，例如 `~/.zshrc`：

```bash
echo "export XHS_KB_ROOT=\"$(pwd)/xhs_codex_kb\"" >> ~/.zshrc
```

## 在 Codex 中调用

自然语言示例：

```text
用 $xhs-kb 给油皮精华写一篇小红书种草笔记，带标题、封面文案、正文和标签。
用 $xhs-kb 诊断这篇小红书笔记为什么点击低，并给重写版。
用 $xhs-kb 做一个新商家 14 天开店和内容种草计划。
用 $xhs-kb 查薯条、聚光、蒲公英分别适合什么投放场景，并列证据。
```

做策略、诊断、报告类输出时，建议要求 Codex 列出本地证据路径。

## CLI 接口

### 1. 查看统计

```bash
python3 xhs-kb/scripts/xhs_kb.py stats
python3 xhs-kb/scripts/xhs_kb.py stats --json
```

### 2. 检索知识库

```bash
python3 xhs-kb/scripts/xhs_kb.py search "小红书 标题公式 痛点 解决方案" -n 5
python3 xhs-kb/scripts/xhs_kb.py search "薯条 聚光 蒲公英 达人合作" --category "2、营销种草师课件"
```

### 3. 生成证据包

```bash
python3 xhs-kb/scripts/xhs_kb.py context "油皮精华 种草笔记 标题 封面" -n 6 --chars 420
```

### 4. 打开原始文本

```bash
python3 xhs-kb/scripts/xhs_kb.py source "documents/001-小红爆款笔记写作指南及商家经营手册.md" --head 3000
python3 xhs-kb/scripts/xhs_kb.py source "小红爆款笔记写作指南及商家经营手册" --head 2000
```

### 5. 指定其他知识库路径

```bash
python3 xhs-kb/scripts/xhs_kb.py --kb /path/to/xhs_codex_kb stats
```

## 验证

验证 skill 结构：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py xhs-kb
```

验证知识库可读：

```bash
python3 xhs-kb/scripts/xhs_kb.py stats
python3 xhs-kb/scripts/xhs_kb.py search "标题公式 痛点 解决方案" -n 3
python3 xhs-kb/scripts/xhs_kb.py context "商家 开店 薯条 聚光 蒲公英" -n 3
```

## 数据来源与边界

- 知识库来自飞书 Wiki 的本地导出与索引。
- 仓库内已经包含原始附件、抽取后的 Markdown、索引、目录和校验记录。
- 原始附件和 `chunks.jsonl` 使用 Git LFS 管理，clone 后需要确保 LFS 文件已拉取。
- PDF 抽取依赖文本层；扫描图像页可能没有可检索正文。
- 4 个附件只保留元数据或无正文可抽取，原件仍保留在 `xhs_codex_kb/files/originals/`。
- 不要声称已读取没有抽出正文的附件全文。
