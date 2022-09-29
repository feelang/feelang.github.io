---
layout: post
title: 彻底搞懂 npm、npx、yarn
date: 2020-11-05
categories: tools
---

要彻底搞清楚 npm、npx、yarn 的区别，先记住下面两条：

* npm 只负责安装 package，不负责执行，yarn 也是，但是比 npm 好用。
* npx 不负责安装，只负责执行 package。

首先举个例子。

npm 安装某个 package 的命令如下：

```bash
$ npm install some-package
```

上面这种安装方式，`install` 后面如果没有跟 -g ，依赖包只能安装在当前目录下。

也就是说 some-package 的路径无法在环境变量 `$PATH` 中体现，因此也就无法在终端直接被执行。

按照“传统工艺”，如果硬要执行 some-package，只能把路径拼完整了才可以。

```bash
$ ./node_modules/.bin/some-package
```

但是这么做显然非常麻烦，手速跟不上思路，影响效率。

所以，“一般做法”是借助 npm 稍作简化，在 package.json 的 scripts 中增加一条：

```json
{
  "name": "whatever",
  "version": "1.0.0",
  "scripts": {
    "some-package": "some-package"
  }
}
```

然后像下面这样执行：

```bash
$ npm run some-package
```

如此一来可以不用拼路径，但是修改 package.json 本身也是一件麻烦事。

于是 npx 闪亮登场。

有了它，npm install 之后的 package 只需要一行命令就可以执行，再也不需要拼路径，也无需修改 package.json 文件了。

```bash
$ npx some-package
```

简单总结一下：

* npm 是 Package Manager，负责管理包
* npx 是 Package eXecutor，负责执行包

那 yarn 又是什么鬼呢？

很简单，yarn 是一个用于取代 npm 的包管理工具，它的优势在于：

* 版本稳定（借助 yarn.lock，类似 cocoapods 的 Podfile.lock）
* 多线程下载 

总之记住一句话：yarn 比 npm 好用。

## 参考资料
* [javascript - Difference between npx and npm? - Stack Overflow](https://stackoverflow.com/questions/50605219/difference-between-npx-and-npm)
