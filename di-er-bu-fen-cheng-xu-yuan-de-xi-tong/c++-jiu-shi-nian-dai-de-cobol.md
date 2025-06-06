# C++ 九十年代的 COBOL

![](../.gitbook/assets/cplus.png)

>问：“C”和“C++”这两个名字来源于哪里？
>
>答：它们是成绩。
>
>——Jerry Leichter

或许，Unix 的哲学——永远不让用户觉得任何事情是容易的——必然导致了 C++ 这种语言的出现。

面向对象编程的理念最早可以追溯到 60 年代的 Simula，70 年代初期则通过 Smalltalk 达到巅峰。其他书籍会告诉你，使用几十种面向对象的语言能让程序员更加高效，代码更健壮，并减少维护成本。但别指望在 C++ 中看到这些优点。

因为 C++ 完全误解了面向对象编程的真正意义。C++ 没有简化事情，反而创下了复杂性的新纪录。就像 Unix 一样，C++ 并不是经过精心设计的，它是一个错误不断累积、一个又一个荒谬的决定逐步显现的产物。它就像是庞大的后知后觉的烂摊子。

C++ 没有语法规则（几乎所有其他语言都有），所以你甚至无法知道某行代码是否合法。将 C++ 与 COBOL 做比较，是对 COBOL 的不公平，后者实际上在其时代的技术条件下，实在是一项了不起的工程成就。C++ 唯一令人称奇的地方是，居然有人能在它上面完成工作。幸运的是，大多数优秀的程序员知道，通过主要使用 C 语言并避开 C++ 中大多数荒唐的功能，他们可以避免 C++。通常，这意味着他们得自己编写一些非面向对象的工具，以获得他们所需要的功能。当然，这意味着他们的代码将是特立独行、不兼容的，且不可能理解或重用。但偶尔在代码中加点 C++ 的薄外壳，足以让经理们误以为他们的项目是值得批准的。

那些现在迫切想摆脱 COBOL 遗留代码中混乱、不易读、拼凑的烂摊子的公司，将会受到不小的冲击。那些已经转向 C++ 的公司，才刚刚开始意识到，C++ 并没有带来预期的回报。当然，已经为时已晚，未来几十年软件灾难的种子已经种下，并且得到充分的滋养。

## 面向对象编程的汇编语言

C++ 并不属于高级语言。为了理解这一点，让我们来看一下真正高级语言的特点：

* **优雅性**：高级语言的符号与所表达的概念之间有简单、容易理解的关系。
* **抽象性**：每个表达式都描述一个且只有一个概念。概念可以独立地描述，也可以自由组合。
* **表达能力**：使用高级语言，可以直截了当地表达程序行为的任何精确且完整的描述。

高级语言让程序员能够以与问题本身相适应的方式表达解决方案。高级程序通常更易于维护，因为它们的意图很清晰。从一段高级源代码中，现代编译器能够生成非常高效的代码，适应各种平台，因此高级代码天生具有高度的可移植性和可重用性。

相比之下，低级语言则要求关注大量与机器内部操作相关的细节，而这些细节与实际问题解决无关。这不仅使代码难以理解，还导致了过时问题的产生。随着新系统的出现，几乎每年都会有新的系统问世，低级代码变得过时，必须手动修补或转换，成本非常高昂。

### 抱歉，您的记忆正在泄漏……

高级语言提供了针对常见问题的内建解决方案。例如，大家都知道，大多数程序错误都与内存管理不当有关。在你使用一个对象之前，必须为它分配空间，正确初始化它，以某种方式跟踪它，并且在不再需要时正确地释放它。当然，这些任务每一项都是极其繁琐且容易出错的，哪怕是最轻微的错误也可能带来灾难性的后果。检测并修正这些错误是出了名的困难，因为它们通常对不同用户的配置和使用模式非常敏感。

用指向结构的指针（但忘记为其分配内存），你的程序将崩溃。使用一个没有正确初始化的结构，它会破坏你的程序，并且崩溃，但可能不会马上崩溃。如果你没有跟踪一个对象，可能会在它仍然在使用时就释放了它的空间。崩溃城市。最好再分配一些结构来跟踪你需要为其分配空间的结构。但如果你过于保守，除非完全确定一个对象不再使用，否则永远不回收它，小心了。很快，你会充满未回收的对象，内存用完，程序崩溃。这就是可怕的“内存泄漏”。

当你的内存空间变得碎片化时会发生什么？通常的解决办法是通过移动对象来整理，但在 C++ 中你不能这样做——如果你忘记正确更新对每个对象的每个引用，你会破坏程序并使其崩溃。

大多数真正的高级语言提供了解决方案——它叫做垃圾回收器。它会为你跟踪所有对象，当对象不再使用时回收它们，而且从不出错。当你使用内建垃圾回收器的语言时，会发生几件美妙的事情：

* 绝大多数的错误会立刻消失。是不是很棒？
* 你的代码变得更小，更易于编写和理解，因为它不再充斥着内存管理的细节。
* 你的代码更有可能在不同平台和不同配置下运行得更高效。

然而，C++ 用户不得不手动处理垃圾回收。许多人已经被洗脑，认为手动处理比使用专家为他们所使用的平台专门编写的东西更高效。这些人可能更喜欢通过请求盘片、磁道和扇区号来创建磁盘文件，而不是通过文件名来创建。虽然在某些配置下这样做可能更高效一两次，但你肯定不想这样使用文字处理器。

你甚至不必只听我们说。去读一读 B. Zorn 的《保守垃圾回收的测量成本》（技术报告 CU-CS-573-92，科罗拉多大学博尔德分校），它描述了一项研究的结果，比较了 C 语言中程序员优化的内存管理技术与使用标准垃圾回收器的性能。C 程序员通过自己编写垃圾回收器，表现的性能明显更差。

好吧，假设你是那些想要垃圾回收器的开明 C++ 程序员之一。你并不孤单，很多人都认为这是个好主意，并试图构建一个。哦，天哪，猜猜看，结果是你不能在 C++ 中添加垃圾回收器，得到的东西也远不如内建垃圾回收器的语言。首先，（惊讶！）当你的代码被编译并运行时，C++ 中的对象不再是对象了。它们只是一个连续的十六进制污泥。没有动态类型信息——没有办法让任何垃圾回收器（或者说，任何使用调试器的用户）指向任何随机的内存位置，并准确知道那里是什么对象，它的类型是什么，是否有人正在使用它。

第二件事是，即使你能编写一个垃圾回收器，偶尔能检测到对象，你在尝试重用别人代码时，仍然会遇到麻烦，特别是如果别人没有使用你的特定系统。由于 C++ 没有标准的垃圾回收器，这种情况肯定会发生。假设我用我的垃圾回收器写了一个数据库，你用你的垃圾回收器写了一个窗口系统。当你关闭其中一个包含我数据库记录的窗口时，你的窗口系统不知道如何通知我的记录它不再被引用了。这些对象就会一直挂在那里，直到所有可用空间都被填满——再次发生内存泄漏。

### 难以学习，且注定如此


C++ 还与汇编语言共享一个重要特点——它非常难以学习和使用，而且更难学会如何高效使用。


> 日期：1991 年 4 月 8 日 星期一 11:29:56 PDT
>
> 发件人：Daniel Weise [daniel@mojave.stanford.edu](mailto:daniel@mojave.stanford.edu)
>
> 收件人：Unix 痛恨者
>
> 主题：从他们的摇篮到我们的坟墓。
>
> Unix 程序之所以如此脆弱和不健壮，其中一个原因是 C 编程人员从小就被训练成编写这种程序。例如，Stroustrup 的 C++ 书中的第一个完整程序（在“hello world”程序之后，顺便说一句，这个程序编译成一个 300K 的镜像）是一个进行英寸到厘米和厘米到英寸转换的程序。用户通过在输入的数值后面附加“i”表示英寸，“c”表示厘米。以下是程序的概要，按照真正的 Unix 和 C 风格编写：
>
> ```cpp
> #include <stream.h>
> main() {
>     [声明]
>     cin >> x >> ch;
>     ;; 设计上的堕胎。
>     ;; 先读取 x，然后读取 ch。
>     if (ch == 'i') [处理 "i" 情况]
>     else if (ch == 'c') [处理 "c" 情况]
>     else in = cm = 0;
>     ;; 没错，不报告错误。
>     ;; 只做一些任意的操作。
>     [执行转换]
> }
> ```
>
> 十三页之后（第 31 页），给出了示例，演示了实现从 n 到 m 的索引数组，而不是通常的从 0 到 m。如果程序员给出了无效的索引，程序只是愉快地返回数组的第一个元素。Unix 的大脑死了，永远如此！

## 鸩水的语法糖

>语法糖会导致分号癌。
>
>——Alan Perlis

几乎每种你在 C 编程语言中可能犯的语法错误，在 C++ 中都被重新定义了，使得现在它能生成可编译的代码。不幸的是，这些语法错误并不总是能产生有效的代码。原因在于人类并不完美。他们会打错字。在 C 中，无论错误多么严重，这些打字错误通常都会被编译器捕捉到。而在 C++ 中，它们却悄悄通过，等到某人真正尝试运行代码时，才会带来麻烦。

C++ 的语法混乱源于它的语言遗产。C++ 从来没有经过正式设计：它是在不断演变中产生的。随着 C++ 的发展，添加了许多构造，它们引入了语言的歧义。为了消除这些歧义，采用了临时的规则。结果是，一门语言拥有毫无意义的规则，这些规则复杂到几乎无法学习。于是，大多数程序员把这些规则放在参考卡片上，或者干脆拒绝使用 C++ 的所有特性，只用有限的子集来编程。

举个例子，C++ 有个规则，规定任何既可以解析为声明又可以解析为语句的字符串，都应该被当作声明来处理。当解析专家读到这样的内容时，他们会不寒而栗，因为他们知道这样的规则非常难以正确实现。AT\&T 甚至没有正确实现其中一些规则。例如，当吉姆·罗斯金德试图弄清楚某些构造的意义时——这些代码片段，他认为合理的人类可能会有不同的理解——他将它们写出来并喂给 AT\&T 的“cfront”编译器。结果是，cfront 崩溃了。

事实上，如果你从互联网主机 ics.uci.edu 免费下载吉姆·罗斯金德的 C++ 语法文件，你会在目录 ftp/pub 中的文件 `c++grammar2.0.tar.Z` 里看到以下注释：“应该注意，我的语法不能与像 cfront 这样的实现保持一致，因为 a) 我的语法是内部一致的（大部分得益于其形式化和 yacc 验证），b) yacc 生成的解析器不会核心转储）（我可能会因为最后一句话而受到很多攻击，但……每次我在试图弄清楚一些 C++ 构造的语法含义时，如果 ARM 的描述不明确，而我把它交给 cfront，cfront 就会核心转储。）”

> 日期：1989 年 5 月 21 日 星期日 18:02:14 PDT
>
> 发件人：tiemann (Michael Tiemann)
>
> 收件人：[sdm@cs.brown.edu](mailto:sdm@cs.brown.edu)
>
> 抄送：Unix 痛恨者
>
> 主题：C++ 注释
>
> 日期：1989 年 5 月 21 日 23:59:37 GMT
>
> 发件人：[sdm@cs.brown.edu](mailto:sdm@cs.brown.edu) (Scott Meyers)
>
> 新组：comp.lang.c++
>
> 组织：布朗大学计算机科学系
>
> 考虑以下 C++ 源代码行：
>
> ```c
> //**********************
> ```
>
> 这应该如何被 C++ 编译器处理？GNU g++ 编译器将其视为注释至行尾，后面跟着一堆星号，但 AT\&T 编译器将其视为一个斜杠后跟着一个注释开始符号。我希望是前者的解释，但在 Stroustrup 的书中找不到任何说明指出应该期待其他解释。
> 实际上，快速编译 `-E` 显示问题出在预处理器上，所以我的问题是：
>
> 1. 这是 AT\&T 预处理器中的 bug 吗？如果不是，为什么？如果是，它会在 2.0 中修复吗，还是我们只能继续忍受它？
> 2. 这是 GNU 预处理器中的 bug 吗？如果是，为什么？
>
>Scott Meyers[sdm@cs.brown.edu](mailto:sdm@cs.brown.edu)
>
> 在 UNIX 中有个古老的规则，即应该接受的标记是最长的那个。因此，‘foo’并不是被解析为三个标识符‘f’，‘o’，‘o’，而是作为一个标识符‘foo’。看看这个规则在以下程序中的作用（以及为什么选择‘/*’作为注释分隔符是明智的）：
>
>```c
>double qdiv(p, q)
>double * p, * q;
>{
>    return * p
>    *q;  
>     }
>```
>
> 所以为什么在 C++ 的情况下不应用相同的规则呢？很简单，这是 bug。
>
> Michael

最糟糕的是，对于那些每天使用 C++ 的人来说，C++ 的最大问题是，即使只使用有限的子集，这门语言仍然很难阅读和理解。拿到另一个程序员的 C++ 代码，很难看一眼并迅速弄明白它的意思。这个语言没有品味，简直是一团糟。C++ 是一门想要自认为是面向对象的语言，但却没有承担面向对象编程的真正责任。C++ 假设任何足够复杂到想要垃圾回收、动态加载或其他类似特性的人，都足够复杂到能够自己实现这些功能，并且有时间去做并调试这个实现。

C++ 操作符重载的真正威力在于，它允许你将相对简单的代码变成一团乱麻，可以与最糟糕的 APL、ADA 或 FORTH 代码相媲美。每个 C++ 程序员都可以创建自己的方言，这种方言对于其他 C++ 程序员来说可能完全是个谜。

但是——嘿——即使是 C++，连标准方言也是私有的。

## 什么是抽象？

你可能认为 C++ 的语法是最糟糕的部分，但这只是当你刚开始学习它时的感觉。一旦你开始用 C++ 编写一个大型项目，你就会意识到，C++ 在抽象方面本质上是有缺陷的。正如任何计算机科学教材会告诉你的那样，抽象是合理设计的主要杠杆。

复杂性来自于系统中各个部分之间的相互作用。如果你有一款 100,000 行的程序，而任何一行代码可能依赖于其他某一行代码中出现的某个细节，你就得警惕 10,000,000,000 种可能的相互作用。抽象的艺术就在于通过将这些相互作用约束在少数几个良好文档化的接口中来降低复杂性。实现某些功能的代码块应该被隐藏在模块化的墙后面。

而 C++ 中的类，作为这门语言的核心，实际上是以一种违背模块化的方式实现的。它们暴露了如此多的内部细节，以至于使用类的用户会非常依赖于该类的实现细节。在大多数情况下，改变一个类会迫使所有可能引用它的代码重新编译。这通常会导致工作停滞，因为必须重新编译整个系统。你的软件不再是“柔软”的和可变的；它更像是速干水泥。

当然，你必须将一半的代码放入头文件中，仅仅是为了声明你的类让其他部分的代码能够使用。显然，类声明中的 public/private 区分毫无意义，因为“private”信息已经在头文件中，这些信息因此变成了公共信息。一旦将信息放入头文件中，你就不愿意更改它们，这样一来就不得不重新编译。程序员开始采取非常规的手段，通过曲折的机制来添加或更改功能，避免修改头文件。他们可能会遇到一些其他的保护机制，但由于有许多方法可以绕过这些机制，这些保护措施对于急于违反协议的人来说不过是些小小的“减速带”。将一切强制转换为 `void*`，然后一切类型检查都不再烦人。

许多其他语言提供了经过深思熟虑的机制，用于不同种类的抽象。C++ 也提供了一些这样的机制，但错过了许多重要的种类。它提供的抽象机制混乱且难以理解。你是否遇到过任何喜欢使用模板的人？结果是，许多概念的表达方式依赖于它们出现的上下文以及它们的使用方式。许多重要的概念根本无法以简单的方式表达；只要表达出来，也无法为它们命名，以便随后直接调用。

例如，命名空间是防止你的代码中的一组名称与另一部分代码中的另一组名称发生冲突的常见方式。一个为服装制造商编写的程序可能有一个名为 Button 的类，它可能与另一个名为 Button 的用户界面工具包类相链接。使用命名空间，这没问题，因为两者的使用规则和含义是明确且易于区分的。

但在 C++ 中就不一样了。你无法确保自己没有使用程序中某个地方已经使用过的名字，可能会造成灾难性的后果。你唯一能做的就是通过一些无意义的前缀，如 ZjxButton，来混淆代码，并希望别人不会也这样做。

> 日期：1994 年 3 月 18 日 星期五 10:52:58 PST
>
> 发件人：Scott L. Burson [gyro@zeta-soft.com](mailto:gyro@zeta-soft.com)
>
> 主题：预处理器 C 粗人会告诉你，C 的最佳特性之一就是预处理器。实际上，它可能是最糟糕的。许多 C 程序是由 `#ifdef` 构成的难以理解的乱麻（如果各种版本的 Unix 实际上是兼容的，这些大多数都不需要存在）。但这只是问题的开始。
>
> C 预处理器最糟糕的问题是它把 Unix 世界锁进了文本文件的监狱，并且扔掉了钥匙。几乎没法以任何形式存储 C 源代码，除非是线性文本文件。为什么？因为几乎不可能解析未经预处理的 C 代码。例如，考虑以下代码：
>
>```c
>#ifdef BSD
>int foo() {
>        #else
>        void foo() {
>            #endif
>            /* ... */
>        }
>```
>
> 在这里，函数 foo 根据宏 `BSD` 是否被定义有两个不同的开始。要在原始形式中解析这种东西几乎是不可能的（据我们所知，这从未实现过）。
>
> 为什么这这么垃圾？因为它限制了我们能够在编程环境中加入的智能。大多数 Unix 程序员不习惯使用这样的环境，也不知道自己错过了什么，但有许多极其有用的功能，在源代码的自动化分析变得可能时，可以轻松提供。
>
> 让我们来看一个例子。在 C 语言大部分时间里，预处理器是获取表达式开码（通过直接插入指令流而不是函数调用来编译）的唯一方法。对于非常简单且常用的表达式，开码是一项重要的效率技术。例如，min，它在上面刚才提到过，通常被定义为一个预处理器宏：
>
> ```c
> #define min(x,y) ((x) < (y) ? (x) : (y))  
> ```
>
> 假设你想编写一个工具，打印出程序中所有引用 min 的函数列表。听起来是个简单的任务，对吧？但是，你无法知道函数的边界，因为你不能在不解析程序的情况下解析它，而你又不能在没有经过预处理器的情况下解析程序，一旦你做了预处理，所有的 min 实例就都被去掉了！所以你只能用 grep 来做了。
>
> 使用预处理器进行开码还有其他问题。例如，在刚才展示的 min 宏中，你会注意到一堆看似冗余的括号。实际上，这些括号必须全部提供，否则当 min 宏在另一个表达式中展开时，结果可能无法按预期解析（实际上，它们并非全都必要——哪些可以省略，以及为什么，这留给读者自行思考）。
>
> 但这个 min 宏最糟糕的问题是，尽管它看起来像是一个函数调用，但它并不像函数调用那样工作。考虑一下：
>
> ```c
> a = min(b++, c);  
> ```
>
> 通过文本替换，这将展开成：
>
> ```c
> a = ((b++) < (c) ? (b++) : (c));  
> ```
>
> 所以，如果 `b` 小于 `c`，`b` 将被递增两次，而不是一次，返回的值将是 `b` 的原始值加 1；另一方面，如果 min 是函数，那么 `b` 只会递增一次，返回的值将是 `b` 的原始值。


## C++ 与 C，如同肺癌与肺

>“如果 C 语言能给你足够的绳子让你上吊，那么 C++ 能给你足够的绳子让你捆绑和塞住邻居的嘴，装配小船上的帆，甚至还有足够的绳子让你从桅杆上上吊。”
>
>——佚名

遗憾的是，尽管如此，对每位计算机科学家和严肃的程序员来说，学习 C++ 可能是最符合他们利益的事情。它很快就成了简历上的一项标配。在过去几年里，我们认识了许多会用 C++ 编程的程序员，甚至能用这门语言写出相当不错的程序……

……但他们讨厌它。

## 程序员的进化

### 高中/初中

```basic
10 PRINT "HELLO WORLD"  
20 END  
```

### 大学一年级

```pascal
program Hello(input, output);  
begin  
  writeln ('Hello world');  
end.  
```

### 大学四年级

```lisp
(defun hello ()  
  (print (list 'HELLO 'WORLD)))  
```

### 新手专业级程序员

```c
#include <stdio.h>

main (argc, argv)  
  int argc;  
  char **argv; {  
    printf ("Hello World!\n");  
}
```

### 资深专业级程序员

```cpp
#include <stream.h>

const int MAXLEN = 80;

class outstring;  

class outstring {  
private:  
  int size;  
  char str[MAXLEN];  

public:  
  outstring() { size=0; }  
  ~outstring() {size=0;}  
  void print();  
  void assign(char *chrs);  
};  

void outstring::print() {  
  int i;  
  for (i=0 ; i< size ; i++)  
    cout << str[i];  
  cout << "\n";  
}  

void outstring::assign(char *chrs) {  
  int i;  
  for (i=0; chrs[i] != '\0'; i++)  
    str[i] = chrs[i];  
  size = i;  
}  

main (int argc, char **argv) {  
  outstring string;  
  string.assign("Hello World!");  
  string.print();  
}
```

### 经理

“George，我需要一款程序来输出字符串‘Hello World!’”

