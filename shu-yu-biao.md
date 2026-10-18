# 术语表

本表是全书术语译法的唯一权威依据（对照 `AGENTS.md`"编写规范"使用）。翻译与校对时**先查本表**；表未收录的术语按 `AGENTS.md` 的总则处理，并在 PR 描述中建议补录。修订本表时须同步排查全书既有译文，保持一致。

## 总则

* 人名：书中作者、黑客、技术人物**保留英文**，不音译（如 Ken Thompson、Dennis Ritchie、Richard P. Gabriel）；大众文化名人按通用中文译名（如伍迪·艾伦、迈克尔·乔丹）。
* 命令、程序、协议、文件格式：一律保留英文（如 csh、find、sendmail、TCP/IP）。
* 公司与机构：正文叙述用中文通名（惠普、微软、苹果、贝尔实验室、麻省理工学院）；无通行译名或并列厂商清单中保留英文原文（DEC、IBM、Apollo、Symbolics、Data General、SCO、AT&T）。
* `Unix`、`UNIX` 等大小写写法保持原文，禁止机械统一。

## 书名与核心概念

| 英文原文 | 统一译法 | 说明 |
| -------- | -------- | ---- |
| The UNIX-HATERS Handbook | 《Unix 痛恨者手册》 | 书名；首次出现可附原文 |
| UNIX-HATERS（邮件列表） | Unix 痛恨者 | 正文叙述用中文名；邮件头 `To:`/`From:` 等引文内保留原文 |
| Worse Is Better | "宁拙勿巧" | 亦作 worse-is-better；书末后记《"宁拙勿巧"的崛起》 |
| The Right Thing | "正确之道" | 亦作 the right thing |
| New Jersey approach | 新泽西方法 | |
| MIT approach | MIT 方法 | |
| Gulag | 古拉格 | 首次出现可注"劳改营" |
| information utility | 信息公用设施 | Multics 立项目标 |
| Multics | Multics | 全称 MULTiplexed Information and Computer System（多路复用信息与计算系统） |

## 人名

| 英文原文 | 统一译法 | 说明 |
| -------- | -------- | ---- |
| Ken Thompson / Dennis Ritchie / Brian Kernighan | 保留英文 | |
| Richard Stallman / Richard M. Stallman | 保留英文 | |
| Richard P. Gabriel | 保留英文 | 不译作"加布里埃尔" |
| Donald A. Norman | 保留英文 | |
| Michael Travers / John Rose / Olin Shivers | 保留英文 | 同一文件内写法一致 |
| Woody Allen | 伍迪·艾伦 | 大众名人音译 |
| Michael Jordan | 迈克尔·乔丹 | 大众名人音译 |

## 机构与公司

| 英文原文 | 统一译法 | 说明 |
| -------- | -------- | ---- |
| AT&T | AT&T | 叙述中首次出现可写"美国电话电报公司（AT&T）" |
| Bell Labs | 贝尔实验室 | |
| MIT | 麻省理工学院 | 缩写 MIT 可保留；同一文件内一致 |
| Xerox PARC | 施乐帕洛阿尔托研究中心（Xerox PARC） | |
| FSF | 自由软件基金会（FSF） | |
| HP | 惠普 | 厂商并列清单中可保留 HP |
| Microsoft | 微软 | 厂商并列清单中可保留 Microsoft |
| Apple | 苹果 | |
| Sun Microsystems | Sun | 首次出现可写全称 |
| Open Software Foundation | 开放软件基金会 | |

## 系统、硬件与产品

| 英文原文 | 统一译法 | 说明 |
| -------- | -------- | ---- |
| Lisp Machine | Lisp 机 | 昵称 LispM 保留英文 |
| ITS | ITS | 全称 Incompatible Timesharing System（不兼容分时系统），首次出现注出 |
| TOPS-20 / TWENEX / Multics / Dorado / Cedar/Mesa / Apollo Domain | 保留英文 | |
| X-Windows / X Window System / X11 | 按原文 | X-Windows 连字符与复数是作者刻意为之，不得改写 |
| Motif / NeWS / NEXTSTEP / OpenStep / Dylan / SimCity | 保留英文 | |
| PDP-7 / PDP-11 / VAX / GE645 / Macintosh / NeXTstation | 保留英文 | |
| Andromeda Strain | 《天外来菌》 | 小说名 |
| Lord of the Rings | 《魔戒》 | |
| Bored of the Rings | 保留英文 | 无通行中译本 |

## 软件与命令

| 英文原文 | 统一译法 | 说明 |
| -------- | -------- | ---- |
| csh / sh / find / grep / make / ps / strip / free / man / catman | 保留英文 | 可加反引号 |
| Emacs / vi | 保留英文 | |
| sendmail / uuencode / rn / trn / routed / finger | 保留英文 | |
| Space Travel | 太空旅行 | 游戏名 |
| Space War | 星际大战 | 游戏名；与 Space Travel 的写法差异按原文保留 |

## 技术术语

| 英文原文 | 统一译法 | 说明 |
| -------- | -------- | ---- |
| core dump | 核心转储 | |
| swap space | 交换空间 | |
| kernel panic | 内核恐慌 | 动词用法译"发生内核恐慌" |
| typeahead | 预键入 | 键盘预输入 |
| teletype | 电传打字机 | |
| hierarchical file system | 分层文件系统 | |
| graft vs. host disease | 移植物抗宿主病 | 移植医学隐喻 |
| rite of passage | 成长的必经之路 | 语境义 |
| flame | 论战、骂战 | 语境义 |
| lossage | 损失 | 黑客俚语，语境义 |
| fix（毒品隐喻） | 过瘾、解瘾 | 区别于"修复" |
| weenie | 弱鸡 | 对 Unix 迷的贬称（Unix weenies → Unix 弱鸡们） |
| guru | 导师 | Unix guru（语境：资深 Unix 专家） |
| idiot light | 警示灯 | 汽车仪表盘指示灯 |
| workstation | 工作站 | |
