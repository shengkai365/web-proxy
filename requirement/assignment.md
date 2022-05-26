## COMP3310 2022 - Assignment 2: An annoying web-proxy

### 1. 背景

- 这项作业占最终分数的15%
- 应在美国东部时间4月22日星期五23:55之前提交--注意：堪培拉时间（gmt+10）
- 除非有特殊情况，否则不接受逾期提交的材料
  - 必须在截止日期前尽早通过课程召集人申请延期，并提供适当的证据或理由。
- 如果您希望对您提交的材料的某些方面得到反馈，请在您提交的材料中的`README`文件中注明。

这是一个编码任务，以加强和检查你的网络编程技能。主要重点是本地套接字编程，以及你理解和实现RFC规范中应用协议的关键元素的能力。

### 2. 作业2 大纲

网络代理是一个简单的网络客户端和网络服务器包裹在一个单一的应用程序中。它接收来自一个或多个客户端（网络浏览器）对特定内容URL的请求，并将其转发到预定的服务器，然后将结果以某种形式返回给你的网络浏览器。这有什么用呢？

- 它可以缓存内容，使第二个及以后的客户提出相同的请求时得到更快速的响应，并释放网络容量。
- 它可以过滤内容，以确保回来的内容是 "安全的"，例如，对儿童或你的家，或对组织内的员工/他们的电脑。
- 它可以过滤请求，以确保人们不访问他们不应该访问的东西，无论人们有什么政策原因。
- 它可以监听请求/响应并学习一些东西，即窥探流量。不过，让人们使用你的代理是一个不同的挑战...
  - 当然，它还可以监听和修改请求/回应，以获得乐趣或利益。

在这项任务中，你需要用C、Java或Python [1] 编写一个网络代理，而不使用任何外部的web/`http`相关的库（不过支持`html`解析也可以）。

你的代码必须按照教程中的练习，以标准的`socket()` API方式打开 socket。你的代码必须自己做出适当的、格式正确的HTTP/1.0（RFC1945）或HTTP/1.1增强型请求（作为客户端，向网络服务器发出）和响应（作为服务器，向网络浏览器发出），并在两个方向上自己捕获/解释其结果。你将手工制作HTTP数据包，所以你需要了解请求/响应的结构和关键的HTTP头。

Wireshark在调试方面会有帮助。最常见的陷阱是在请求中没有把行尾的"\n\n "写对，这是与操作系统和语言有关的。记住在发送时要保守，在接受时要合理地自由。

> [1]由于大多数高性能的网络服务器和内核网络模块都是用C语言编写的，而其他语言则远远次之，因此值得学习。但是，时间很短。如果你想使用其他语言（在C/Java/Python之外），请与你的导师讨论--它必须有本地套接字访问，而且必须有人能够对它评分。

你的成功和高评分的代理将需要做什么：

1. 作为一个著名网站的代理，http://comp3310.ddns.net/
   - 该网站还没有完全投入使用，当它投入使用时将会发布公告。它将是澳大利亚国家植物园网站的一个近似的镜像网站。
2. 重写原来指向网站的绝对 (简单) URL链接，现在指向你的代理，所以所有后续的请求（到我们的网站）也要通过你的代理。
   - 有时链接不是以纯粹的`<a href="...">`风格写成的，例如，它们是在`javascript`中计算出来的，在检查之后，我们将接受这些中断。
3. 修改文本内容，用粗体字 "eht"替换正文中的每个 "the"字（即在html中写成`<b>eht</b>`）。
4. 日志（打印到 `STDOUT` ）：
   - 每个请求的时间戳
   - 每一个进入你的代理的客户请求，如收到的（'GET / HTTP/1.0'，等等）
     - 不要记录其他头信息
   - 每一个回来的服务器状态反应（200 OK, 404 Not found, 等等）
     - 不要记录其他头信息
   - 计算你的代理对该页面所做的修改，分别计算文字修改和链接重写（即返回两个标记的数字）

我们将对指定的网站进行测试，通过运行您的代码，打开我们的网络浏览器，向您的运行代理发出顶级（'/'）页面请求，就像它是服务器一样，我们应该得到我们经过适当修改[2]的远程主页。我们在浏览器中点击的任何（简单的）链接都应该把我们带回你的代理，并再次进入下一个页面的网站，等等。我们不打算走得太深，有一些过于复杂的页面，我们将只挑选几个。每次只有一个客户端浏览器对你的代理运行。注意，这是一个互动的过程，你没有缓存或以其他方式存储修改的页面。

你应该只需要管理HTML页面（检查Content-Type头）的修改。任何来自网站的非HTML内容（如图像、JS、CSS等）都可以不加改动地通过。不要忘了捕捉和穿越请求中的所有头信息，因为该网站可能至少需要HTTP/1.1 "Host: " header

为了提高效率，你也可以使用持久的 http/tcp 连接，但要注意连接超时。

> [2] 大多数浏览器支持直接配置代理地址，但行为可能有点不一致，所以我们试图避免这种情况。

### 3. 提交和评估

你需要提交你的源代码，以及一个可执行文件（如果合适）。如果它需要运行说明，请在README文件中提供这些说明。你提交的文件必须是一个压缩文件，根据需要打包所有内容，并通过wattle上的适当链接提交。

有许多现有的网络代理/缓存工具和库，其中许多都有源代码。虽然对你来说可能是教育性的，但评审员知道它们的存在，他们会对照它们和本班的其他作品检查你的代码。

你的代码将被评估为 [with marks% available]

1. 输出正确性 [40%]
   - 它代表客户浏览者向服务器发送的 http 查询
   - 它返回给客户端浏览器包含修改后的服务器内容的 http
   - 用户能够在其浏览器中跟踪链接
   - 如上所述的请求/回应的日志
2. 性能 [20%]
   - 一个优秀的代理应该是完全透明的，不会造成任何明显的延迟。
   - 使用标准的Linux环境（如CS实验室、WSL），代码的运行有多容易？

3. 代码的正确性、清晰性和风格 [40%]
   - 使用本地套接字，编写自己的HTTP发送者/接收者信息
   - 文档，即注释和任何`README` —— 新来的人有多容易接受并修改它

可能会有粗糙的HTML页面，在图像地图中嵌入脚本和链接，以及其他技巧，还有许多对其他网站的引用。在某些情况下，我们会对粗糙的链接放松警惕，你不应该代理那些不在`comp3310.ddns.net`网站上的链接或请求。

你应该能够在任何你喜欢的基于HTTP的网站上测试你的代码，尽管现在很多网站都使用HTTPS，或者有复杂的html/js页面，这可能会使解析更加困难。Wireshark对于检查你的代码与浏览器或命令行工具（如wget/curl）的行为非常有帮助。你的导师可以帮助你提供建议（直接或通过论坛），同学也可以。