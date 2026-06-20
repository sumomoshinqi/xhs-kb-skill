# xhs-kb

`xhs-kb` 是一个 Codex skill，用来检索并使用本地小红书运营知识库。

这个仓库已经包含：

- Codex skill：`xhs-kb/`
- 完整知识库数据：`xhs_codex_kb/`
- 可直接运行的检索 CLI：`xhs-kb/scripts/xhs_kb.py`

## 适用场景

这个 skill 适合把本地知识库转成可执行的小红书内容、运营和增长方案。常见用例包括：

### 1. 内容创作

- 种草笔记生成：按产品、人群、场景和痛点生成标题、封面文案、正文、标签、评论区引导。
- 探店/打卡笔记：把现场照片、位置、价格、体验和避坑点整理成可发布笔记。
- 测评笔记：围绕产品质地、使用前后、对比、适用人群和真实体验组织内容。
- 干货笔记：把课程、方法论、清单和 SOP 转成收藏型内容。
- 情绪/故事型笔记：把个人经历、反差、槽点、惊喜感写成更有点击欲的开头和标题。

### 2. 笔记诊断与改写

- 点击低诊断：检查标题、封面、首图、关键词、场景冲突和用户点击理由。
- 互动低诊断：检查正文结构、情绪钩子、提问方式、评论引导和收藏价值。
- 转化弱诊断：检查卖点表达、证据链、使用场景、购买理由和信任感。
- 笔记重写：基于原笔记保留事实，重写标题、封面文案、正文、标签和发布注意事项。
- 旧内容翻新：把已有笔记改成热点版、搜索版、干货版、种草版或强转化版。

### 3. 账号运营

- 起号规划：确定账号定位、人设、内容栏目、选题池和前 7/14/28 天发布节奏。
- 选题规划：按目标人群、搜索词、痛点、热点和转化目标生成选题库。
- 内容 SOP：拆分从选题、素材、封面、标题、正文、标签到发布复盘的流程。
- 数据复盘：根据曝光、点击、互动、收藏、评论和转化表现判断下一步优化方向。
- 账号诊断：检查主页包装、昵称、简介、合集、置顶笔记和内容一致性。

### 4. 商家与产品增长

- 新商家开店：整理开店准备、基础装修、商品页、内容种草和日常运营动作。
- 新品起盘：围绕卖点提炼、竞品拆解、种草内容、达人合作和投放节奏出方案。
- 商品种草：把产品卖点转成用户视角的使用场景、痛点解决和证据表达。
- 直播承接：规划直播预热笔记、直播间福利、组件引导和复盘优化。
- 私域承接：设计从笔记评论、私信、店铺、直播到私域转化的链路。

### 5. 投放与合作

- 薯条投放：判断适合加热的笔记、投放目标和优化方向。
- 聚光投放：拆分搜索/信息流场景、关键词、人群和素材策略。
- 蒲公英合作：筛选达人类型、沟通话术、内容 brief 和投后复盘指标。
- 达人合作复盘：判断内容质量、互动效果、转化线索和后续放大方式。
- 广告素材诊断：检查封面、标题、利益点、证据和落地链路是否一致。

### 6. 知识库检索与报告

- 快速查资料：检索标题公式、封面公式、平台工具、商家运营资料和课程内容。
- 生成证据包：为策略、诊断或报告输出本地来源路径，方便复查。
- 主题报告：整理某个主题下的资料摘要，例如封面标题、达人合作、商家开店、内容 SOP。
- 竞品/案例拆解：按内容结构、卖点、封面、标题、评论和转化路径拆解案例。
- 批量素材整理：从知识库中抽取标签、标题模板、评论引导和内容框架。

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
用 $xhs-kb 把这张探店照片改成一篇更容易点击的小红书笔记。
用 $xhs-kb 为一个新防晒产品做 30 条选题，按搜索型、痛点型、测评型分类。
用 $xhs-kb 拆解这篇笔记互动低的原因，并给标题、封面、正文三版优化方案。
用 $xhs-kb 设计一套达人合作 brief，包含人群、卖点、内容方向和验收指标。
用 $xhs-kb 根据本地知识库整理一份“小红书封面标题优化”报告，并列本地证据路径。
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
