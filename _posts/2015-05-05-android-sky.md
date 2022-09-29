---
layout: post
title: Dart更近一步，Sky会一统江湖吗？
date: 2015-05-05
categories: Dart
---

从接触编程到现在，除了搞过几天JQuery，几乎没怎么写过Javascript，刚刚看了两篇介绍 ECMAScript6 的文章，突然觉得没写过JS也没什么好遗憾的。

<!--more-->

* [ES6 In Depth: An Introduction](https://hacks.mozilla.org/2015/04/es6-in-depth-an-introduction/)
* [ES6 In Depth: Iterators and the for-of loop](https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/)

ES6 好像从2009年就开始制定了，现在终于支持 `forEach`、`for-in`等操作，也支持`Map`、`Set`等数据类型，而且为了考虑兼容性问题居然引入了一个 `for-of`，不过看到 [Githut](http://githut.info/) 上关于 github 语言的统计数据，不得不佩服JS社区强大的生产力。

话说回来，Dart 作为一个崭新的语言，自诞生那天起就抛去了向下兼容的历史包袱，而且可以直接转成 Javascript，Chrome 的 V8 团队还专门为 Dart 做了一个虚拟机 - Dartium。

Dart 目的跟 Node 一样，也是为了统一前后端开发，这一点在上一篇文章 （[Dart是一个怎样的语言？](http://blog.csdn.net/feelang/article/details/45469151) ）已经说过了，所以用 Dart 做 web 开发也没有额外的学习成本，当然前提是你得会写 Dart。

官方教程提供的一个简单的 web 开发教程 - [Avast, Ye Pirates: Write a Web App](https://www.dartlang.org/codelabs/darrrt/)，用`DartEditor`导入后，工程结构如下图所示：

![](/assets/imgs/dart-project-structure.png)

有css，有html，一个最简单的web工程（没有后端），在 `DartEditor` 中可以用两种方式来运行这个工程。

![](/assets/imgs/dart-run.png)

如果选择了 `Dartium`，编译成功后会唤起一个使用了 Dartium 引擎的 chrome 浏览器，而过选择了 `Run as JavaScript` 就会先把 dart 编译成 js 的工程（工程结构图中灰色的部分），然后唤起一个使用了 V8 引擎的 chrome 浏览器。

其实用 Dart 做开发还是挺方便的，js 都是可以直接拿来用的，但是社区不成熟，不像 node 社区那样有那么多的库。

---

我们再来看看下一代 Android 开发框架 - [sky](https://github.com/domokit)，今天照着 readme 玩了一下官方提供的几个demo，流畅度可以跟 native 媲美，但是需要从网络加载代码，所以启动时间比较慢，毕竟只是一个实验版本，像 react-native 那样做个本地缓存也不会有什么问题。

整个开发过程与上面的 web 开发非常相似，只不过代码文件的后缀名换了而已。

首先需要创建一个 `pubspec.yaml`，类似于 Node 的 `package.json` 或者 gradle 脚本的 `build.gradle`，主要是一些包依赖关系和 APP 的基本信息，最后一行表示依赖最新版本的 sky。

```yaml
name: your_app_name
dependencies:
 sky: any
```

在当前目录下执行 `pub get`，会根据 `pubspec.yaml` 的依赖配置获取 APP 所依赖的包。

```shell
➜  widgets git:(master) ✗ pub get
Resolving dependencies... (1.7s)
+ mojo 0.0.5+dart-summit-1
+ sky 0.0.5+dart-summit-7
Changed 2 dependencies!
➜  widgets git:(master) ✗
```

执行完毕后会发现在本地多了一个 `package` 文件夹，里面有刚刚下载的两个包。

![这里写图片描述](http://img.blog.csdn.net/20150505003910350)

*pub会首先把下载来的包缓存到本地，如果有的新的下载可以直接引用之前下载过的包。*

sky 我们都知道了，它就是 Android 全新的开发框架，由两部分组成：

<pre>
<i>The Sky engine</i>. The engine is the core of the system. Written in C++, the engine provides the muscle of the Sky system. The engine provides several primitives, including a soft real-time scheduler and a hierarchial, retained-mode graphics system, that let you build high-quality apps.

<i>The Sky framework</i>. The framework makes it easy to build apps using Sky by providing familiar user interface widgets, such as buttons, infinite lists, and animations, on top of the engine using Dart. These extensible components follow a functional programming style inspired by React.
</pre>

简单来说，*Sky engine* 是一个图形系统，VDOM 的创建和diff应该也是它负责的，而 *Sky framework* 则是一个UI库，提供了我们创建 VDOM 时所需的节点元素。

那 mojo 又是什么呢？

<pre>Mojo is an effort to extract a common platform out of Chrome's renderer and plugin processes that can support multiple types of sandboxed content, such as HTML, Pepper, or NaCl.</pre>

简单来说，mojo 就是 sky 的运行时环境，但是 domokit 下还有一个[mojo-sdk](https://github.com/domokit/mojo_sdk)，这个 sdk 为我们提供给了基于 mojo 做二次开发所用到的 API。

<pre>The Mojo Public API is a binary stable API to the Mojo system.</pre>

它支持很多种语言，目前为止包括 `C`、`CPP`、`Dart`、`Go`、`Java`、`js`。

也就是说，Google 想打造的是这样一个生态系统。

![](/assets/imgs/dart.png)

---

如果这个愿景能够实现，120fps的卖点也许会一统江湖，但是 Google IO 2015 根本没有提及这个项目，希望 Google 不是玩票 :(
