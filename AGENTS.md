# AGENTS.md

本文件为 Claude Code（claude.ai/code）及其他编码代理在本仓库工作时提供指引。

## 仓库概览

这是《Unix 痛恨者手册》（*The UNIX-HATERS Handbook*）的中文翻译项目，由 FreeBSD 中文社区（FreeBSD-Ask）译制，GitHub 仓库为 `FreeBSD-Ask/unix-haters`。基于 GitBook 格式，源内容为 Markdown 文件，由 GitBook 平台自动构建和部署，无需本地构建步骤。

* 原书：Simson L. Garfinkel、Daniel Weise、Steven Strassmann 编著，John Klossner 插图，IDG Books Worldwide, Inc. 1994 年出版，ISBN 978-1568842035。原书内容固定于 1994 年，**不存在上游同步问题**，不要"更新版本号"。
* **翻译权威源：仓库根目录的 `ugh.pdf`（360 页）**。逐句校对时以该 PDF 为唯一权威源；禁止以中文版已有翻译作为修改依据，避免错误沿袭。
* 术语翻译以根目录 **`shu-yu-biao.md`（术语表）** 为唯一权威依据（已加入 `SUMMARY.md` 目录）；本文件"编写规范"一节是快速参考，两者冲突时以术语表为准。
* README 中的说明（"附录部分不属于原书"）与本文件一致。

## 版本与流程

无需拉取上游仓库，全部校对与增补工作以 `ugh.pdf` 为准。

如需机器可检索的英文原文，运行 `python script/extract_ugh_pdf.py`（依赖 `pypdf`）生成 `en/` 目录下的分章纯文本。注意：

* `en/` 已加入 `.gitignore`，是本地工作文件，**不要提交**。
* 提取文本带有 `[pNN]` 页码标记，便于回到 PDF 定位。
* 提取文本存在排版伪影：断词连字符（如 `par-ticular`）、页眉页脚混入、脚注与正文混排、项目符号丢失等。它只作对照参考，**不要** 把提取文本直接粘贴进译文；引用原文时以 PDF 页面为准。

## 内容架构

### 核心文件

* **`SUMMARY.md`** — 全书唯一数据源，定义完整目录结构和导航树。GitBook 用它来生成侧边栏。**第一行 `# Table of contents` 绝对不能变更**，否则 GitBook 同步失效。
* **`mu-lu.md`** — 由 `mulu.yml` CI 工作流从 `SUMMARY.md` 自动复制生成，**不要手动编辑**。
* **`ugh.pdf`** — 原书 PDF，翻译与校对的唯一权威原文。
* **`script/`** — 校对辅助脚本（如 `extract_ugh_pdf.py`），临时脚本与日志也放在此目录；已被 `.gitignore` 忽略，仅本地使用。
* **`en/`** — 本地生成的分章英文参考文本（gitignored，可随时用脚本重建）。

### 目录结构

* 前置内容在根目录：`qian-yan.md`（前言，对应原书 Foreword，Donald A. Norman 撰）、`xu-yan.md`（序言，对应原书 Preface，三位编辑撰写）、`fan-xu-yan.md`（反序言，对应原书 Anti-Foreword，Dennis Ritchie 撰）。注意：中文"前言/序言"与英文 Foreword/Preface 的对应关系与常见习惯相反，翻译与校对时不要混淆。
* `shi-qing-hai-mei-zui-zao-jie-xia-lai-zhi-hui-geng-zao/` — 序言（Preface）的其余小节：我们是谁、Unix 痛恨者手册往事、贡献者与致谢、排版惯例、免责声明；其中"你并不孤单"（You are not alone）是"Unix 痛恨者手册往事"的 H2 小节，不是独立文件。
* 正文 16 章按四部分组织，每部分一个目录，命名 `di-X-bu-fen-<拼音 slug>/`；每章为独立 `.md` 文件，章号与英文原版 1:1 对应（Ch1–Ch16）。
* `fulu/` — 附录，**不属于原书**，是三篇外部文章的译文（详见"附录校对"一节）。
* `.gitbook/assets/` — GitBook 静态资源（章首插图等）。
* 原书书末的 Index（索引）不翻译。

### 标题管理（关键约束）

`sync-headers.yml` 工作流会在每次 push 时自动将 `SUMMARY.md` 中的标题同步到对应 `.md` 文件的 H1。**这意味着直接编辑 `.md` 文件的 `# 标题` 会被 CI 覆盖。** 修改章节标题时，只改 `SUMMARY.md` 中对应的 `* [标题](路径)` 条目即可。

## CI/CD 工作流

所有工作流位于 `.github/workflows/`：

| 工作流 | 触发条件 | 说明 |
| ------ | -------- | ---- |
| `sync-headers.yml` | push | 从 SUMMARY.md 同步一级标题到各 .md 文件 |
| `mulu.yml` | SUMMARY.md 变更时 push | 复制 SUMMARY.md → mu-lu.md |
| `Markdown-lint2-pr.yml` | pull_request | 对变更的 .md 文件运行 markdownlint |
| `bold-spacing.yml` | pull_request（*.md 变更） | 检查加粗标记两侧空格 |
| `markdown-lint2.yml` | workflow_dispatch | markdownlint 检查并自动修复，规则见 `.github/.markdownlint.json` |
| `md-padding.yml` | workflow_dispatch | 自动在 CJK 与英文/数字间添加空格 |
| `AutoCorrect.yml` | workflow_dispatch | AutoCorrect 空格与标点检查，配置见 `.autocorrectrc` |
| `links.yml` | 定时 + workflow_dispatch | lychee 死链检查，配置见 `.github/lychee.toml` |
| `file-name-check.yml` | push（*.md 变更） | 检查 SUMMARY.md 中引用的文件是否存在 |
| `check-images.yml` | `.gitbook/assets/**` 变更 + workflow_dispatch | 运行 `.github/scripts/check_images.py` 检查图片引用 |
| `create-pdf.yml` | workflow_dispatch | 使用 `FreeBSD-Ask/gitbook-pdf-export` 工具导出 PDF/EPUB 并发布 Release |

## 编写规范

### 格式

* **命令行前缀：** `#` 表示 root 权限，`$` 表示普通用户。不要使用 `sudo`。
* **提示块：** tip/important/note/warning/caution 使用 `>` 缩进引用，关键词 **加粗**。
* **代码块：** 书中大量出现 shell 会话、邮件头、新闻组帖子、配置文件等引文。无法判断语言时使用 ` ```sh ` 兜底，禁止使用 text 作为代码块标记，不窜改既有的代码块标记。
* **表格：** 一律居中。
* **禁止 HTML：** 本项目不支持任何 HTML 语法。
* **文件命名：** 使用拼音 slug，文件名中不得包含空格、中文字符或英文冒号 `:`，必须兼容 Windows 操作系统对文件名的要求。例外：`fulu/Reconsidered.md` 为历史遗留英文名，保留不改。
* **路径与 IP：** 全书正文中的路径（带 `/` 或 `\` 的，如 `/etc/motd`、`/usr/spool/uucp`）和 IP 地址一律使用 **加粗**，不使用反引号 `` ` `` 包裹；不要混合使用 `*` 和 `` ` ``（如 `*`path`*` 是错误的）。
* **命令、选项、参数：** 命令、选项、可调选项、可调参数等格式使用 `行间代码`（反引号）包裹。注意：不带选项和参数的裸命令，如 mv cp 等，一般不加反引号，不进行包裹。
* **转义字符：** 除非是命令、选项和参数，否则含转义字符 `\` 的元素一律使用 **加粗** 包裹整个元素，不在正文中直接使用转义字符。逐个手动修改，禁止批量替换。
* **避免滥用"已"字：** 如"XX 已新增"应改为"新增 XX"；"已修复"应改为"修复完成"。禁止机械替换。
* **禁止篡改：** 不要篡改软件版本号、用户名、邮箱、URL、IP 地址、带圈数字（如 ①②③ 等），确保其位置、数量和英语原文一致。书中引用的邮件头（From/Subject/Date 等）与命令输出属于"事实引文"，除翻译注释性文字外不得改动技术内容。
* **避免章节交叉引用：** 正文不要出现具体的章节交叉引用（如"参见第 5 章"），改用语义化链接。
* **代码块注释翻译：** 代码块（` ``` ` 围栏）内的英文注释必须翻译为中文（如 shell 注释 `# This is a comment` → `# 这是一个注释`）。只翻译注释部分，不修改实际命令或代码。保持代码结构和格式不变。
* **禁止「」引号：** 正文中不允许出现「」引号，一律替换为""（中文双引号）。禁止机械替换，需逐个手动修改。
* **引号必须成对且方向正确：** 正文使用中文弯引号，外层用""，引号内再用''；不得出现方向颠倒（如"text"收尾方向错误）、半边引号缺配、或直引号 " 与 ' 混入正文。代码块与行内代码内的引号保持原样，不改。
* **禁止双冒号链接语法：** 不允许使用 AsciiDoc 风格的双冒号链接语法（如 `xref:file[文本]`、`link:file[文本]`），必须使用标准 markdown 链接 `[文本](路径)` 指向真实位置。
* **禁止软换行：** 所有段落必须在同一行内完成，不得跨行拼接，不得使用行尾 `+` 等软换行标记。
* **加粗空格：** `**加粗**` 的第一个 `**` 前必须有且只有一个半角空格（行首、列表项标记后、引用块标记后属例外），第二个 `**` 后必须有且只有一个半角空格；加粗紧邻标点（如 `，`、`。`、`、`、`：`、`；`、`（`、`)`、`,`）或位于行尾时，该侧免加空格。此规则用于避免 GitBook 渲染加粗失效，由 `.github/scripts/check_bold_spacing.py` 检查。

### 术语与人名

* **术语译法以 `shu-yu-biao.md`（术语表）为准**，本节为快速参考；术语表未收录的按下述总则处理，并在 PR 中建议补录术语表。
* 书名统一译为《Unix 痛恨者手册》（原书名 *The UNIX-HATERS Handbook*，首次出现可附原文）。
* 人名保留英文原文（如 Ken Thompson、Dennis Ritchie、Richard Stallman、Donald Norman），不要音译。
* 命令、程序、系统与商标名保留英文：csh、sh、find、make、sendmail、rn、trn、NeWS、X11、NFS、TOPS-20、ITS、Multics、Lisp Machine 等。
* `Unix`、`UNIX` 的大小写保持原文写法，禁止机械统一。
* "拷贝" → "复制"，"壳/外壳" → "shell"。禁止机械替换。
* 第二人称叙述一律使用"你"而非"您"；直接引语（邮件、对话、章节标题中的引文）按说话语境处理（如第 12 章标题中的"您"）。
* 参考文献一章的条目按项目既定决策采用对应中译本信息（书名、出版社、ISBN）；没有中译本的条目保留英文原版信息，不要杜撰中译本。

### CJK 空格

中英文、中文与数字之间必须加半角空格。文件和命令名用 `` ` `` 括起来。`md-padding.yml` 和 `AutoCorrect.yml` 工作流会自动检测修复。

### 图片

在正文中插入图片，使用 markdown 格式引用 `.gitbook/assets/` 下的资源；`check-images.yml` 会校验引用与实际文件的一致性。

## 翻译校对工作流程（Claude Code）

对已翻译章节进行质量审校时，参考以下步骤：

1. **获取原文**：运行 `python script/extract_ugh_pdf.py` 生成 `en/` 分章文本（或用 pypdf 直接读取 `ugh.pdf` 对应页），以英文原文为基准逐句比对。拿不准时打开 `ugh.pdf` 对应页面核对版面与脚注。

2. **逐句对照**：将中文翻译与英文原文逐句比对，重点检查以下问题类别：

   | 问题类型 | 示例 |
   | -------- | ---- |
   | 事实性错误 | *CLU Reference Manual* 误译为《C 语言参考手册》 |
   | 漏译 | 英文原版有但中文缺失的句子或段落 |
   | 重复/串段 | 同一段落被误译两次，或相邻段落内容串行 |
   | 机翻腔/表达生硬 | "在阅读本章后，你将会收获" → "通过阅读本章，你将了解" |
   | 用词不当 | 原文的双关、俚语被译丢或译反 |
   | 引文失真 | 邮件、新闻组帖子等引文的意思与原文不符 |
   | 语法/文字错误 | 重复字词、"非常地"应为"非常" |
   | 欧化汉语、倒装句、后置句、偷换主语、不必要的被动句 | 自行联网制定标准，避免语法错误和非地道汉语表述 |

3. **提交修改**：
   * 基于 `main` 创建分支 `fix/<章节名或主题>`
   * 仅提交修改的 `.md` 文件，不要包含无关文件
   * 提交信息格式：`fix: 修正第 X 章翻译错误`（无章号的前置内容/附录写明篇名）
   * 用 `gh pr create` 创建 PR，目标分支为 `main`
   * PR 描述中列出每处修改及原因

4. **注意事项**：
   * 不要修改 `# 标题`——会被 `sync-headers.yml` CI 覆盖；标题改动只改 `SUMMARY.md`
   * 保持术语一致性，遵循本文"编写规范"
   * 补译漏译内容时，确保翻译风格与上下文一致
   * 禁止篡改带圈数字，如 ①②③ 等，确保其位置、数量和英语原文一致
   * 禁止篡改代码块（包括 shell 命令、邮件头、配置文件内容等），仅修改正文翻译
   * 禁止篡改用户名、邮箱、URL、IP 地址等技术参数
   * 以 `ugh.pdf` 为唯一权威源；禁止以中文版已有翻译作为修改依据，避免错误沿袭

5. **逐句校对递归工作流**（核心约束）：
   * **逐行逐句子** 遍历内容，检查逻辑一致性，联网复核后修改
   * **三轮 + 一轮复查**：完整执行三轮逐句校对，然后严格、完整地复查一轮；若仍有问题，继续执行三轮，递归直至无问题
   * **逐个修改**：修改时禁止机械修改、禁止批量；必须逐个手动修改，禁止使用软件工具批量替换或批量逐个复核
   * **修改前后复核**：每次修改前确认问题真实存在、修改后确认改动准确且未引入新错误
   * **不复查旧错**：不得复查以前已经完成三轮的错误；每轮查询内容必须是新的（若与之前的复查重复则跳过、不改，只看是否有新增内容）
   * **联网复查**：对于不存在的实际访问查询（如失效链接、书中提到的历史事实），需联网复查三次后修改
   * **禁止绕过审查**：不得以任何方式搜索、批量、绕过逐句子审查流程

## 附录校对（重要）

`fulu/` 三篇译文 **不属于原书 `ugh.pdf`**，是后来网络上的评论文章。校对时 **不能** 以 PDF 为源，必须联网检索原文网页，以检索到的原文为准：

| 文件 | 原文 | 作者与年份 |
| ---- | ---- | ---------- |
| `fulu/bingdu.md` | 《Unix 的流行病学》 | Philip E. Agre，1994 |
| `fulu/pinglun.md` | 评论《Unix 痛恨者手册》 | Andrew Kuchling，1997 |
| `fulu/Reconsidered.md` | 重新审视《Unix 痛恨者手册》 | Eric S. Raymond，2008 |

校对步骤：联网检索原文 → 逐句对照 → 逐个手动修改。检索不到原文的句子，按译文自身逻辑与事实核查处理，并联网复核三次后再改。

## Lint 配置

* **markdownlint**（`.github/.markdownlint.json`）：本地已安装 `markdownlint-cli2 v0.22.1`（基于 `markdownlint v0.40.0`），可在本地直接运行检查与修复
  * **本地运行命令**（在仓库根目录执行）：

    ```sh
    # 检查全部中文 .md（en/ 为 gitignored 的提取文本，自动跳过）
    markdownlint-cli2 "**/*.md" "!.github/**" "!.gitbook/**" "!node_modules/**" "!script/**" --config .github/.markdownlint.json

    # 自动修复可修复的问题（MD012 多余空行、MD047 末尾换行、MD034 裸 URL 等）
    markdownlint-cli2 "**/*.md" "!.github/**" "!.gitbook/**" "!node_modules/**" "!script/**" --config .github/.markdownlint.json --fix
    ```

  * **MD060 表格列风格规则（重要）**：配置为 `"style": "compact"` + `"aligned_delimiter": true`
    * **compact 风格**：管道符两侧各保留 **单个空格**，例如 `| cell1 | cell2 |`；空单元格写作 `| |`（不是 `||` 或 `|  |`）
    * **aligned_delimiter**：分隔行 `|---|` 的管道符位置必须与表头行的管道符位置对齐
    * **CJK 显示宽度**：markdownlint 按 **显示宽度** 计算列位置，**每个中文字符按 2 宽度** 计算（与英文 1 宽度不同）。因此含 CJK 的列宽 = CJK 字符数 × 2 + ASCII 字符数 × 1
    * **分隔行 dash 数量公式**：若某列内容显示宽度为 W，则分隔行该列总宽（含两侧空格）也应为 W，dash 数量 = W − 4（减去前后各 1 空格 + 前后各 1 冒号）。例如列内容 `FreeBSD 版本` 显示宽度 = 7+1+4 = 12，分隔行应为 ` :--------: `（8 个 dash）
    * **常见错误修复**：当 markdownlint 报 `MD060/table-column-style [Table pipe does not align with header for option "aligned_delimiter"]` 时，需手动扩展分隔行 dash 数量，使管道符位置与表头按显示宽度对齐；`--fix` 无法自动修复此类问题
  * **MD056 表格列数规则**：表头声明几列，所有数据行都必须有几列；末尾缺空单元格时需补 `| |`，而非省略管道符
* **lychee**（`.github/lychee.toml`）：6 线程、30 并发、30 秒超时、最多 3 次重试、Chrome UA、接受 200/402/403/418/429 状态码、排除私有 IP 与 localhost
* **加粗空格**（`.github/scripts/check_bold_spacing.py`）：检查 `**加粗**` 两侧空格，规则见“编写规范 · 格式”；PR 时由 `bold-spacing.yml` 自动执行
  * 本地检查：`python .github/scripts/check_bold_spacing.py`
  * 就地修复：`python .github/scripts/check_bold_spacing.py --fix`
